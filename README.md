# Indic Punct Library

## Installation Instructions 

```buildoutcfg
git clone https://github.com/Open-Speech-EkStep/indic-punct.git
cd indic-punct
bash install.sh
python setup.py bdist_wheel
pip install -e .
```

## Usage

Currently (v 0.0.5) we are supporting the following languages:
- Punctuation:
  - Hindi ('hi')
  - English ('en')
  - Gujarati ('gu')
  - Telugu ('te')
  - Marathi ('mr')
  - Kannada ('kn')
  - Punjabi ('pa')
- Inverse Text Normalization:
  - Hindi
  - English
  - Gujarati
  - Telugu

We are planning to add other Indic languages. 

### Punctuation 
```buildoutcfg
from punctuate.punctuate_text import Punctuation
hindi = Punctuation('hi') #loads model in memory
english = Punctuation('en')
gujarati = Punctuation('gu')
hindi.punctuate_text(["इस श्रेणी में केवल निम्नलिखित उपश्रेणी है", "मेहुल को भारत को सौंप दिया जाए"])
english.punctuate_text(['how are you', 'great how about you'])
gujarati.punctuate_text(['નમસ્તે તમે કેમ છો', 'મારે કામે જવુ જ પડશે'])

----Outputs----
['इस श्रेणी में केवल निम्नलिखित उपश्रेणी है। ', 'मेहुल को भारत को सौंप दिया जाए। ']
['How are you?', 'Great, how about you?']
['નમસ્તે તમે કેમ છો? ', 'મારે કામે જવુ જ પડશે। ']
```

### Inverse Text Normalization
```buildoutcfg
from inverse_text_normalization.run_predict import inverse_normalize_text
inverse_normalize_text(['I have twenty cars',
                        'The army had four thousand six hundred forty six horses'],
                         lang='en')
inverse_normalize_text(['दस लाख एक हज़ार चार सौ बीस', 'चार करोड़ चार लाख'], lang='hi')
inverse_normalize_text(['મારી પાસે ત્રણ બિલાડીઓ છે', 'ચાર કરોડ ચાર લાખ', 'તેને એક હજાર ચારસો ચાર રૂપિયા આપો'], lang='gu')
inverse_normalize_text(['ఏడు లక్షల నాలుగు వేల తొమ్మిది వందల యాభై ఒకటి', 'నేను ఏడు వందల పదమూడు సినిమాలు చూశాను'], lang='te')

----Outputs----
['I have 20 cars', 'The army had 4646 horses']
['10,01,420', '4,04,00,000']    
['મારી પાસે 3 બિલાડીઓ છે', '4,04,00,000', 'તેને ₹ 1,404 આપો']
['7,04,951', 'నేను 713 సినిమాలు చూశాను']
```

