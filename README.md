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

Currently (v 2.0.5) we are supporting the following languages:
- Punctuation:
  - Hindi ('hi')
  - English ('en')
  - Gujarati ('gu')
  - Telugu ('te')
  - Marathi ('mr')
  - Kannada ('kn')
  - Punjabi ('pa')
  - Tamil ('ta')
  - Bengali ('bn')
  - Odia ('or')
  - Malayalam ('ml')
  - Assamese ('as')
  
- Inverse Text Normalization:
  - Hindi
  - English
  - Gujarati
  - Telugu
  - Marathi
  - Punjabi
  - Tamil
  - Bengali
  - Malayalam
  - Odia
  - Assamese
  - Kannada

We are planning to add other Indic languages. 

### Punctuation 
```buildoutcfg
from punctuate.punctuate_text import Punctuation
hindi = Punctuation('hi') #loads model in memory
english = Punctuation('en')
gujarati = Punctuation('gu')
telugu = Punctuation('te')
marathi = Punctuation('mr')
kannada = Punctuation('kn')
punjabi = Punctuation('pa')
tamil = Punctuation('ta')
bengali = Punctuation('bn')
odia = Punctuation('or')
malayalam = Punctuation('ml')
assamese = Punctuation('as')

hindi.punctuate_text(["इस श्रेणी में केवल निम्नलिखित उपश्रेणी है", "मेहुल को भारत को सौंप दिया जाए"])
english.punctuate_text(['how are you', 'great how about you'])
gujarati.punctuate_text(['નમસ્તે તમે કેમ છો', 'મારે કામે જવુ જ પડશે'])
telugu.punctuate_text(['రోహిత్ శర్మ విరాట్ కోహ్లీ రాహుల్ మరియు మహమ్మద్ షమీ భారతదేశం కోసం ఆడతారు'])
marathi.punctuate_text(['पण रामायण हिंदुत्व किंवा आजच्या भारतापुरते मर्यादित नाही तर इंडोनेशिया मलेशिया थायलंड कंबोडिया फिलिपिन्स व्हिएतनाम इत्यादींमध्येही प्रचलित आहे'])
kannada.punctuate_text(['ಬಿಜೆಪಿ ಕಾಂಗ್ರೆಸ್ ಮತ್ತು ಜನತಾದಳವು ಪ್ರತಿಷ್ಠಿತ ಸ್ಥಾನಗಳನ್ನು ಗಳಿಸಲು ಎಲ್ಲಾ ಹಂತಗಳನ್ನು ಹಿಂತೆಗೆದುಕೊಳ್ಳುತ್ತಿವೆ'])
punjabi.punctuate_text(['ਸਰੀਰ ਵਿੱਚ ਕੈਲਸ਼ੀਅਮ ਜ਼ਿੰਕ ਆਇਰਨ ਆਦਿ ਪੌਸ਼ਟਿਕ ਤੱਤਾਂ ਦੀ ਕਮੀ ਹੁੰਦੀ ਹੈ'])
tamil.punctuate_text(['உங்கள் பெயர் என்ன'])
bengali.punctuate_text(['যে কুড়ুলটা দিয়ে এই ধ্বংসলীলা হয়েছিল সেটিকে নিয়ে কী করা উচিত'])
odia.punctuate_text(['ମୋର ଅନେକ କଲମ ପେନ୍ସିଲ୍ ନୋଟବୁକ୍ ବହି ଏବଂ ଟେବୁଲ୍ ଅଛି', 'ଭାରତର ରାଜଧାନୀ କ’ଣ'])
malayalam.punctuate_text(['നിങ്ങൾ എവിടെ താമസിക്കുന്നു', 'ഇന്ന് ഒരു നല്ല ദിവസമാണ്'])
assamese.punctuate_text(['তোমাৰ ভাল নে'])

----Outputs----
['इस श्रेणी में केवल निम्नलिखित उपश्रेणी है। ', 'मेहुल को भारत को सौंप दिया जाए। ']
['How are you?', 'Great, how about you?']
['નમસ્તે તમે કેમ છો? ', 'મારે કામે જવુ જ પડશે। ']
['రోహిత్ శర్మ, విరాట్ కోహ్లీ, రాహుల్ మరియు మహమ్మద్ షమీ భారతదేశం కోసం ఆడతారు.']
['पण रामायण हिंदुत्व किंवा आजच्या भारतापुरते मर्यादित नाही तर इंडोनेशिया, मलेशिया, थायलंड, कंबोडिया, फिलिपिन्स, व्हिएतनाम इत्यादींमध्येही प्रचलित आहे.']
['ಬಿಜೆಪಿ, ಕಾಂಗ್ರೆಸ್ ಮತ್ತು ಜನತಾದಳವು ಪ್ರತಿಷ್ಠಿತ ಸ್ಥಾನಗಳನ್ನು ಗಳಿಸಲು ಎಲ್ಲಾ ಹಂತಗಳನ್ನು ಹಿಂತೆಗೆದುಕೊಳ್ಳುತ್ತಿವೆ.']
['ਸਰੀਰ ਵਿੱਚ ਕੈਲਸ਼ੀਅਮ ਜ਼ਿੰਕ, ਆਇਰਨ ਆਦਿ ਪੌਸ਼ਟਿਕ ਤੱਤਾਂ ਦੀ ਕਮੀ ਹੁੰਦੀ ਹੈ।']
['உங்கள் பெயர் என்ன? ']
['যে কুড়ুলটা দিয়ে এই ধ্বংসলীলা হয়েছিল, সেটিকে নিয়ে কী করা উচিত?']
['ମୋର ଅନେକ କଲମ ପେନ୍ସିଲ୍, ନୋଟବୁକ୍ ବହି ଏବଂ ଟେବୁଲ୍ ଅଛି।','ଭାରତର ରାଜଧାନୀ କ’ଣ?']
['നിങ്ങൾ എവിടെ താമസിക്കുന്നു? ', 'ഇന്ന് ഒരു നല്ല ദിവസമാണ്. ']
['তোমাৰ ভাল নে? ']
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
inverse_normalize_text(['रीटाकडे नऊशे वीस मांजरी आहेत','बत्तीस कोटी एकवीस लाख सदतीस हजार चारशे बारा'], lang='mr')
inverse_normalize_text(['ਬਾਰਾਂ ਲੱਖ ਵੀਹ ਹਜਾਰ ਸੱਤ ਸੌ ਪੰਦਰਾਂ','ਮੇਰੇ ਕੋਲ ਦਸ ਰੁਪਏ ਹਨ'], lang='pa')
inverse_normalize_text(['ஒன்று நூறு முப்பத்து ஒன்பது படங்கள் பார்த்திருக்கிறேன்','தொண்ணூற்றிநான்கு கோடி ஐந்து இலட்சம் முந்நூறு இருபத்து இரண்டு'], lang='ta')
inverse_normalize_text(['আমার পাঁচটি কলম আছে', 'তিনি দুইশত সাতটি সিনেমা দেখেছেন'], lang='bn')
inverse_normalize_text(['ഇരുനൂറ്റി അമ്പത് രൂപ ഞാൻ അവന് കൊടുത്തു', 'അവൻ എനിക്ക് പത്ത് യൂറോ തന്നു'], lang='ml')
inverse_normalize_text(['ମୋ ହାତରେ ପାଞ୍ଚ ଡଲାର ଅଛି', 'ମୋ ହାତରେ ପାଞ୍ଚ ଶହ ଟଙ୍କା ଅଛି', 'ମୋ ହାତରେ ସାତ ଶହ ୟୁରୋ ଅଛି'], lang='or')
inverse_normalize_text(['মই 10 বাকচ মিঠাই বিতৰণ কৰিলো', 'নিৰান্নব্বৈটা কোটি পাঁচ লাখ আঠশ বাইছ'], lang='as')
inverse_normalize_text(['ನನ್ನ ಕೈಯಲ್ಲಿ ಐದು ಡಾಲರ್ ಇದೆ', 'ನನ್ನ ಬ್ಯಾಗ್ ನಲ್ಲಿ ಐದು ನೂರು ರೂಪಾಯಿ ಪೆನ್ನಿದೆ', 'ನನ್ನ ಖಾತೆಯಲ್ಲಿ ಐದು ಕೋಟಿ ಯೂರೋ ಇದೆ'], lang='kn')

----Outputs----
['I have 20 cars', 'The army had 4646 horses']
['10,01,420', '4,04,00,000']    
['મારી પાસે 3 બિલાડીઓ છે', '4,04,00,000', 'તેને ₹ 1,404 આપો']
['7,04,951', 'నేను 713 సినిమాలు చూశాను']
['रीटाकडे 920 मांजरी आहेत','32,21,37,412']
['12,20,715', 'ਮੇਰੇ ਕੋਲ ₹ 10 ਹਨ']
['139 படங்கள் பார்த்திருக்கிறேன்', '94,05,00,322']
['আমার 5 কলম আছে', 'তিনি 207 সিনেমা দেখেছেন']
['₹ 250 ഞാൻ അവന് കൊടുത്തു', 'അവൻ എനിക്ക് € 10 തന്നു']
['ମୋ ହାତରେ $ 5 ଅଛି', 'ମୋ ହାତରେ ₹ 500 ଅଛି', 'ମୋ ହାତରେ € 700 ଅଛି']
['মই 10 বাকচ মিঠাই বিতৰণ কৰিলো', '99,05,00,822']
['ನನ್ನ ಕೈಯಲ್ಲಿ $ 5 ಇದೆ', 'ನನ್ನ ಬ್ಯಾಗ್ ನಲ್ಲಿ ₹ 500 ಪೆನ್ನಿದೆ', 'ನನ್ನ ಖಾತೆಯಲ್ಲಿ € 5,00,00,000 ಇದೆ']
```

