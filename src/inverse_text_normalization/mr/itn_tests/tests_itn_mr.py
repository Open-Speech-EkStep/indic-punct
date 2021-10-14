'''
Please move this file to src/ before running the tests
'''

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class MarathiInverseTextNormalization(unittest.TestCase):

    def test_two_digit_numbers_are_converted_to_numerals(self):
        data = ['रीटाला सोळा मांजरी आहेत']
        expected_output = ['रीटाला 16 मांजरी आहेत']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')
        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_hundreds_are_converted_to_numerals_with_correct_grammar_only(self):
        data = [
            'चार शंभर',
            'शंभर',
            'शे',
            'चारशे'

        ]
        expected_output = [
            '4 100',  # we want चारशे for 400. 'चार शंभर' is incorrect usage
            '100',  # शंभर implies 100
            'शे',  # शे in itself doesn't imply 100. It has to come with a number
            '400'  # correct usage

        ]

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_hundreds_are_converted_to_numerals(self):
        data = [
            'रीटाकडे नऊशे वीस मांजरी आहेत',
            'दोनशे एकोणीस',
            'दोन शे एकोणीस'  # space between two and hundred
        ]
        expected_output = [
            'रीटाकडे 920 मांजरी आहेत',
            '219',
            '219'
        ]

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_thousands_are_converted_to_numerals(self):
        data = ['एक हजार चारशे वीस', 'बारा हजार सातशे तीन', 'पंधराशे', 'पंधराशे सात',
                'पंधरा शे सात',
                'अठरा हजार तीनशे नव्व्याण्णव']
        expected_output = ['1,420', '12,703', '1,500', '1,507', '1,507', '18,399']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_lakhs_are_converted_to_formatted_numerals(self):
        data = ['चार लाख चारशे चार',
                'चार लक्ष चारशे चार',  # alternate spelling
                'बारा लाख वीस हजार सातशे पंधरा',
                'बारा लाख वीस हज़ार सातशे पंधरा']  # alternate spelling
        expected_output = ['4,00,404',
                           '4,00,404',
                           '12,20,715',
                           '12,20,715']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_single_and_double_digit_crores_are_converted_to_formatted_numerals(self):
        data = ['चार कोटी',
                'एकवीस लाख',
                'चार कोटी एकवीस लाख', 'चार कोटी एकवीस लाख चार हजार चारशे चार',
                'बत्तीस कोटी एकवीस लाख सदतीस हजार चारशे बारा', 'बत्तीस कोटी दोनशे']
        expected_output = ['4,00,00,000', '21,00,000',
                           '4,21,00,000', '4,21,04,404', '32,21,37,412', '32,00,00,200']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_spoken_form_of_single_digit_thousands_for_years_are_converted(self):
        # TODO: don't format (comma) for years
        data = ['वर्ष एकोणीसशे चौर्‍याहत्तर', 'वर्ष एकोणीसशे चौहत्तर', 'एक हजार नऊशे चौहत्तर लेख आहेत']
        expected_output = ['वर्ष 1,974', 'वर्ष 1,974', '1,974 लेख आहेत']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_variations_of_hundreds_and_thousands_of_crores_or_lakhs_are_converted(self):
        data = ['चार हजार चारशे कोटी', 'दोनशे कोटी', 'चोवीस हजार कोटी', 'चार हजार चारशे लाख']
        expected_output = ['44,00,00,00,000', '2,00,00,00,000', '2,40,00,00,00,000', '44,00,00,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_spoken_variations_of_hundreds_and_thousands_of_crores_or_lakhs_are_converted(self):
        data = ['एकोणीसशे एकोणीस कोटी', 'सत्तावीसशे कोटी', 'छत्तीसशे लाख']
        expected_output = ['19,19,00,00,000', '27,00,00,00,000', '36,00,00,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_simple_lakhs_of_crores_are_converted(self):
        data = ['चार लाख कोटी']
        expected_output = ['40,00,00,00,00,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_number_after_decimals_are_not_formatted_with_commas(self):
        data = ['एकोणतीस दशांश चार तीन', 'शून्य दशांश नऊ तीन चार पाच']
        expected_output = ['29.43', '0.9345']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_spoken_words_like_only_crore_lakh_and_thousand_are_converted_to_corresponding_numerals(self):
        data = ['त्याला हजार द्या', 'त्याला कोटी द्या', 'त्याला लाख द्या', 'शंभर']
        expected_output = ['त्याला 1,000 द्या', 'त्याला 1,00,00,000 द्या', 'त्याला 1,00,000 द्या', '100']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_money_is_converted_to_corresponding_numerals(self):
        data = ['त्याला एक हजार रुपये द्या', 'त्याला एक हजार चारशे एकोणतीस डॉलर द्या']
        expected_output = ['त्याला ₹ 1,000 द्या', 'त्याला $ 1,429 द्या']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='mr')

        inverse_normalizer_prediction = [sent.replace('\r', '') for sent in inverse_normalizer_prediction]

        self.assertEqual(expected_output, inverse_normalizer_prediction)


if __name__ == '__main__':
    unittest.main()
