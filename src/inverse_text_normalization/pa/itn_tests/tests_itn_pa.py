'''
Please move this file to src/ before running the tests

Referred sources for 11-99 include :
https://en.wikibooks.org/wiki/Punjabi/Numbers
https://omniglot.com/language/numbers/punjabi.htm
https://www.2indya.com/punjabi-numbers/
'''

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class PunjabiInverseTextNormalization(unittest.TestCase):
    def test_single_digit_number_converted_to_numerals(self):
        data = ['ਮੇਰੇ ਕੋਲ ਚਾਰ ਬੈਗ ਹਨ', 'ਰੀਟਾ ਅਗਲੇ ਮਹੀਨੇ ਅੱਠ ਸ਼ਹਿਰਾਂ ਵਿੱਚ ਜਾਵੇਗੀ', 'ਦੋ']
        expected_output = ['ਮੇਰੇ ਕੋਲ 4 ਬੈਗ ਹਨ', 'ਰੀਟਾ ਅਗਲੇ ਮਹੀਨੇ 8 ਸ਼ਹਿਰਾਂ ਵਿੱਚ ਜਾਵੇਗੀ', '2']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='pa')
        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_two_digit_numbers_are_converted_to_numerals(self):
        data = ['ਰੀਟਾ ਦੇ ਕੋਲ ਉਨੀ ਪੈੱਨ ਹਨ',  # Rita has 19 pens
                'ਮੇਰੇ ਕੋਲ ਚਾਲੀ ਗਲਾਸ ਹਨ',  # 40
                'ਸਤਾਸੀ']

        expected_output = ['ਰੀਟਾ ਦੇ ਕੋਲ 19 ਪੈੱਨ ਹਨ',
                           'ਮੇਰੇ ਕੋਲ 40 ਗਲਾਸ ਹਨ',
                           '87']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='pa')
        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_hundreds_are_converted_to_numerals(self):
        data = ['ਬਾਜ਼ਾਰ ਵਿੱਚ ਸੌ ਦੁਕਾਨਾਂ ਹਨ',
                'ਬਾਗ ਵਿੱਚ ਸੱਤ ਸੌ ਬਾਰਾਂ ਫੁੱਲ ਹਨ',
                'ਨੌ ਸੌ ਬਿਆਸੀ'
                ]
        expected_output = ['ਬਾਜ਼ਾਰ ਵਿੱਚ 100 ਦੁਕਾਨਾਂ ਹਨ',
                           'ਬਾਗ ਵਿੱਚ 712 ਫੁੱਲ ਹਨ',
                           '982'
                           ]

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='pa')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_thousands_are_converted_to_numerals(self):
        data = ['ਉਸ ਕੋਲ ਪੰਦਰਾਂ ਸੌ ਕਾਰਾਂ ਹਨ',
                'ਸੱਤਰ ਸੌ ਛੱਤੀ',
                'ਇੱਕ ਹਜਾਰ ਚਾਰ ਸੌ ਵੀਹ',
                'ਬਾਰਾਂ ਹਜਾਰ ਸੱਤ ਸੌ ਤਿੰਨ',
                'ਇੱਕ ਹਜ਼ਾਰ ਚਾਰ ਸੌ ਵੀਹ']
        expected_output = ['ਉਸ ਕੋਲ 1,500 ਕਾਰਾਂ ਹਨ',
                           '7,036',
                           '1,420',
                           '12,703',
                           '1,420']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='pa')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_lakhs_are_converted_to_numerals(self):
        data = ['ਦੋ ਲੱਖ', 'ਦੋ ਲੱਖ ਸੱਤ ਸੌ', 'ਚਾਰ ਲੱਖ ਚਾਰ ਸੌ ਚਾਰ',
                'ਬਾਰਾਂ ਲੱਖ ਵੀਹ ਹਜਾਰ ਸੱਤ ਸੌ ਪੰਦਰਾਂ']
        expected_output = ['2,00,000', '2,00,700', '4,00,404', '12,20,715']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='pa')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_single_and_double_digit_crores_are_converted_to_formatted_numerals(self):
        data = ['ਚਾਰ ਕਰੋੜ ਇੱਕੀ ਲੱਖ', 'ਚਾਰ ਕਰੋੜ ਇੱਕੀ ਲੱਖ ਚਾਰ ਹਜਾਰ ਛੇ ਸੌ ਸੱਤ']
        expected_output = ['4,21,00,000', '4,21,04,607']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='pa')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_spoken_form_of_single_digit_thousands_for_years_are_converted(self):
        # TODO: don't format (comma) for years
        data = ['ਸਾਲ ਉਨੀ ਸੌ ਚੌਹੱਤਰ', 'ਲੇਖਾਂ ਦੀ ਗਿਣਤੀ ਇੱਕ ਹਜਾਰ ਨੌ ਸੌ ਚੌਹੱਤਰ ਹੈ', 'ਇਕਵਿੰਜਾ ਸੌ ਬਾਈ']
        expected_output = ['ਸਾਲ 1,974', 'ਲੇਖਾਂ ਦੀ ਗਿਣਤੀ 1,974 ਹੈ', '5,122']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='pa')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_money_is_converted_to_corresponding_numerals(self):
        data = ['ਉਸਨੂੰ ਤਿੰਨ ਹਜਾਰ ਡਾਲਰ ਦਿਓ', 'ਉਸਨੂੰ ਦੋ ਸੌ ਯੂਰੋ ਦਿਓ', 'ਮੇਰੇ ਕੋਲ ਦਸ ਰੁਪਏ ਹਨ']
        expected_output = ['ਉਸਨੂੰ $ 3,000 ਦਿਓ', 'ਉਸਨੂੰ € 200 ਦਿਓ', 'ਮੇਰੇ ਕੋਲ ₹ 10 ਹਨ']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='pa')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)


if __name__ == '__main__':
    unittest.main()