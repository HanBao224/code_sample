import unittest
import database
import psycopg2


class TestStringMethods(unittest.TestCase):
    def test_init_db(self):
        self.assertTrue(database.init_db())
        con = psycopg2.connect(database="music", user="honka",
                               password="daichan224",
                               host="localhost")
        cur = con.cursor()
        cur.execute("SELECT * FROM songs")
        i = cur.fetchone()
        self.assertTrue(i == None)

        cur.execute("SELECT * FROM idx_table")
        i = cur.fetchone()
        self.assertTrue(i == None)
        con.close()

    def test_build_table(self):
        self.assertTrue(database.init_db())
        self.assertTrue(database.build_tables("MUSIC_test/"))
        con = psycopg2.connect(database="music", user="honka",
                               password="daichan224",
                               host="localhost")
        cur = con.cursor()
        cur.execute("SELECT id, song_name from idx_table")
        i = cur.fetchone()
        self.assertEqual(i[0], 1)
        self.assertEqual(i[1], 'MUSIC_test/test_12s.wav')

        cur.execute("SELECT * from songs")
        i = cur.fetchone()
        self.assertEqual(i[0], 1)  # line_id
        self.assertEqual(i[1], 1)  # song_index
        self.assertEqual(len(i[2]), 6000)  # first window's fingerprint
        con.close()

    def test_query_song(self):
        self.assertTrue(database.init_db())
        self.assertTrue(database.build_tables("MUSIC_test/"))
        rtn = database.query_song(1)
        self.assertEqual(rtn[0], 1)  # song_index
        self.assertEqual(len(rtn[1]), 6000)  # first window's fingerprint

    def test_query_song_info(self):
        self.assertTrue(database.init_db())
        self.assertTrue(database.build_tables("MUSIC_test/"))
        rtn = database.query_song_info(1)
        self.assertEqual(rtn[0], 1)
        self.assertEqual(rtn[1], 'MUSIC_test/test_12s.wav')

    def test_get_all_fingerprint(self):
        self.assertTrue(database.init_db())
        self.assertTrue(database.build_tables("MUSIC_test/"))
        hash_input = database.get_all_fingerprint()

        self.assertEqual(len(hash_input), 3)
        self.assertEqual(hash_input[0].size, 6000)

    def test_hashing_and_query(self):
        # test hash_query if we do not remove the duplicates
        self.assertTrue(database.init_db())
        self.assertTrue(database.build_tables("MUSIC_test/"))
        hash_input = database.get_all_fingerprint()
        query_table = database.hashing(hash_input)
        info, min_distance = database.query_hash_nearest(
                             'MUSIC_test/test_12s.wav', query_table)
        self.assertEqual(info[0], 1)
        self.assertEqual(info[1], 'MUSIC_test/test_12s.wav')
        self.assertTrue(min_distance < 0.0001)  # small error due to hashing

    def test_detect_duplicate(self):
        self.assertTrue(database.init_db())
        self.assertTrue(database.build_tables("MUSIC_test/"))
        self.assertTrue(database.detect_duplicates('MUSIC_test/test_12s.wav'))

    def test_insert_new_song(self):
        self.assertTrue(database.init_db())
        self.assertTrue(database.build_tables("MUSIC_test/"))
        self.assertTrue(database.insert_new_songs('MUSIC_test/test_12s.wav'))

        con = psycopg2.connect(database="music", user="honka",
                               password="daichan224",
                               host="localhost")
        cur = con.cursor()

        cur.execute("SELECT id from songs")
        i = cur.fetchall()
        self.assertEqual(len(i), 3)
        con.close()

    def test_insert_new_info(self):
        info_list = ["abc"]
        col_name = "singer"
        self.assertTrue(database.init_db())
        self.assertTrue(database.build_tables("MUSIC_test/"))

        database.insert_new_info(info_list, col_name)
        con = psycopg2.connect(database="music", user="honka",
                               password="daichan224",
                               host="localhost")
        cur = con.cursor()

        cur.execute("SELECT singer from idx_table")
        i = cur.fetchall()
        self.assertEqual([('abc',)], i)


if __name__ == '__main__':
    unittest.main()
