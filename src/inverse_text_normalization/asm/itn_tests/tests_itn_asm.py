'''
Please move this file to src/ before running the tests
'''

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class AssameseInverseTextNormalization(unittest.TestCase):

    def test_single_digit_numbers_are_converted_to_numerals(self):
        data = ['চাৰি', 'আঠ', 'ছয়টা কলম', 'তাইৰ নখন চকী আছে']
        expected_output = ['4', '8', '6 কলম', 'তাইৰ 9 চকী আছে']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='as')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_double_digit_numbers_are_converted_to_numerals(self):
        data = ['পঁচিছ', 'চৌসত্তৰ', 'মই দহ বাকচ মিঠাই বিতৰণ কৰিলো', 'সাতত্ৰিছ পইণ্ট',
                'অংগীকৰণৰ দ্বাৰা সাতষষ্ঠিটা টা গছ ৰোপণ কৰা হৈছিল']
        expected_output = ['25', '74', 'মই 10 বাকচ মিঠাই বিতৰণ কৰিলো', '37 পইণ্ট',
                           'অংগীকৰণৰ দ্বাৰা 67 টা গছ ৰোপণ কৰা হৈছিল']
        inverse_normalizer_prediction = inverse_normalize_text(data, lang='as')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_hundreds_are_converted_to_numerals(self):
        data = ['এশ', 'এশটা শিশু', 'এশখন চকীৰ প্ৰয়োজন', 'দুশ', 'দুশ আঠষষ্ঠি', 'তিনিশ চৌৰাশী', 'পাঁচশ এসত্তৰ',
                'চাৰিশ এঘাৰ', 'ছয়শ', 'সাতশ', 'আঠশ', 'নশ']
        expected_output = ['100', '100 শিশু', '100 চকীৰ প্ৰয়োজন', '200', '268', '384', '571', '411', '600', '700',
                           '800', '900']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='as')
        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_tens_of_hundreds_are_converted_to_numerals(self):
        data = ['চৌদ্দশ নব্বৈ জন',
                'পঞ্চল্লিছশ ন']
        expected_output = ['1490 জন',
                           '4509']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='as')
        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_thousands_are_converted_to_numerals(self):
        data = ['হাজাৰ', 'এক হাজাৰ', 'এহাজাৰ', 'পাঁচ হাজাৰ সাতশ', 'ষাঠি হাজাৰ দুশ ত্ৰিশ', 'নব্বৈ হাজাৰ আঠশ একাৱন্ন']
        expected_output = ['1000', '1000', '1000', '5700', '60,230', '90,851']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='as')
        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_lakhs_are_converted_to_numerals(self):
        data = ['এক লাখ', 'লাখ', 'দুই লাখ একচল্লিছ হাজাৰ নশ', 'তিৰাশী লাখ তিনিশ ছয়ষষ্ঠি']
        expected_output = ['1,00,000', '1,00,000', '2,41,900', '83,00,366']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='as')
        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_crores_are_converted_to_numerals(self):
        data = ['এক কোটি', 'কোটি', 'সাত কোটি', 'নিৰান্নব্বৈটা কোটি পাঁচ লাখ আঠশ বাইছ']

        expected_output = ['1,00,00,000',
                           '1,00,00,000',
                           '7,00,00,000',
                           '99,05,00,822']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='as')
        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_money_is_converted_to_corresponding_numerals(self):
        data = ['মই পোন্ধৰ টকাত এটা কলম কিনিছিলো', 'দহ ইউৰো', 'তাই তিনিশ ডলাৰ ভাড়া দিয়ে']

        expected_output = ['মই ₹ 15 এটা কলম কিনিছিলো', '€ 10', 'তাই $ 300 ভাড়া দিয়ে']
        inverse_normalizer_prediction = inverse_normalize_text(data, lang='as')
        self.assertEqual(expected_output, inverse_normalizer_prediction)


if __name__ == '__main__':
    unittest.main()
