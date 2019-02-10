from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import h5_side
import tensorflow as tf
import vgg
from datetime import datetime
import numpy as np
import os
from sklearn.metrics import confusion_matrix
import tensorflow.contrib.slim as slim

MAX_STEP = 12345
slim = tf.contrib.slim

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

flags = tf.app.flags

flags.DEFINE_integer('batch_size', 35, 'The batch size')
flags.DEFINE_float('initial_learning_rate', None, 'Learning rate at begining.')
flags.DEFINE_integer('learning rate', None, 'learning rate')
flags.DEFINE_string('model_path', 'vgg_16.ckpt', 'path to the checkpoint')
flags.DEFINE_integer('dropout_keep_prob', 0.5, 'drop_keep_prob')
flags.DEFINE_string('log_save_dir',  "/mnt/dfs/han/eye-project/vgg/checkpoint_side/", 'save dir')
FLAGS = flags.FLAGS

now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
root_logdir = 'tf_logs'
logdir = "{}/run-{}/".format(root_logdir, now)


def train():
    with tf.Graph().as_default() as g:

        # variables_to_restore = slim.get_variables_to_restore(exclude=['vgg_16/fc8'])
        # init_assign_op, init_feed_dict = slim.assign_from_checkpoint('/mnt/dfs/han/eye-project/vgg_16.ckpt', variables_to_restore)

        tf.logging.set_verbosity(tf.logging.INFO)

        image1 = tf.placeholder(tf.float32, shape=[FLAGS.batch_size, 224, 224, 3])
        image2 = tf.placeholder(tf.float32, shape=[FLAGS.batch_size, 224, 224, 3])

        labels1 = tf.placeholder(np.int32, shape=[FLAGS.batch_size, ])
        labels1 = tf.cast(labels1, tf.int64)
        labels2 = tf.placeholder(np.int32, shape=[FLAGS.batch_size, ])
        labels2 = tf.cast(labels2, tf.int64)

        labels = tf.placeholder(np.int32, shape=[FLAGS.batch_size, ])

        hot_labels1 = slim.one_hot_encoding(labels1, 10)
        hot_labels2 = slim.one_hot_encoding(labels2, 10)

        with slim.arg_scope(vgg.vgg_arg_scope()):
            net1, end_points1 = vgg.vgg_16(image1, num_classes=0, scope='vgg16', is_training=True, reuse=False)
            net1 = slim.fully_connected(net1, 10, activation_fn=None, scope='fc8', reuse=False)
            logits1 = tf.squeeze(net1, [1, 2], name='fc8/squeezed')

            net2, end_points2 = vgg.vgg_16(image2, num_classes=0, scope='vgg16', is_training=True, reuse=True)
            net2 = slim.fully_connected(net2, 10, activation_fn=None, scope='fc8_2', reuse=True)
            logits2 = tf.squeeze(net2, [1, 2], name='fc8_2/squeezed')

            with tf.name_scope('Metrics'):
                with tf.name_scope('loss') as scope:
                    # loss1, loss2 may not be used
                    cross_entropy1 = tf.losses.sigmoid_cross_entropy(logits=logits1, multi_class_labels=hot_labels1)
                    loss1 = tf.reduce_mean(cross_entropy1, name='loss')

                    cross_entropy2 = tf.losses.sigmoid_cross_entropy(logits=logits2, multi_class_labels=hot_labels2)
                    loss2 = tf.reduce_mean(cross_entropy2, name='loss')

                    regularization_loss = tf.add_n(slim.losses.get_regularization_losses())
                    loss = between_class_loss(logits1, logits2, labels)

                    total_loss = loss1 + loss2 + loss

                with tf.name_scope('Optimizer'):
                    global_step = tf.Variable(0, trainable=False, name='global_step')
                    starter_learning_rate = 0.00005
                    # lr = tf.train.exponential_decay(starter_learning_rate, global_step, 500, 0.6, staircase=True)
                    lr = 0.0005
                    optimizer = tf.train.AdamOptimizer(0.00005)

                    update_op = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
                    train_var = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)

                    train_op = slim.learning.create_train_op(total_loss, optimizer,
                                                             global_step=global_step,
                                                             update_ops=update_op,
                                                             variables_to_train=train_var)

                with tf.name_scope('accuracy') as scope:
                    predictions = tf.equal(tf.arg_max(logits1, 1), tf.arg_max(logits2, 1))
                    correct = tf.equal(predictions, labels)
                    correct = tf.cast(correct, tf.float32)
                    # accuracy = tf.reduce_mean(correct) * 100.0
                    accuracy, accuracy_update = tf.contrib.metrics.streaming_accuracy(predictions, labels)
                    metric_op = tf.group(accuracy_update)

                saver = tf.train.Saver(slim.get_variables_to_restore())

        with tf.Session(graph=g) as sess:
            coord = tf.train.Coordinator()
            tf.train.start_queue_runners(sess=sess, coord=coord)
            #sess.run(init_assign_op, init_feed_dict)
            sess.run(tf.global_variables_initializer())
            sess.run(tf.local_variables_initializer())
            saver.restore(sess, "/mnt/dfs/han/eye-project/vgg/checkpoint_side/model.ckpt-800")
            global_step = sess.run(global_step)

            try:
                for step in np.arange(global_step, MAX_STEP):
                    if coord.should_stop():
                        break

                    x, y= h5_side.read_batches('/mnt/local/han/train.hdf5', FLAGS.batch_size)
                    val_x, val_y = h5_side.read_batches('/mnt/local/han/train_1.hdf5', FLAGS.batch_size)

                    if(x.shape[0] != FLAGS.batch_size) or (val_x.shape[0] != FLAGS.batch_size):
                        continue

                    sess.run([train_op], feed_dict={image1: x, labels:y, val_images:val_x, val_labels:val_y})

                    rs_labels, rs_val_labels = sess.run([labels, val_labels], feed_dict = {labels:y, val_labels:val_y})
                    rs_logits, rs_loss, rs_accuracy = sess.run([logits, loss, accuracy], feed_dict = {image:x, labels:y})
                    #current_lr = sess.run(lr)
                    print("step:", step)
                    print('loss:', rs_loss, '  accuracy:', rs_accuracy)

                    rs_loss_val, rs_accuracy_val, rs_logits_val = sess.run([loss_val, accuracy_val, logits_val], feed_dict = {val_images:val_x, val_labels:val_y})

                    print('loss_val:', rs_loss_val)
                    print('accur_val:', rs_accuracy_val)



                    if step % 30 == 0 or step+1 == MAX_STEP:
                        #print("predictions:", tf.arg_max(rs_logits, 1).eval())
                        print("true:", rs_labels)

                        summary_str = sess.run(summary_op, feed_dict = {image:x, labels:y})
                        writerTrain.add_summary(summary_str, step)
                        writerTrain.flush()

                    #if step % 50 == 0 or step+1 == MAX_STEP:
                        val_summary_str = sess.run(val_summary_op, feed_dict = {val_images:val_x, val_labels:val_y})
                        writerVal.add_summary(val_summary_str, step)
                        writerVal.flush()

                        #print('loss_val:', rs_loss_val)
                        #print('accur_val:', rs_accuracy_val)
                        val_pred = np.argmax(rs_logits_val, 1)

                        print("true:", rs_val_labels)
                        print("pred:", val_pred)

                        print('Train CM:')
                        cm_train = confusion_matrix(y_true=rs_val_labels, y_pred=val_pred)
                        print(cm_train)
                        print('\t')
                    if step % 200 == 0 or step+1 == MAX_STEP:
                        checkpoint_path = os.path.join(FLAGS.log_save_dir, 'model.ckpt')
                        saver.save(sess, checkpoint_path, global_step=step)

            except tf.errors.OutOfRangeError:
                print('Done training -- epoch limit reached')



def between_class_loss(logits1, logits2, label, m=5.0):
    logits1 = tf.cast(logits1, tf.float32)
    logits2 = tf.cast(logits2, tf.float32)

    dist_sim = [[np.sum((l1 - l2) ** 2) for l2 in logits2] for l1 in logits1]
    dist_dissim = np.max([0, m**2 - dist_sim])
    return dist_sim * label + (1 - label) * dist_dissim
