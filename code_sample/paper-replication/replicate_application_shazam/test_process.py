import unittest
from process import WaveClass


class TestStringMethods(unittest.TestCase):
    def test_WaveClass(self):
        # test file is a wav. that is about 12.03s long
        wv_test = WaveClass("MUSIC_test/test_12s.wav")
        rate_test, nframes_test, array_test, time_test = wv_test.readwav()
        window_list_test = wv_test.spectral(length_of_window=10)
        spec_test = wv_test.specgram(wv_test.array[0])
        peak_test = wv_test.get_peak(window_list_test[0], N=5)

        trans_data_test = wv_test.prepare_dataset(window_list_test, N=5, Method='peak')
        trans_data_test2 = wv_test.prepare_dataset(window_list_test, N=5, Method='scaled_frequencies')

        # test readwav()
        self.assertEqual(rate_test, 44100)
        self.assertTrue(nframes_test/rate_test > 12)
        self.assertTrue(array_test[0].size == nframes_test)
        self.assertEqual(len(array_test), 2)

        # test spectral()
        self.assertEqual(len(window_list_test), 3)
        self.assertEqual(window_list_test[2].size, 44100*10)

        # test specgram()
        self.assertEqual(len(spec_test), 3)
        self.assertEqual(spec_test[0].size, 271338)

        # test
        self.assertEqual(len(peak_test), 5)


if __name__ == '__main__':
    unittest.main()


