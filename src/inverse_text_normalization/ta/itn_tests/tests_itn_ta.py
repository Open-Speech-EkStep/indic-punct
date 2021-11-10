'''
Please move this file to src/ before running the tests
'''

import unittest
from inverse_text_normalization.run_predict import inverse_normalize_text


class TamilInverseTextNormalization(unittest.TestCase):

    def test_single_digit_numbers_are_converted_to_numerals(self):
        data = ['நான்கு', 'எட்டு', 'என்னிடம் ஐந்து பேனாக்கள் உள்ளன']
        expected_output = ['4', '8', 'என்னிடம் 5 பேனாக்கள் உள்ளன']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ta')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_double_digit_numbers_are_converted_to_numerals(self):
        data = ['பதினெட்டு', 'என்னிடம் ஐம்பது பூனைகள் உள்ளன', 'என்னிடம் எண்பத்தியொன்று பேனாக்கள் உள்ளன'
                'என்னிடம் இருபத்து நான்கு பேனாக்கள் உள்ளன']
        expected_output = ['18', 'என்னிடம் 50 பூனைகள் உள்ளன', 'என்னிடம் 81 பேனாக்கள் உள்ளன'
                           'என்னிடம் 24 பேனாக்கள் உள்ளன']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ta')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_upto_nine_with_hundreds_are_converted_to_numerals(self):
        #TODO: spelling of 900/90
        '''
        Numbers from 200 to 900 do not follow normal grammar
        '''
        data = ['நூறு',
                'இருநூறு',
                'முந்நூறு',
                'நானூறு',
                'ஐநூறு',
                'அறுநூறு',
                'எழுநூறு',
                'எண்ணூறு',
                'தொண்ணூறு' #90 not 900 tulayeram
                ]
        expected_output = ['100',
                           '200',
                           '300',
                           '400',
                           '500',
                           '600',
                           '700',
                           '800',
                           '900']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ta')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_hundreds_are_converted_to_numerals(self):
        data = ['இருநூறு',
                'இருநூறு மூன்று',
                'ஒன்று நூறு முப்பத்து ஒன்பது படங்கள் பார்த்திருக்கிறேன்',
                'அவளிடம் எண்ணூறு நாற்பத்து நான்கு அட்டைகள் உள்ளன'
                ]
        expected_output = ['200',
                           '203',
                           '139 படங்கள் பார்த்திருக்கிறேன்',
                           'அவளிடம் 844 அட்டைகள் உள்ளன'
                           ]

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ta')

        self.assertEqual(expected_output, inverse_normalizer_prediction)



    def test_num_with_tens_of_hundreds_are_converted_to_numerals(self):
        data = ['பதினொன்று நூறு',
                 'பன்னிரண்டு நூறு தொண்ணூற்றிஒன்பது',
                 'முப்பத்து ஆறு நூறு அறுபத்து ஏழு',
                 'எண்பத்தியொன்பது நூறு இருபத்து மூன்று']
        expected_output = ['1100',
                           '1299',
                           '3667',
                           '8923']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ta')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_thousands_are_converted_to_numerals(self):
        data = ['ஆயிரம்',
                'ஒன்று ஆயிரம்',
                'ஒன்று ஆயிரம் முப்பத்து ஒன்று',
                'இருபத்து ஆறு ஆயிரம்'
                ]
        expected_output = ['1000', '1000', '1031', '26,000']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ta')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_lakhs_are_converted_to_numerals(self):
        data = ['இலட்சம்','ஒன்று இலட்சம்', 'ஒன்பது இலட்சம்',
                'நாற்பத்து ஆறு இலட்சம் இருபத்து மூன்று ஆயிரம் ஒன்பது நூறு ஐம்பத்து இரண்டு',
                'நாற்பத்து ஆறு இலட்சம் இருபத்து மூன்று ஆயிரம் தொண்ணூறு ஐம்பத்து இரண்டு'
                ]
        expected_output = ['1,00,000', '1,00,000', '9,00,000', '46,23,952', '46,23,952']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ta')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_num_with_crores_are_converted_to_numerals(self):
        data = ['கோடி',
                'ஒன்று கோடி',
                'ஏழு கோடி',
                'தொண்ணூற்றிநான்கு கோடி ஐந்து இலட்சம் முந்நூறு இருபத்து இரண்டு'
                ]

        expected_output = ['1,00,00,000',
                           '1,00,00,000',
                           '7,00,00,000',
                           '94,05,00,322']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ta')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

    def test_money_is_converted_to_corresponding_numerals(self):
        data = ['ஆறு கோடி ரூபாய்',#'கோடி ரூபாய்',
                'முந்நூறு ரூபாய்',
                'வங்கியில் பத்து ரூபாய் கடன் வாங்கினார்',
                'அவளிடம் இருபது டாலர்கள் உள்ளன',
                'அவளிடம் ஒன்று நூறு பவுண்டுகள் உள்ளன'
                ]

        expected_output = ['₹ 6,00,00,000',
                           '₹ 300',
                           'வங்கியில் ₹ 10 கடன் வாங்கினார்',
                           'அவளிடம் $ 20 உள்ளன',
                           'அவளிடம் £ 100 உள்ளன']

        inverse_normalizer_prediction = inverse_normalize_text(data, lang='ta')

        self.assertEqual(expected_output, inverse_normalizer_prediction)

if __name__ == '__main__':
    unittest.main()
