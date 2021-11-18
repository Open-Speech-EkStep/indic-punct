'''
Please move this file to src/ before running the tests
'''

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class MalayalamInverseTextNormalization(unittest.TestCase):

    def test_single_digit_numbers_are_converted_to_numerals(self):
        data = ['ഒന്ന്', 'അവൾക്ക് അഞ്ച് പേനകൾ ഉണ്ടായിരുന്നു', 'എട്ട്']
        expected_output = ['1', 'അവൾക്ക് 5 പേനകൾ ഉണ്ടായിരുന്നു', '8']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_double_digit_numbers_are_converted_to_numerals(self):
        data = ['അവൾക്ക് പത്ത് മേശകൾ ഉണ്ടായിരുന്നു', 'മുപ്പത്തി എട്ട്', 'തൊണ്ണൂറ്റി ഒന്ന്']
        expected_output = ['അവൾക്ക് 10 മേശകൾ ഉണ്ടായിരുന്നു', '38', '91']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_multiples_of_hundreds_are_converted_to_numerals(self):
        '''
        #Todo : handle numbers for 500, 600, 800 and 900
        '''
        data = ['ഇരുന്നൂറ്', 'മുന്നൂറ്', 'നാനൂറ്', 'അറുനൂറു', 'എഴുനൂറ്']  # 'അഞ്ഞൂറ്','എണ്ണൂറ്', 'തൊള്ളായിരം']
        expected_output = ['200', '300', '400', '600', '700']  # '500','800','900']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_hundreds_are_converted_to_numerals(self):
        data = ['നൂറ്', 'ഒന്ന് നൂറ്', 'ഇരുനൂറ്റി എഴുപത്തി ഒന്‍പത്', 'മുന്നൂറ്റി അമ്പത്തി ഏഴ്',
                'അറുനൂറ്റി ഇരുപത്തി നാല്', 'എഴുനൂറ്റി പതിനൊന്ന്']
        expected_output = ['100', '100', '279', '357', '624', '711']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)


if __name__ == '__main__':
    unittest.main()
