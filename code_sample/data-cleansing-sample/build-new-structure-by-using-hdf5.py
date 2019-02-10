import numpy as np
import pandas as pd
import h5py
from random import shuffle
from scipy.misc import imread, imresize
import glob
from math import floor
from random import randint
#import image_processing

def read_info_h5(info_csv, shuffle_data=True):
    info = pd.read_csv(info_csv)
    image_path = info['path'].values
    side = info['side'].values
    field = info['field'].values

    if shuffle_data:
        c = list(zip(image_path, side, field))
        shuffle(c)
        image_path, side, field = zip(*c)
    """
    train_image_path = image_path[0:int(0.6*len(image_path))]
    train_side = side[0:int(0.6 * len(side))]
    train_field = field[0:int(0.6 * len(field))]
    train = zip(train_image_path, train_field, train_side)

    val_image_path = image_path[int(0.6 * len(image_path)):int(0.8 * len(image_path))]
    val_side = side[int(0.6 * len(side)):int(0.8 * len(side))]
    val_field = field[int(0.6 * len(field)):int(0.8 * len(field))]
    val = zip(val_image_path, val_field, val_side)

    test_image_path = image_path[int(0.8 * len(image_path)):]
    test_side = side[int(0.8 * len(side)):]
    test_field = field[int(0.8 * len(field)):]
    test = zip(test_image_path, test_field, test_side)
    """
    data = zip(image_path, side, field)
    return data


def read_image_convert_h5(zip_info, name, h=2000, w=2000, c=3, data_order='tf'):
    hdf5_path = '/mnt/dfs/han/eye-project/data_for_hash.hdf5'
    image_path, side, field = zip(*zip_info)
    shape = (len(image_path), h, w, c)

    hdf5_file = h5py.File(hdf5_path, mode='w')
    hdf5_file.create_dataset("image", shape, np.float32)
    hdf5_file.create_dataset("side", (len(side),), np.int32)
    hdf5_file.create_dataset("field", (len(field),), np.int32)

    print(shape, len(side), len(field))

    path0 = '/mnt/huge-dataset/DR-data-2.4m'

    for i in range(len(image_path)):
        if i % 5 == 0 and i > 1:
            print('Train data: {}/{}'.format(i, len(image_path)))
        path = path0 + image_path[i]
        path = path.replace("\\", "/")
        img = imread(path)
        if len(img.shape) != 3:
           continue

        if img.shape[2] == 3:
           img = imresize(img, (2000, 2000))
        else:
           continue

        hdf5_file['image'][i, ...] = img[None]
        hdf5_file['side'][i] = side[i]
        hdf5_file['field'][i] = field[i]
    hdf5_file.close()



def read_batches(file_name,  batch_size):
    f = h5py.File(file_name, 'r')
    image = f["image"]

    data_num = image.shape[0]

    i = randint(1, data_num - 100*batch_size)
    # i_e = min([(batches_list[0] + 1) * batch_size, data_num])

    labels = []
    temp = 0
    index = []

    while i < data_num and temp < batch_size:
        if f["field"][i] == 4:
            i+=1
        
        elif f["field"][i] == 1:
            if f["side"][i] == 0:
                labels.append(0)
            else:
                labels.append(0)
            index.append(i)
            temp += 1
            i += 1

        elif f["field"][i] == 2:
            if f["side"][i] == 0:
                labels.append(1)
            else:
                labels.append(1)
            index.append(i)
            temp += 1
            i += 1

        else:
            if f["side"][i] == 0:
                labels.append(2)
            else:
                labels.append(2)
            index.append(i)
            temp += 1
            i += 1
    batch_images = f["image"][index,...]    
    return batch_images, labels


def cal_mean_std(file_name):
    f = h5py.File(file_name, 'r')
    image = f["image"]

    red_mean = np.mean(f["image"][:,:,:,0])
    green_mean = np.mean(f["image"][:,:,:,1])
    blue_mean = np.mean(f["image"][:,:,:,2]) 

    red_std = np.std(f["image"][:,:,:,0])
    green_std = np.std(f["image"][:,:,:,1])
    blue_std = np.std(f["image"][:,:,:,2])

    return red_mean, green_mean, blue_mean, red_std, green_std, blue_std


def transform_data():
    train = read_info_h5("test_data.csv")
    read_image_convert_h5(train, 'train', 2000, 2000, 3)
    #read_image_convert_h5(train, 'test', 224, 224, 3)
    #read_image_convert_h5(train, 'val', 224, 224, 3)


if __name__ == '__main__':
    transform_data()


