'''
Please move this file to src/ before running the tests
'''

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class TeluguInverseTextNormalization(unittest.TestCase):

    def test_single_digit_numbers_are_converted_to_numerals(self):
        data = ['ఒకటి',  # okati (1)
                'ఎనిమిది',  # 8
                'నాకు ఒకటి పిల్లి ఉంది'  # I have 1 cat (okati)
                ]
        expected_output = ['1', '8', 'నాకు 1 పిల్లి ఉంది']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_double_digit_numbers_are_converted_to_numerals(self):
        data = ['ఇరవై మూడు',  # iravai mudu (23)
                'ఆమెకు ఇరవై మూడు పిల్లులు ఉన్నాయి',  # She has 23 cats
                'మీరు దీని పంతొమ్మిది కాపీలు చేయగలరా',  # can you make 19 copies of this
                'మీరు దీని పందొమ్మిది కాపీలు చేయగలరా',  # can you make 19 copies of this (alt spelling of 19)
                'నాకు యాభై ఏడు పిల్లులు ఉన్నాయి'  # i have 57 cats
                ]
        expected_output = ['23', 'ఆమెకు 23 పిల్లులు ఉన్నాయి', 'మీరు దీని 19 కాపీలు చేయగలరా',
                           'మీరు దీని 19 కాపీలు చేయగలరా', 'నాకు 57 పిల్లులు ఉన్నాయి']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_multiples_of_ten_are_converted_to_numerals(self):
        '''
        Tests both the ways of writing some characters: with normalization and without.
        Google outputs composite chars like ['ై'] instead of ['ె', 'ౖ'].
        Our current ASR model can only predict ['ై']

        '''
        data = ['ఇరవై',  # 20 ours
                'ఇరవై',  # 20 google
                'ముప్పై',  # 30 ours
                'ముప్పై',  # 30 google
                'నలభై',  # 40 ours
                'నలభై',  # 40 google
                'యాభై',  # 50 ours
                'యాభై',  # 50 google
                'అరవై',  # 60 ours
                'అరవై',  # 60 google
                'డెబ్బై',  # 70 ours
                'డెబ్భై',  # 70 google
                'ఎనభై',  # 80 ours
                'ఎనభై',  # 80 google
                'తొంభై',  # 90 ours
                'తొం బై'  # 90 google
                ]
        expected_output = ['20', '20', '30', '30', '40', '40', '50', '50', '60', '60', '70', '70', '80', '80', '90',
                           '90']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_series_of_forty_is_converted_to_numerals(self):
        '''
        Series of 40 also has the same normalization issue:
        Tests both the ways of writing some characters: with normalization and without.
        Google outputs composite chars like ['ై'] instead of ['ె', 'ౖ'].
        Our current ASR model can only predict ['ై']
        '''
        data = ['నలభై మూడు',  # 43 ours
                'నలభై మూడు',  # 43 google
                'నలభై ఏడు',  # 47 ours
                'నలభై ఏడు'  # 47 google
                ]
        expected_output = ['43', '43', '47', '47']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_hundreds_are_converted_to_numerals(self):
        data = ['వంద',  # vanda (100)
                'ఒకటి వంద', # okati vanda (one hundred) 
                'రెండు వంద',  # Rendu vanda
                'రెండు వందలు',  # Rendu vandalu 200
                'తొమ్మిది వందలు మూడు',  # tomidi vandalu mudu 903
                'తొమ్మిది వందల మూడు',  # tomidi vandala mudu 903
                'నేను ఏడు వందల పదమూడు సినిమాలు చూశాను'  # i have seen 713 movies
                ]
        expected_output = ['100', '100', '200', '200', '903', '903', 'నేను 713 సినిమాలు చూశాను']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_tens_of_hundreds_are_converted_to_numerals(self):
        data = ['పన్నెండు వందల నలభై నాలుగు',  # 1244 ours
                'పన్నెండు వందల నలభై నాలుగు',  # 1244 google
                'పన్నెండు వందల నలభై',  # 1240 google
                'పన్నెండు వందల నలభై',  # 1240 ours
                'ఎనభై తొమ్మిది వందల అరవై ఐదు',  # 8965
                'పదమూడు వందల తొమ్మిది'  # 1309
                ]
        expected_output = ['1,244', '1,244', '1,240', '1,240', '8,965', '1,309']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_thousands_are_converted_to_numerals(self):
        data = ['వెయ్యి',  # veyyi (en:thousand)google
                'ఒకటి వెయ్యి',  # okati veyyi
                'ఏడు వెయ్యి',  # Ēḍu veyyi

                'ఏడు వేలు',  # Ēḍu vēlu 7000
                'ఏడు వేల ఎనిమిది',  # Ēḍu velu enimidi 7008
                'ఏడు వేల ఎనిమిది',  # Ēḍu vēla enimidi 7008

                'ఏడు వేల యాభై ఆరు',  # Ēḍu vēla yābhai āru 7056
                'ఐదు వేల ఎనభై మూడు',  # 5083
                'తొమ్మిది వేల మూడు వందలు',  # Tom'midi vēla mūḍu vandalu 9300
                'తొమ్మిది వేల ఐదు వందల డెబ్బై రెండు'  # Tom'midi vēla aidu vandala ḍebbai reṇḍu 9572

                ]
        expected_output = ['1,000', '1,000', '7,000', '7,000',
                           '7,008', '7,008',
                           '7,056', '5,083',
                           '9,300', '9,572'
                           ]

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_lakhs_are_converted_to_numerals(self):
        data = ['లక్ష',  # only "lakh" laska
                'ఒక లక్ష',  # oka laksa (one lakh, but oka is more like "a")
                'ఐదు లక్షల మూడు వందలు',  # 5,00,300
                'ఏడు లక్షల నాలుగు వేల తొమ్మిది వందల యాభై ఒకటి',  # 7,04,951
                'మూడు లక్షల ఎనభై ఆరు వేల ఏడు వందల నలభై ఎనిమిది',  # 3,86,748
                'నాలుగు లక్షల నలభై తొమ్మిది',  # 4,00,049
                'డెబ్బై లక్షలు',  # 70,00,000
                'పదిహేను లక్షల ఇరవై ఏడు వేలు'  # 15,27,000
                ]
        expected_output = ['1,00,000',
                           'ఒక 1,00,000',
                           '5,00,300',
                           '7,04,951',
                           '3,86,748',
                           '4,00,049',
                           '70,00,000',
                           '15,27,000'
                           ]

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_crores_are_converted_to_numerals(self):
        data = ['కోటి',  # only "crore" koti
                'ఐదు కోట్ల ఏడు లక్షలు',  # 5,07,00,000
                'మూడు కోట్ల ఇరవై లక్షల డెబ్బై ఐదు',  # 3,20,00,075
                'ఎనభై ఒకటి కోటి'  # 81,00,00,000
                ]
        expected_output = ['1,00,00,000',
                           '5,07,00,000',
                           '3,20,00,075',
                           '81,00,00,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_hundreds_of_crores_or_lakhs_are_converted_to_numerals(self):
        data = ['నాలుగు వందల కోట్లు',  # 400 crore
                'ఐదు వందల లక్షలు' # 500 lakh
                ]
        expected_output = ['4,00,00,00,000',
                           '5,00,00,000'
                           ]

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='te')

        self.assertEqual(expected_output, inverse_normalizer_prediction)


if __name__ == '__main__':
    unittest.main()
