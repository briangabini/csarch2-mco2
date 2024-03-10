# main_test.py

import unittest
from ..main import Binary128Converter

class TestBinary128Converter(unittest.TestCase):
    def setUp(self):
        self.converter = Binary128Converter()

    """ def test_convert_decimal_to_binary128(self):
        self.converter.convert_decimal_to_binary128(5.25, 0)
        self.assertEqual(self.converter.get_binary128(), '0 10000000000000 0101000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(self.converter.get_hexadecimal(), '0x400A0000000000000000000000000000') """

    def test_convert_fraction_to_binary(self):
        result = self.converter.convert_fraction_to_binary(0.25)
        self.assertEqual(result, '01')

    def test_convert_binary_mantissa_to_binary128(self):
        self.converter.convert_binary_mantissa_to_binary128('101.01', 25)
        self.assertEqual(self.converter.get_binary128(), '0 100000000011010 0101000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(self.converter.get_hexadecimal(), '0X401A5000000000000000000000000000')

    def test_normalize_binary_floating_point_that_needs_left_shift(self):
        normalized_mantissa, base_2_exponent = self.converter.normalize_binary_floating_point('101.01', 25)
        self.assertEqual(normalized_mantissa, '1.0101')
        self.assertEqual(base_2_exponent, 27)
        
    def test_normalize_binary_floating_point_that_needs_right_shift(self):
        normalized_mantissa, base_2_exponent = self.converter.normalize_binary_floating_point('0.0101', 25)
        self.assertEqual(normalized_mantissa, '1.01')
        self.assertEqual(base_2_exponent, 23)

if __name__ == '__main__':
    unittest.main()