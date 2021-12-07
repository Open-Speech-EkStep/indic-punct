"""
Please move this file to src/ before running the tests
"""

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class OriyaInverseTextNormalization(unittest.TestCase):

    def test_single_digit_numbers_are_converted_to_numerals(self):
        data = ['ଶୂନ', 'ଏକ', 'ଦୁଇ', 'ତିନି', 'ଚାରି', 'ପାଞ୍ଚ', 'ଛଅ', 'ସାତ', 'ଆଠ', 'ନଅ']
        expected_output = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='or')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_double_digit_numbers_are_converted_to_numerals(self):
        data = ['ଏଗାର', 'ଉଣେଇଶ', 'ଏକାବନ', 'ବାଷଠି', 'ଅଠାଅଶୀ', 'ଅନେଶତ']
        expected_output = ['11', '19', '51', '62', '88', '99']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='or')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_multiples_of_hundreds_are_converted_to_numerals(self):
        # data = ['ଶହେ', 'ଦୁଇ ଶହେ', 'ତିନି ଶହେ', 'ଚାରି ଶହେ', 'ପାଞ୍ଚ ଶହେ', 'ଛଅ ଶହେ', 'ସାତ ଶହେ', 'ଆଠ ଶହେ', 'ନଅ ଶହେ']
        # expected_output = ['100', '200', '300', '400', '500', '600', '700', '800', '900']

        data = ['ଏକ ଶହେ ପାଞ୍ଚ', 'ଏକ ଶହେ ପଞ୍ଚାବନ', 'ଦୁଇ ଶହେ ଏଗାର', 'ପାଞ୍ଚ ଶହେ ପଞ୍ଚାବନ', 'ନଅ ଶହେ ଅନେଶତ',
                'ଆଠ ଶହେ ପଞ୍ଚଚାଳିଶି', 'ସାତ ଶହେ ବାସ୍ତରୀ']
        expected_output = ['105', '155', '211', '555', '999', '845', '772']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='or')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_thousand_are_converted_to_numerals(self):
        data = ['ହଜାର', 'ଏକ ହଜାର ଏକ', 'ଏକ ହଜାର ନଅ', 'ଏକ ହଜାର ଏକ ଶହେ', 'ଏକ ହଜାର ଏକ ଶହେ ପଚାଶ', 'ଏକ ହଜାର ଦୁଇ ଶହେ ପଚାଶ',
                'ଏକ ହଜାର ତିନି ଶହେ ପଞ୍ଚସ୍ତରୀ', 'ଏକ ହଜାର ଚାରି ଶହେ ଚଉରାଳିଶି', 'ଏକ ହଜାର ପାଞ୍ଚ ଶହେ',
                'ଦୁଇ ହଜାର ପାଞ୍ଚ ଶହେ ପଞ୍ଚାବନ',
                'ତିନି ହଜାର ତିନି ଶହେ ତେତିଶି', 'ଚାରି ହଜାର ଚାରି ଶହେ ଚଉରାଳିଶି', 'ସାତ ହଜାର ସାତ ଶହେ ସତସ୍ତରୀ',
                'ଆଠ ହଜାର ଆଠ ଶହେ ଅଠାଅଶୀ',
                'ନଅ ହଜାର ନଅ ଶହେ ଅନେଶତ', 'ଦଶ ହଜାର', 'ଦଶ ହଜାର ପାଞ୍ଚ', 'ଦଶ  ହଜାର ପଚାଶ', 'ଦଶ ହଜାର ପାଞ୍ଚ ଶହେ',
                'ଏଗାର ହଜାର ପାଞ୍ଚ ଶହେ',
                'ପନ୍ଦର ହଜାର ପାଞ୍ଚ ଶହେ', 'ପଚିଶି ହଜାର ପାଞ୍ଚ ଶହେ', 'ପଞ୍ଚାବନ ହଜାର ନଅ ଶହେ', 'ଅନେଶତ ହଜାର ନଅ ଶହେ ଅନେଶତ']

        expected_output = ['1000', '1001', '1009', '1100', '1150', '1250', '1375', '1444', '1500', '2555', '3333',
                           '4444', '7777', '8888', '9999', '10,000', '10,005', '10,050', '10,500', '11,500', '15,500',
                           '25,500', '55,900', '99,999']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='or')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_lakhs_are_converted_to_numerals(self):
        data = ['ଏକ ଲକ୍ଷ', 'ଏକ ଲକ୍ଷ ଏକ', 'ଏକ ଲକ୍ଷ ଦଶ', 'ଏକ ଲକ୍ଷ ଏକ ଶହେ', 'ଏକ ଲକ୍ଷ ଏକ ହଜାର', 'ଏକ ଲକ୍ଷ ଦଶ ହଜାର',
                'ଦୁଇ ଲକ୍ଷ ଅନେଶତ ହଜାର ନଅ ଶହେ ଅନେଶତ', 'ନଅ ଲକ୍ଷ ଅନେଶତ ହଜାର ନଅ ଶହେ ଅନେଶତ',
                'ପାଞ୍ଚ ଲକ୍ଷ ପଞ୍ଚାବନ ହଜାର ପାଞ୍ଚ ଶହେ ପଞ୍ଚାବନ',
                'ପନ୍ଦର ଲକ୍ଷ ପଞ୍ଚାବନ ହଜାର ପାଞ୍ଚ ଶହେ ପଞ୍ଚାବନ', 'ଏଗାର ଲକ୍ଷ ଏଗାର ହଜାର ଏକ ଶହେ ଏଗାର',
                'ସତସ୍ତରୀ ଲକ୍ଷ ସତସ୍ତରୀ ହଜାର ସାତ ଶହେ ସତସ୍ତରୀ',
                'ଅନେଶତ ଲକ୍ଷ ଅନେଶତ ହଜାର ନଅ ଶହେ ଅନେଶତ']

        expected_output = ['1,00,000', '1,00,001', '1,00,010', '1,00,100', '1,01,000', '1,10,000', '2,99,999',
                           '9,99,999',
                           '5,55,555', '15,55,555', '11,11,111', '77,77,777', '99,99,999']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='or')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_crores_are_converted_to_numerals(self):
        data = ['ଏକ କୋଟି ଅନେଶତ ଲକ୍ଷ ଅନେଶତ ହଜାର ନଅ ଶହେ ଅନେଶତ', 'ଏକ କୋଟି',
                'ତିନି କୋଟି ତେତିଶି ଲକ୍ଷ ତେତିଶି ହଜାର ତିନି ଶହେ ତେତିଶି',
                'ଆଠ କୋଟି ଅଠାଅଶୀ ଲକ୍ଷ ଅଠାଅଶୀ ହଜାର ଆଠ ଶହେ ଅଠାଅଶୀ', 'ନଅ କୋଟି ଅନେଶତ ଲକ୍ଷ ଅନେଶତ ହଜାର ନଅ ଶହେ ଅନେଶତ',
                'ଦଶ କୋଟି',
                'ପଚିଶି କୋଟି', 'ଅନେଶତ କୋଟି ଅନେଶତ ଲକ୍ଷ ଅନେଶତ ହଜାର ନଅ ଶହେ ଅନେଶତ']

        expected_output = ['1,99,99,999', '1,00,00,000', '3,33,33,333', '8,88,88,888', '9,99,99,999', '10,00,00,000',
                           '25,00,00,000', '99,99,99,999']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='or')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_money_is_converted_to_corresponding_numerals(self):
        data = ['ମୋ ହାତରେ ପାଞ୍ଚ ଡଲାର ଅଛି', 'ମୋ ହାତରେ ପାଞ୍ଚ ଶହ ଟଙ୍କା ଅଛି', 'ମୋ ହାତରେ ସାତ ଶହ ୟୁରୋ ଅଛି',
                'ମୋ ହାତରେ ତିନି ଶହ ଅନେଶତ ପାଉଣ୍ଡ ଷ୍ଟର୍ଲିଂ ଅଛି']
        expected_output = ['ମୋ ହାତରେ $ 5 ଅଛି', 'ମୋ ହାତରେ ₹ 500 ଅଛି', 'ମୋ ହାତରେ € 700 ଅଛି', 'ମୋ ହାତରେ £ 399 ଅଛି']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='or')

        self.assertEqual(expected_output, inverse_normalizer_prediction)


if __name__ == '__main__':
    unittest.main()
