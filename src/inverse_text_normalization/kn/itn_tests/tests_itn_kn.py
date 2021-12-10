"""
Please move this file to src/ before running the tests
"""

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class KannadaInverseTextNormalization(unittest.TestCase):

    def test_single_digit_numbers_are_converted_to_numerals(self):
        data = ['ಸೊನ್ನೆ', 'ಒಂದು', 'ಎರಡು', 'ಮೂರು', 'ನಾಲ್ಕು', 'ಐದು', 'ಆರು', 'ಏಳು', 'ಎಂಟು', 'ಒಂಬತ್ತು']
        expected_output = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='kn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_double_digit_numbers_are_converted_to_numerals(self):
        data = ['ಹತ್ತು', 'ಇಪ್ಪತ್ತು', 'ಮೂವತ್ತು', 'ನಲವತ್ತು', 'ಐವತ್ತು', 'ಅರವತ್ತು', 'ಎಪ್ಪತ್ತು', 'ಎಂಬತ್ತು', 'ತೊಂಬತ್ತು',
                'ಮೂವತ್ತೈದು']
        expected_output = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '35']

        # data = ['ಹನ್ನೊಂದು','ಇಪ್ಪತ್ತೆರಡು','ಮುವತ್ತ ಮೂರು','ನಲವತ್ತು ನಾಲ್ಕು','ಐವತ್ತೈದು','ಅರವತ್ತಾರು','ಎಪ್ಪತ್ತೇಳು','ಎಂಬತ್ತೆಂಟು','ತೊಂಬತ್ತೊಂಬತ್ತು']
        # expected_output = ['11','22','33','44','55','66','77','88','99']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='kn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_multiples_of_hundreds_are_converted_to_numerals(self):
        # data = ['ನೂರು','ಎರಡು ನೂರು','ಮೂರು ನೂರು','ನಾಲ್ಕು ನೂರು','ಐದು ನೂರು','ಆರು ನೂರು','ಏಳು ನೂರು','ಎಂಟು ನೂರು','ಒಂಬತ್ತು ನೂರು']
        # expected_output = ['100', '200', '300', '400', '500', '600', '700', '800', '900']

        # data = ['ಒಂದು ನೂರ ಹತ್ತು','ಎರಡು ನೂರ ಇಪ್ಪತ್ತು','ಮೂರು ನೂರ ಮೂವತ್ತು','ನಾಲ್ಕು ನೂರ ನಲವತ್ತು','ಐದು ನೂರ ಐವತ್ತು','ಆರು ನೂರ ಅರವತ್ತು',
        #         'ಏಳು ನೂರ ಎಪ್ಪತ್ತು','ಎಂಟು ನೂರ ಎಂಬತ್ತು','ಒಂಬತ್ತು ನೂರ ತೊಂಬತ್ತು']
        # expected_output = ['110','220','330','440','550','660','770','880','990']

        data = ['ಒಂದು ನೂರ ಮೂರು', 'ಎರಡು ನೂರ ಆರು', 'ಮೂರು ನೂರ ಒಂಬತ್ತು', 'ನಾಲ್ಕು ನೂರ ಹನ್ನೆರಡು', 'ಐದು ನೂರ ಹದಿನೈದು',
                'ಆರು ನೂರ ಹದಿನೆಂಟು', 'ಒಂದು ನೂರ ಹನ್ನೊಂದು', 'ಐದು ನೂರ ಐವತ್ತೈದು', 'ಆರು ನೂರ ಅರವತ್ತಾರು',
                'ಏಳು ನೂರ ಎಪ್ಪತ್ತೇಳು', 'ಎಂಟು ನೂರ ಎಂಬತ್ತೆಂಟು', 'ಒಂಬತ್ತು ನೂರ ತೊಂಬತ್ತೊಂಬತ್ತು']

        expected_output = ['103', '206', '309', '412', '515', '618', '111', '555', '666', '777', '888', '999']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='kn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_simple_thousand_series_numbers_are_converted_to_numerals(self):
        data = ['ಒಂದು ಸಾವಿರ', 'ಎರಡು ಸಾವಿರ', 'ಮೂರು ಸಾವಿರ', 'ನಾಲ್ಕು ಸಾವಿರ', 'ಐದು ಸಾವಿರ', 'ಆರು ಸಾವಿರ', 'ಏಳು ಸಾವಿರ',
                'ಎಂಟು ಸಾವಿರ', 'ಒಂಬತ್ತು ಸಾವಿರ']

        expected_output = ['1000', '2000', '3000', '4000', '5000', '6000', '7000', '8000', '9000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='kn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_thousand_are_converted_to_numerals(self):
        data = ['ಹನ್ನೆರಡು ಸಾವಿರದ ಎರಡು ನೂರ ಅರವತ್ತೈದು', 'ಹದಿಮೂರು ಸಾವಿರದ ಮೂರು ನೂರ ಎಂಬತ್ತು',
                'ಹದಿನಾಲ್ಕು ಸಾವಿರದ ನಾಲ್ಕು ನೂರ ತೊಂಬತ್ತೈದು',
                'ಹದಿನೈದು ಸಾವಿರದ ಆರು ನೂರ ಹತ್ತು', 'ಹದಿನೇಳು ಸಾವಿರದ ಎಂಟು ನೂರ ನಲವತ್ತು',
                'ಹದಿನೆಂಟು ಸಾವಿರದ ಒಂಬತ್ತು ನೂರ ಐವತ್ತೈದು',
                'ಇಪ್ಪತ್ತು ಸಾವಿರದ ಎಪ್ಪತ್ತು', 'ನಲವತ್ತೆಂಟು ಸಾವಿರ', 'ಐವತ್ತು ಸಾವಿರದ ನಾಲ್ಕು ನೂರು',
                'ಐವತ್ತೆರಡು ಸಾವಿರದ ಎಂಟು ನೂರು', 'ಐವತ್ತೈದು ಸಾವಿರದ ಎರಡು ನೂರು',
                'ಐವತ್ತೇಳು ಸಾವಿರದ ಆರು ನೂರು', 'ಅರವತ್ತು ಸಾವಿರ', 'ಅರವತ್ತೆರಡು ಸಾವಿರದ ನಾಲ್ಕು ನೂರು',
                'ಅರವತ್ತೇಳು ಸಾವಿರದ ಎರಡು ನೂರು',
                'ಅರವತ್ತೊಂಬತ್ತು ಸಾವಿರದ ಆರು ನೂರು', 'ಎಪ್ಪತ್ತೆರಡು ಸಾವಿರ',
                'ತೊಂಬತ್ತೊಂಬತ್ತು ಸಾವಿರದ ಒಂಬತ್ತು ನೂರ ತೊಂಬತ್ತೊಂಬತ್ತು']

        expected_output = ['12,265', '13,380', '14,495', '15,610', '17,840', '18,955', '20,070', '48,000', '50,400',
                           '52,800', '55,200', '57,600', '60,000', '62,400', '67,200', '69,600', '72,000', '99,999']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='kn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_lakhs_are_converted_to_numerals(self):
        data = ['ಒಂದು ಲಕ್ಷ', 'ಎರಡು ಲಕ್ಷ', 'ನಾಲ್ಕು ಲಕ್ಷ', 'ಆರು ಲಕ್ಷ', 'ಎಂಟು ಲಕ್ಷ', 'ಹತ್ತು ಲಕ್ಷ', 'ಹನ್ನೆರಡು ಲಕ್ಷ', 'ಹದಿನಾಲ್ಕು ಲಕ್ಷ', 'ಹದಿನಾರು ಲಕ್ಷ',
                'ಹದಿನೆಂಟು ಲಕ್ಷ', 'ಇಪ್ಪತ್ತು ಲಕ್ಷ', 'ಮೂವತ್ತು ಲಕ್ಷ', 'ನಲವತ್ತು ಲಕ್ಷ', 'ನಲವತ್ತಾರು ಲಕ್ಷ', 'ನಲವತ್ತೆಂಟು ಲಕ್ಷ', 'ಐವತ್ತು ಲಕ್ಷ', 'ಐವತ್ತೆರಡು ಲಕ್ಷ',
                'ಐವತ್ತಾರು ಲಕ್ಷ', 'ಐವತ್ತೆಂಟು ಲಕ್ಷ', 'ಅರವತ್ತು ಲಕ್ಷ', 'ಅರವತ್ತೆರಡು ಲಕ್ಷ', 'ಅರವತ್ತಾರು ಲಕ್ಷ', 'ಅರವತ್ತೆಂಟು ಲಕ್ಷ', 'ಎಪ್ಪತ್ತೆರಡು ಲಕ್ಷ',
                'ಎಪ್ಪತ್ತಾರು ಲಕ್ಷ', 'ಎಪ್ಪತ್ತೆಂಟು ಲಕ್ಷ', 'ಎಂಬತ್ತೆರಡು ಲಕ್ಷ', 'ಎಂಬತ್ತಾರು ಲಕ್ಷ', 'ಎಂಬತ್ತೆಂಟು ಲಕ್ಷ', 'ತೊಂಬತ್ತು ಲಕ್ಷ', 'ತೊಂಬತ್ತೆರಡು ಲಕ್ಷ',
                'ತೊಂಬತ್ತಾರು ಲಕ್ಷ', 'ತೊಂಬತ್ತೆಂಟು ಲಕ್ಷ']

        expected_output = ['1,00,000', '2,00,000', '4,00,000', '6,00,000', '8,00,000', '10,00,000', '12,00,000',
                           '14,00,000', '16,00,000', '18,00,000', '20,00,000', '30,00,000', '40,00,000', '46,00,000',
                           '48,00,000', '50,00,000', '52,00,000', '56,00,000', '58,00,000', '60,00,000', '62,00,000',
                           '66,00,000', '68,00,000', '72,00,000', '76,00,000', '78,00,000', '82,00,000', '86,00,000',
                           '88,00,000', '90,00,000', '92,00,000', '96,00,000', '98,00,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='kn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_crores_are_converted_to_numerals(self):
        data = ['ಒಂದು ಕೋಟಿ', 'ಎರಡು ಕೋಟಿ', 'ನಾಲ್ಕು ಕೋಟಿ', 'ಆರು ಕೋಟಿ', 'ಎಂಟು ಕೋಟಿ', 'ಹತ್ತು ಕೋಟಿ', 'ಹನ್ನೆರಡು ಕೋಟಿ',
                'ಹದಿನಾಲ್ಕು ಕೋಟಿ', 'ಹದಿನಾರು ಕೋಟಿ', 'ಹದಿನೆಂಟು ಕೋಟಿ']

        expected_output = ['1,00,00,000', '2,00,00,000', '4,00,00,000', '6,00,00,000', '8,00,00,000', '10,00,00,000',
                           '12,00,00,000', '14,00,00,000', '16,00,00,000', '18,00,00,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='kn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_money_is_converted_to_corresponding_numerals(self):
        data = ['ನನ್ನ ಕೈಯಲ್ಲಿ ಐದು ಡಾಲರ್ ಇದೆ', 'ನನ್ನ ಬ್ಯಾಗ್ ನಲ್ಲಿ ಐದು ನೂರು ರೂಪಾಯಿ ಪೆನ್ನಿದೆ', 'ನನ್ನ ಖಾತೆಯಲ್ಲಿ ಐದು ಕೋಟಿ ಯೂರೋ ಇದೆ',
                'ನನ್ನ ಖಾತೆಯಲ್ಲಿ ಎಪ್ಪತ್ತೆರಡು ಸಾವಿರ ಪೌಂಡ್‌ಗಳ ಸ್ಟರ್ಲಿಂಗ್ ಇದೆ']
        expected_output = ['ನನ್ನ ಕೈಯಲ್ಲಿ $ 5 ಇದೆ', 'ನನ್ನ ಬ್ಯಾಗ್ ನಲ್ಲಿ ₹ 500 ಪೆನ್ನಿದೆ', 'ನನ್ನ ಖಾತೆಯಲ್ಲಿ € 5,00,00,000 ಇದೆ', 'ನನ್ನ ಖಾತೆಯಲ್ಲಿ £ 72,000 ಇದೆ']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='kn')

        self.assertEqual(expected_output, inverse_normalizer_prediction)


if __name__ == '__main__':
    unittest.main()
