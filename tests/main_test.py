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

    def test_convert_border_positive_infinity_binary_mantissa_to_binary_128(self):
        self.converter.convert_binary_mantissa_to_binary128('0.0000101', 16388)
        self.assertEqual(self.converter.get_binary128(),
                         '0 111111111111110 0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(self.converter.get_hexadecimal(), '0X7FFE4000000000000000000000000000')

    def test_convert_positive_infinity_binary_mantissa_to_binary_128(self):
        self.converter.convert_binary_mantissa_to_binary128('0.000101', 16388)
        self.assertEqual(self.converter.get_binary128(),
                         '0 111111111111111 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(self.converter.get_hexadecimal(), '0X7FFF0000000000000000000000000000')

    def test_convert_border_negative_infinity_binary_mantissa_to_binary_128(self):
        self.converter.convert_binary_mantissa_to_binary128('-0.0000101', 16388)
        self.assertEqual(self.converter.get_binary128(),
                         '1 111111111111110 0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(self.converter.get_hexadecimal(), '0XFFFE4000000000000000000000000000')

    def test_convert_negative_infinity_binary_mantissa_to_binary_128(self):
        self.converter.convert_binary_mantissa_to_binary128('-0.000101', 16388)
        self.assertEqual(self.converter.get_binary128(),
                         '1 111111111111111 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(self.converter.get_hexadecimal(), '0XFFFF0000000000000000000000000000')

    def test_convert_border_positive_denorm_binary_mantissa_to_binary_128(self):
        self.converter.convert_binary_mantissa_to_binary128('1011000.0', -16388)
        self.assertEqual(self.converter.get_binary128(),
                         '0 000000000000001 0110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(self.converter.get_hexadecimal(), '0X16000000000000000000000000000')

    def test_convert_positive_denorm_binary_mantissa_to_binary_128(self):
        self.converter.convert_binary_mantissa_to_binary128('101100.0', -16388)
        sign_and_exp = self.converter.get_binary128()[:17]
        mantisa = self.converter.get_binary128()[18:]
        self.assertEqual(sign_and_exp,
                         '0 000000000000000')
        self.assertNotEqual(mantisa, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(len(mantisa), 112)

    def test_convert_border_negative_denorm_binary_mantissa_to_binary_128(self):
        self.converter.convert_binary_mantissa_to_binary128('-1011000.0', -16388)
        self.assertEqual(self.converter.get_binary128(),
                         '1 000000000000001 0110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(self.converter.get_hexadecimal(), '0X80016000000000000000000000000000')

    def test_convert_negative_denorm_binary_mantissa_to_binary_128(self):
        self.converter.convert_binary_mantissa_to_binary128('-101100.0', -16388)
        sign_and_exp = self.converter.get_binary128()[:17]
        mantisa = self.converter.get_binary128()[18:]
        self.assertEqual(sign_and_exp,
                         '1 000000000000000')
        self.assertNotEqual(mantisa, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(len(mantisa), 112)

    def test_convert_super_negative_denorm_binary_mantissa_to_binary_128(self):
        self.converter.convert_binary_mantissa_to_binary128('-1.0', -180000)
        sign_and_exp = self.converter.get_binary128()[:17]
        mantisa = self.converter.get_binary128()[18:]
        self.assertEqual(sign_and_exp,
                         '1 000000000000000')
        self.assertNotEqual(mantisa, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.assertEqual(len(mantisa), 112)

    def test_normalize_binary_floating_point_that_needs_left_shift(self):
        normalized_mantissa, base_2_exponent = self.converter.normalize_binary_floating_point('101.01', 25)
        self.assertEqual(normalized_mantissa, '1.0101')
        self.assertEqual(base_2_exponent, 27)
        
    def test_normalize_binary_floating_point_that_needs_right_shift(self):
        normalized_mantissa, base_2_exponent = self.converter.normalize_binary_floating_point('0.0101', 25)
        self.assertEqual(normalized_mantissa, '1.01')
        self.assertEqual(base_2_exponent, 23)

    def test_normalize_border_binary_floating_no_shift(self):
        normalized_mantissa, base_2_exponent = self.converter.normalize_binary_floating_point('1.0', 16383)
        self.assertEqual(normalized_mantissa, '1.0')
        self.assertEqual(base_2_exponent, 16383)

    def test_positive_infinity_binary_floating(self):
        normalized_mantissa, base_2_exponent = self.converter.normalize_binary_floating_point('1.0', 16384)
        self.assertEqual(normalized_mantissa, '1.0')
        self.assertEqual(base_2_exponent, 16384)

    def test_negative_infinity_binary_floating(self):
        normalized_mantissa, base_2_exponent = self.converter.normalize_binary_floating_point('1.0', -16384)
        self.assertEqual(normalized_mantissa, '1.0')
        self.assertEqual(base_2_exponent, -16384)

    def test_positive_border_infinity_binary_floating_shift_right(self):
        normalized_mantissa, base_2_exponent = self.converter.normalize_binary_floating_point('0.0000101', 16388)
        self.assertEqual(normalized_mantissa, '1.01')
        self.assertEqual(base_2_exponent, 16383)

    def test_negative_border_infinity_binary_floating_shift_left(self):
        normalized_mantissa, base_2_exponent = self.converter.normalize_binary_floating_point('101100.0', -16388)
        self.assertEqual(normalized_mantissa, '1.011000')
        self.assertEqual(base_2_exponent, -16383)

if __name__ == '__main__':
    unittest.main()