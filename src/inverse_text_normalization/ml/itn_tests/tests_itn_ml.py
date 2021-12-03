'''
Please move this file to src/ before running the tests
'''

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class MalayalamInverseTextNormalization(unittest.TestCase):

    def test_single_digit_numbers_are_converted_to_numerals(self):
        # data = ['ഒന്ന്', 'അവൾക്ക് അഞ്ച് പേനകൾ ഉണ്ടായിരുന്നു', 'എട്ട്']
        # expected_output = ['1', 'അവൾക്ക് 5 പേനകൾ ഉണ്ടായിരുന്നു', '8']

        data = ['പൂജ്യം','ഒന്ന്','രണ്ട്','മൂന്ന്','നാല്','അഞ്ച്','ആറ്','ഏഴ്','എട്ട്','ഒമ്പത്']
        expected_output = ['0','1','2','3','4','5','6','7','8','9']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_double_digit_numbers_are_converted_to_numerals(self):
        # data = ['അവൾക്ക് പത്ത് മേശകൾ ഉണ്ടായിരുന്നു', 'മുപ്പത്തി എട്ട്', 'തൊണ്ണൂറ്റി ഒന്ന്']
        # expected_output = ['അവൾക്ക് 10 മേശകൾ ഉണ്ടായിരുന്നു', '38', '91']

        data = ['നാല്പത്തൊമ്പത്','അമ്പത്','അമ്പത്തൊന്ന്','അമ്പത്തിരണ്ട്','അമ്പത്തിമൂന്ന്','അമ്പത്തിനാല്','അമ്പത്തഞ്ച്','അമ്പത്തിയാറ്','അമ്പത്തിയേഴ്','അമ്പത്തിയെട്ട്','അമ്പത്തൊമ്പത്','അറുപത്']
        expected_output = ['49','50','51','52','53','54','55','56','57','58','59','60']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_multiples_of_hundreds_are_converted_to_numerals(self):
        '''
        #Todo : handle numbers for 500, 800 and 900
        '''
        data = ['നൂറ്', 'ഇരുനൂറ്', 'മുന്നൂറ്', 'നാനൂറ്', 'അഞ്ഞൂറ്', 'അറുനൂറ്', 'എഴുനൂറ്', 'എണ്ണൂറ്']  # 'തൊള്ളായിരം'
        expected_output = ['100', '200', '300', '400', '500', '600', '700', '800']  # '900'

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_hundreds_are_converted_to_numerals(self):
        # data = ['നൂറ്', 'ഒന്ന് നൂറ്', 'ഇരുനൂറ്റി എഴുപത്തി ഒന്‍പത്', 'മുന്നൂറ്റി അമ്പത്തി ഏഴ്',
        #         'അറുനൂറ്റി ഇരുപത്തി നാല്', 'എഴുനൂറ്റി പതിനൊന്ന്']
        # expected_output = ['100', '100', '279', '357', '624', '711']

        data = ['അഞ്ഞൂറ്റി ഒന്ന്','അഞ്ഞൂറ്റി പത്ത്','അഞ്ഞൂറ്റി ഇരുപത്തഞ്ച്','അഞ്ഞൂറ്റി അമ്പത്','എണ്ണൂറ്റി അഞ്ച്','എണ്ണൂറ്റി അമ്പത്','എണ്ണൂറ്റി തൊണ്ണൂറ്','തൊള്ളായിരം','തൊള്ളായിരത്തി ഒന്ന്',
                'തൊള്ളായിരത്തി പത്ത്','തൊള്ളായിരത്തി അമ്പത്','തൊള്ളായിരത്തി തൊണ്ണൂറ്','തൊള്ളായിരത്തി തൊണ്ണൂറ്റൊന്ന്','തൊള്ളായിരത്തി തൊണ്ണൂറ്റൊമ്പത്','തൊള്ളായിരത്തി പത്തൊമ്പത്',
                'തൊള്ളായിരത്തി അമ്പത്തഞ്ച്']
        expected_output = ['501', '510', '525', '550', '805', '850', '890', '900', '901', '910', '950', '990', '991', '999', '919', '955']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_thousands_are_converted_to_numerals(self):
        # Todo: Handle 1101 - 1199 series.

        data = ['ആയിരം','ആയിരത്തി ഒന്ന്','ആയിരത്തി അമ്പത്','ആയിരത്തി നൂറ്','ആയിരത്തി ഇരുനൂറ്','ആയിരത്തി മുന്നൂറ്റി തൊണ്ണൂറ്', 'ആയിരത്തി അഞ്ഞൂറ്','ആയിരത്തി അഞ്ഞൂറ്റി അമ്പത്','രണ്ടായിരം',
                'രണ്ടായിരത്തി ഒന്ന്','രണ്ടായിരത്തി അഞ്ഞൂറ്','അയ്യായിരം', 'അയ്യായിരത്തി ഒന്ന്','അയ്യായിരത്തി അഞ്ഞൂറ്', 'എണ്ണായിരം','എണ്ണായിരത്തി അമ്പത','നാലായിരം','ആറായിരം','ഏഴായിരം',
                'ആയിരത്തി ഒന്ന് നൂറ്റി പതിനൊന്ന്','അയ്യായിരത്തി ഒന്ന് നൂറ്റി പതിനൊന്ന്']

        expected_output = ['1000','1001','1050','1100','1200','1390','1500','1550','2000','2001','2500','5000','5001', '5500', '8000','8050', '4000','6000',
                            '7000', '1111', '5111']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

