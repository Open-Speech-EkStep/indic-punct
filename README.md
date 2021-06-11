# Indic Punct Library

## Installation Instructions 

### Method 1 
```buildoutcfg
git clone https://github.com/Open-Speech-EkStep/indic-punct.git
cd indic-punct
bash install.sh
python setup.py bdist_wheel
pip install -e .
```

### Method 2 
```buildoutcfg
git clone https://github.com/Open-Speech-EkStep/indic-punct.git
cd indic-punct
bash install.sh
pip install git+https://github.com/Open-Speech-EkStep/indic-punct.git#egg=indic-punct
```

## Usage
Currently we are supporting punctuation and inverse text normalization for Hindi and English. 
We are planning to add other Indic languages. 

### Punctuation 
```buildoutcfg
from punctuate.punctuate_text import Punctuation
hindi = Punctuation('hi') #loads model in memory
english = Punctuation('en')
hindi.punctuate_text(["इस श्रेणी में केवल निम्नलिखित उपश्रेणी है", "मेहुल को भारत को सौंप दिया जाए"])
english.punctuate_text(['how are you', 'great how about you'])
['इस श्रेणी में केवल निम्नलिखित उपश्रेणी है। ', 'मेहुल को भारत को सौंप दिया जाए। ']
['How are you?', 'Great, how about you?']
```

### Inverse Text Normalization
```buildoutcfg
from inverse_text_normalization.run_predict import inverse_normalize_text
inverse_normalize_text(['I have twenty cars',
                        'The army had four thousand six hundred forty six horses'],
                         lang='en')
inverse_normalize_text(['दस लाख एक हज़ार चार सौ बीस', 'चार करोड़ चार लाख'], lang='hi')
['I have 20 cars', 'The army had 4646 horses']
['10,01,420', '4,04,00,000']                    
```

