'''
Please move this file to src/ before running the tests
'''

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class BengaliInverseTextNormalization(unittest.TestCase):

    def test_single_digit_numbers_are_converted_to_numerals(self):
        data = ['চার', 'আট', 'পাঁচ কলম', 'আমার নয়টি কলম আছে']
        expected_output = ['4', '8', '5 কলম', 'আমার 9 কলম আছে']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='bn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_double_digit_numbers_are_converted_to_numerals(self):
        data = ['ছাব্বিশ', 'একষট্টি গরু', 'বিশটি শিশু সুখী', 'বিশ কলম', 'আমার কাছে আটচল্লিশ চেয়ার আছে']
        expected_output = ['26', '61 গরু', '20 শিশু সুখী', '20 কলম', 'আমার কাছে 48 চেয়ার আছে']
        inverse_normalizer_prediction = inverse_normalize_text(data, lang='bn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_hundreds_are_converted_to_numerals(self):
        data = ['শত', 'একশত', 'দুইশত', 'তিনশ এগারো', 'সাতশ চুয়ান্ন']
        expected_output = ['100', '100', '200', '311', '754']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='bn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_tens_of_hundreds_are_converted_to_numerals(self):
        data = ['চৌদ্দশত লোক',
                'রিতার জন্ম ঊনিশ শত নব্বই সালে']
        expected_output = ['1400 লোক',
                           'রিতার জন্ম 1990 সালে']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='bn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_thousands_are_converted_to_numerals(self):
        data = ['হাজার', 'এক হাজার', 'চব্বিশ হাজার তিনশত পঞ্চান্ন', 'তিনি আট হাজার পাঁচশ পর্যন্ত গুনতে পারেন',
                'জাদুকর ছয় হাজার সাতশ একত্রিশ কৌশল জানতেন']
        expected_output = ['1000', '1000', '24,355', 'তিনি 8500 পর্যন্ত গুনতে পারেন',
                           'জাদুকর 6731 কৌশল জানতেন']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='bn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_lakhs_are_converted_to_numerals(self):
        data = ['এক লাখ', 'লাখ', 'পাঁচ লাখ বিয়াল্লিশ হাজার', 'নয় লাখ', 'স্টেডিয়ামে ছিল ছয় লাখ সত্তর হাজার মানুষ',
                'পঞ্চান্ন লাখ আটষট্টি হাজার চারশত সতের']
        expected_output = ['1,00,000', '1,00,000', '5,42,000', '9,00,000', 'স্টেডিয়ামে ছিল 6,70,000 মানুষ',
                           '55,68,417']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='bn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_crores_are_converted_to_numerals(self):
        data = ['এক কোটি', 'কোটি', 'তিন কোটি', 'নিরানব্বইটি কোটি পাঁচ লাখ তিনশ বাইশ']

        expected_output = ['1,00,00,000',
                           '1,00,00,000',
                           '3,00,00,000',
                           '99,05,00,322']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='bn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_money_is_converted_to_corresponding_numerals(self):
        data = ['আমি তাকে একশত পঞ্চাশ টাকা দিলাম', 'দশ ইউরো', 'সে তার বন্ধুর কাছ থেকে চল্লিশ পাউন্ড ধার নিয়েছিল']

        expected_output = ['আমি তাকে ₹ 150 দিলাম', '€ 10', 'সে তার বন্ধুর কাছ থেকে £ 40 ধার নিয়েছিল']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='bn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)


if __name__ == '__main__':
    unittest.main()
