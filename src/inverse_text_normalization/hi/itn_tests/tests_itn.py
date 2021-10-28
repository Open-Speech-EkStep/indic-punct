'''
Please move this file to src/ before running the tests
'''

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text

hindi_digits_with_zero = '0123456789'


class HindiInverseTextNormalization(unittest.TestCase):

    def test_two_digit_numbers_are_converted_to_numerals(self):
        data = ['रीटा के पास सोलह बिल्लियाँ हैं।']
        expected_output = ['रीटा के पास 16 बिल्लियाँ हैं।']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')
        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_context_based_freezing_freezes_one_and_two(self):
        data = ['एक हज़ार चार सौ बीस',
                'एक',
                'दो',
                'तीन',
                'मुझे दो पानी की बोतल दो',
                'मुझे दो सौ पानी की बोतल दो',
                'मुझे दो रुपये दो']
        expected_output = ['1,420',
                           'एक',
                           'दो',
                           '3',
                           'मुझे दो पानी की बोतल दो',
                           'मुझे 200 पानी की बोतल दो',
                           'मुझे ₹ 2 दो']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')
        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_hundreds_are_converted_to_numerals(self):
        data = ['रीटा के पास चार सौ बीस बिल्लियाँ हैं।']
        expected_output = ['रीटा के पास 420 बिल्लियाँ हैं।']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_thousands_are_converted_to_unformatted_numerals(self):
        # no formatting in indian format for this test
        data = ['एक हज़ार चार सौ बीस', 'बारह हज़ार सात सौ तीन', 'पंद्रह सौ', 'पंद्रह सौ सात', 'पंद्रह सौ']
        expected_output = ['1,420', '12,703', '1,500', '1,507', '1,500']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    # def test_lakhs_are_converted_to_unformatted_numerals(self):
    #     # no formatting in indian format for this test
    #     # TODO: 'दो लाख पंद्रह सौ'
    #     data = ['दो लाख', 'दो लाख चार सौ', 'चार लाख चार सौ चार', 'बारह लाख बीस हज़ार सात सौ पंद्रह']
    #     expected_output = ['200000', '200400', '400404', '1220715']
    #
    #     inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')
    #
    #     inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]
    #
    #     self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_thousands_and_lakhs_are_converted_to_formatted_numerals(self):
        data = ['एक हज़ार चार सौ बीस', 'बारह हज़ार सात सौ तीन', 'चार लाख चार सौ चार',
                'बारह लाख बीस हज़ार सात सौ पंद्रह']
        expected_output = ['1,420', '12,703', '4,00,404', '12,20,715']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_single_and_double_digit_crores_are_converted_to_formatted_numerals(self):
        data = ['चार करोड़ इक्कीस लाख', 'चार करोड़ इक्कीस लाख चार हज़ार चार सौ चार',
                'बत्तीस करोड़ इक्कीस लाख सैंतीस हज़ार चार सौ बारह', 'बत्तीस करोड़ चार सौ']
        expected_output = ['4,21,00,000', '4,21,04,404', '32,21,37,412', '32,00,00,400']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_spoken_form_of_single_digit_thousands_for_years_are_converted(self):
        # TODO: don't format (comma) for years
        data = ['वर्ष उन्निस सौ चौहत्तर', 'लेखों की संख्या एक हज़ार नौ सौ चौहत्तर हैं।']
        expected_output = ['वर्ष 1,974', 'लेखों की संख्या 1,974 हैं।']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_variations_of_hundreds_and_thousands_of_crores_or_lakhs_are_converted(self):
        data = ['चार हज़ार चार सौ करोड़', 'दो सौ करोड़', 'चौबीस हज़ार करोड़', 'चार हज़ार चार सौ लाख']
        expected_output = ['44,00,00,00,000', '2,00,00,00,000', '2,40,00,00,00,000', '44,00,00,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_spoken_variations_of_hundreds_and_thousands_of_crores_or_lakhs_are_converted(self):
        data = ['उन्निस सौ उन्निस करोड़', 'सत्ताईस सौ करोड़', 'छत्तीस सौ लाख']
        expected_output = ['19,19,00,00,000', '27,00,00,00,000', '36,00,00,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_simple_lakhs_of_crores_are_converted(self):
        data = ['चार लाख करोड़़']
        expected_output = ['4,00,000 करोड़़']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_number_after_decimals_are_not_formatted_with_commas(self):
        data = ['शून्य दशमलव शून्य आठ चार पाँच']
        expected_output = ['0.0845']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_numbers_with_decimal_parts_are_converted_to_formatted_numerals(self):
        data = ['उसे एक सौ एक दशमलव तीन आठ शून्य बुखार है', 'चार करोड़ इक्कीस लाख दशमलव शून्य आठ']
        expected_output = ['उसे 101.380 बुखार है', '4,21,00,000.08']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_spoken_words_like_only_crore_lakh_and_thousand_are_converted_to_corresponding_numerals(self):
        data = ['उसे हज़ार देदो', 'उसे करोड़ देदो', 'उसे लाख देदो', 'सौ']
        expected_output = ['उसे 1,000 देदो', 'उसे 1,00,00,000 देदो', 'उसे 1,00,000 देदो', '100']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_money_is_converted_to_corresponding_numerals(self):
        data = ['उसे एक हज़ार डॉलर देदो', 'उसे एक हज़ार चार सौ बीस रुपये देदो']
        expected_output = ['उसे $ 1,000 देदो', 'उसे ₹ 1,420 देदो']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='hi')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)


if __name__ == '__main__':
    unittest.main()