'''
    def test_num_with_one_hundred_are_converted_to_numerals(self):
        # Todo: Handle 1101 - 1199 series.

        data = ['ആയിരത്തി നൂറ്റി പതിനൊന്ന്','ആയിരത്തി നൂറ്റി അമ്പത്തൊന്ന്','രണ്ടായിരത്തി നൂറ്റി പതിനൊന്ന്','അയ്യായിരത്തി നൂറ്റി ഇരുപത്തിരണ്ട്']
        expected_output = ['1111', '1151', '2111', '5122']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)
'''

    def test_num_in_range_9000_to_9999_are_converted_to_numerals(self):

        data = ['ഒമ്പതിനായിരം','ഒമ്പതിനായിരത്തി ഒന്ന്','ഒമ്പതിനായിരത്തി അമ്പത്','ഒമ്പതിനായിരത്തി ഇരുനൂറ്','ഒമ്പതിനായിരത്തി അഞ്ഞൂറ്']
        expected_output = ['9000', '9001', '9050', '9200', '9500']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_in_range_10000_to_99999_are_converted_to_numerals(self):

        data = ['പത്ത്ആയിരം','പത്ത്ആയിരത്തി ഒന്ന്','പത്ത്ആയിരത്തി ഇരുനൂറ്റി അമ്പത്','പത്ത്ആയിരത്തി അഞ്ഞൂറ്','പത്ത്ആയിരത്തി തൊള്ളായിരം','പതിനൊന്നായിരം','പതിനൊന്നായിരത്തി ഒന്ന്',
                'പതിനൊന്നായിരത്തി അഞ്ഞൂറ്റി ഒന്ന്','പന്ത്രണ്ടായിരം','പതിമൂന്നായിരം','പതിനാലായിരം','പതിനയ്യായിരം','പതിനാറായിരം','പതിനേഴായിരം','പതിനെട്ടായിരം','പത്തൊമ്പതിനായിരം',
                'ഇരുപത്ആയിരം','ഇരുപത്തൊന്നായിരം','ഇരുപത്തയ്യായിരം', 'തൊണ്ണൂറ്റൊമ്പതിനായിരത്തി തൊള്ളായിരത്തി തൊണ്ണൂറ്റൊമ്പത്','അമ്പത്തൊന്നായിരത്തി ഇരുനൂറ്റി അമ്പത്തഞ്ച്',
                'എഴുപത്തയ്യായിരത്തി എഴുനൂറ്റി അമ്പത്തിയേഴ്','എൺപത്തിയെട്ടായിരത്തി എണ്ണൂറ്റി എൺപത്തിയെട്ട്','ഇരുപത്തയ്യായിരത്തി എഴുനൂറ്റി അറുപത്തഞ്ച്','അമ്പത്തിയേഴായിരത്തി അറുനൂറ്']

        expected_output = ['10,000','10,001','10,250','10,500','10,900','11,000','11,001','11,501','12,000','13,000','14,000','15,000','16,000','17,000',
                           '18,000', '19,000','20,000','21,000','25,000', '99,999', '51,255', '75,757', '88,888', '25,765', '57,600']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_lakhs_are_converted_to_numerals(self):

        data = ['ഒരു ലക്ഷം','രണ്ട് ലക്ഷം','അഞ്ച് ലക്ഷം','എട്ട് ലക്ഷം','ഒമ്പത് ലക്ഷം','ഒരു ലക്ഷത്തി ആയിരം','രണ്ട് ലക്ഷത്തി അഞ്ഞൂറ്','അഞ്ച് ലക്ഷത്തി അമ്പത്',
                'എട്ട് ലക്ഷത്തി എഴുപത്തയ്യായിരത്തി ഇരുനൂറ്റി ഇരുപത്തഞ്ച്','ഒമ്പത് ലക്ഷത്തി ഒന്ന്','തൊണ്ണൂറ്റൊമ്പത് ലക്ഷത്തി തൊണ്ണൂറ്റൊമ്പതിനായിരത്തി തൊള്ളായിരത്തി തൊണ്ണൂറ്റൊമ്പത്',
                'അമ്പത്തഞ്ച് ലക്ഷത്തി അമ്പത്തയ്യായിരത്തി അഞ്ഞൂറ്റി അമ്പത്തഞ്ച്']

        expected_output = ['1,00,000','2,00,000','5,00,000', '8,00,000', '9,00,000', '1,01,000', '2,00,500', '5,00,050', '8,75,225', '9,00,001',
                           '99,99,999', '55,55,555']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_crores_are_converted_to_numerals(self):

        data = ['ഒരു കോടി തൊണ്ണൂറ്റൊമ്പത് ലക്ഷത്തി തൊണ്ണൂറ്റൊമ്പതിനായിരത്തി തൊള്ളായിരത്തി തൊണ്ണൂറ്റൊമ്പത്','ഒരു കോടി അമ്പത്തഞ്ച് ലക്ഷത്തി അമ്പത്തയ്യായിരത്തി അഞ്ഞൂറ്റി അമ്പത്തഞ്ച്','ഒമ്പത് കോടി',
                'അഞ്ച് കോടി അമ്പത് ലക്ഷം','രണ്ട് കോടി അഞ്ച് ലക്ഷം','ഇരുപത്തഞ്ച് കോടി']

        expected_output = ['1,99,99,999', '1,55,55,555', '9,00,00,000', '5,50,00,000', '2,05,00,000', '25,00,00,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_money_is_converted_to_corresponding_numerals(self):
        data = ['ഇരുനൂറ്റി അമ്പത് രൂപ ഞാൻ അവന് കൊടുത്തു', 'അവൻ എനിക്ക് പത്ത് യൂറോ തന്നു', 'ഇയാളുടെ വാലറ്റിൽ തൊള്ളായിരം രൂപ', 'എന്റെ കയ്യിൽ അഞ്ഞൂറ് ഡോളർ ഉണ്ട്',
                'അമ്പത്തഞ്ച് ലക്ഷത്തി അമ്പത്തയ്യായിരത്തി അഞ്ഞൂറ്റി അമ്പത്തഞ്ച് രൂപ ഞാൻ അവന് കൊടുത്തു', 'എന്റെ കയ്യിൽ ഏഴായിരത്തി അഞ്ഞൂറ് പൗണ്ട് സ്റ്റെർലിംഗ് ഉണ്ട്']

        expected_output = ['₹ 250 ഞാൻ അവന് കൊടുത്തു', 'അവൻ എനിക്ക് € 10 തന്നു', 'ഇയാളുടെ വാലറ്റിൽ ₹ 900', 'എന്റെ കയ്യിൽ $ 500 ഉണ്ട്', '₹ 55,55,555 ഞാൻ അവന് കൊടുത്തു',
                           'എന്റെ കയ്യിൽ £ 7500 ഉണ്ട്']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ml')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

if __name__ == '__main__':
    unittest.main()
















