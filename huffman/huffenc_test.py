__author__ = 'martin'

import unittest
from huffenc import encode_file, decode_file


class MyTestCase(unittest.TestCase):
    def test_huffman_encoder(self):
        import hashlib
        encode_file('testing/test_file.txt', 'testing/test_file.hc')
        decode_file('testing/test_file.hc', 'testing/test_file_decoded.txt')

        f1 = open('testing/test_file.txt', 'rb')
        a = hashlib.sha1(f1.read()).hexdigest()
        f1.close()

        f2 = open('testing/test_file_decoded.txt', 'rb')
        b = hashlib.sha1(f2.read()).hexdigest()
        f2.close()

        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
