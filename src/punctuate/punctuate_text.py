import torch
from transformers import AlbertForTokenClassification, AlbertTokenizer
import numpy as np
import json
import torch.nn as nn
from indicnlp.tokenize import indic_tokenize
import os
import wget
import sys
from nemo.collections.nlp.models import PunctuationCapitalizationModel
#import sysconfig

#cache = sysconfig.get_path('purelib') + '/'

class Punctuation:
    def __init__(self, language_code):
        self.language_code = language_code
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.language_code == 'en':
            self.model_path = 'deployed_models/model_data/punctuation_en_bert.nemo'
            self.download_model_data()
            self.model = PunctuationCapitalizationModel.restore_from(self.model_path)
        else:
            self.model_path = 'deployed_models/model_data/' + self.language_code + '.pt'
            self.encoder_path = 'deployed_models/model_data/' + self.language_code + '.json'
            self.dict_map = 'deployed_models/model_data/' + self.language_code + '_dict.json'
            self.tokenizer, self.model = self.load_model_parameters()


    def bar_thermometer(self, current, total, width=80):
        progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    def download_model_data(self):

        if not os.path.exists('deployed_models/model_data'):
            os.makedirs('deployed_models/model_data', exist_ok=True)

        if self.language_code == 'en':
            if not os.path.exists(self.model_path):
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/{self.language_code}/punctuation_en_bert.nemo',
                    self.model_path, bar=self.bar_thermometer)
        else:
            if not os.path.exists(self.model_path):
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/{self.language_code}/{self.language_code}.pt',
                    self.model_path, bar=self.bar_thermometer)

            if not os.path.exists(self.encoder_path):
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/{self.language_code}/{self.language_code}.json',
                    self.encoder_path, bar=self.bar_thermometer)

            if not os.path.exists(self.dict_map):
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/{self.language_code}/{self.language_code}_dict.json',
                    self.dict_map, bar=self.bar_thermometer)

    def load_model_parameters(self):
        self.download_model_data()
        with open(self.encoder_path) as label_encoder:
            train_encoder = json.load(label_encoder)

        tokenizer = AlbertTokenizer.from_pretrained('ai4bharat/indic-bert')

        model = AlbertForTokenClassification.from_pretrained('ai4bharat/indic-bert',
                                                             num_labels=len(train_encoder),
                                                             output_attentions=False,
                                                             output_hidden_states=False)

        model = nn.DataParallel(model)
        checkpoint = torch.load(self.model_path, map_location=self.device)
        model.load_state_dict(checkpoint['state_dict'])
        model = model.module.to(self.device)

        model.eval()
        return tokenizer, model

    def get_tokens_and_labels_indices_from_text(self, text):

        tokenized_sentence = self.tokenizer.encode(text)
        input_ids = torch.tensor([tokenized_sentence]).to(self.device)
        with torch.no_grad():
            output = self.model(input_ids)
        label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
        return tokens, label_indices

    def punctuate_text_others(self, text):
        print('current working dir:', os.getcwd())
        print('abs path:', os.path.abspath(self.encoder_path))
#         print('cache path:', cache)

        with open(self.encoder_path) as label_encoder:
            train_encoder = json.load(label_encoder)

        with open(self.dict_map) as dict_map:
            punctuation_dict = json.load(dict_map)

        punctuated_sentences = []

        for sentence in text:

            tokens, label_indices = self.get_tokens_and_labels_indices_from_text(sentence)

            new_tokens = []
            new_labels = []
            for i in range(1, len(tokens) - 1):
                if tokens[i].startswith("▁"):
                    current_word = tokens[i][1:]
                    new_labels.append(list(train_encoder.keys())[list(train_encoder.values()).index(label_indices[0][i])])
                    for j in range(i + 1, len(tokens) - 1):
                        if not tokens[j].startswith("▁"):
                            current_word = current_word + tokens[j]
                        if tokens[j].startswith("▁"):
                            break
                    new_tokens.append(current_word)
            full_text = ''
            tokenized_text = indic_tokenize.trivial_tokenize_indic(sentence)
            
            new_labels = ['blank' if x=='PAD' else x for x in new_labels] #fix for PAD predicted in outputs

            if len(tokenized_text) == len(new_labels):
                full_text_tokens = tokenized_text
            else:
                full_text_tokens = new_tokens

            for word, punctuation in zip(full_text_tokens, new_labels):
                full_text = full_text + word + punctuation_dict[punctuation]
            punctuated_sentences.append(full_text)

        return punctuated_sentences

    def punctuate_text_english(self, text):
        self.model = self.model.to(self.device)
        return self.model.add_punctuation_capitalization(text)

    def punctuate_text(self, text):
        if len(text.strip()) == 0:
            return ''
        if self.language_code == 'en':
            return self.punctuate_text_english(text)
        elif self.language_code in ['hi', 'gu', 'te', 'mr', 'kn', 'pa', 'ta']:
            return self.punctuate_text_others(text)


if __name__ == "__main__":
    
    punjabi = Punctuation('pa')
    print(*punjabi.punctuate_text(
        ['ਸਰੀਰ ਵਿੱਚ ਕੈਲਸ਼ੀਅਮ ਜ਼ਿੰਕ ਆਇਰਨ ਆਦਿ ਪੌਸ਼ਟਿਕ ਤੱਤਾਂ ਦੀ ਕਮੀ ਹੁੰਦੀ ਹੈ',
        'ਕੀ ਆਰਿਅਨ ਖਾਨ ਘਰ ਤੇ ਦੀਵਾਲੀਆਪਨ ਖਰਚ ਕਰਦਾ ਹੈ',
        'ਭਾਜਪਾ ਕਾਂਗਰਸ ਅਤੇ ਜਨਤਾ ਦਲ ਵੱਕਾਰੀ ਸੀਟਾਂ ਹਾਸਲ ਕਰਨ ਲਈ ਸਾਰੇ ਕਦਮ ਵਾਪਸ ਲੈ ਰਹੇ ਹਨ',
        'ਭਾਰਤ-ਪਾਕਿਸਤਾਨ ਮੈਚ ਨਾਲ ਸਬੰਧਤ ਹੈਸ਼ਟੈਗ ਐਤਵਾਰ ਸਵੇਰ ਤੋਂ ਸੋਸ਼ਲ ਮੀਡੀਆ ਤੇ ਟ੍ਰੈਂਡ ਕਰ ਰਹੇ ਹਨ']
    ), sep='\n')
    
    kannada = Punctuation('kn')
    print(*kannada.punctuate_text(
        ['ವೀಡಿಯೋದಲ್ಲಿ ಏನಿದೆ',
        'ಹೇಗೆ ದೀರ್ಘಕಾಲದ ಕೊಲೈಟಿಸ್ ತಡೆಗಟ್ಟಲು',
        'ಡಿಸೈನರ್ ಸಲಹೆಃ ನಿಮ್ಮ ಕೋಣೆ ತುಂಬಾ ಕಡಿಮೆಯಾಗಿರುವುದರಿಂದ ತೊಂದರೆ ನಿದ್ರಿಸುವುದೇ',
        'ದೇಹದಲ್ಲಿ ಪೋಷಕಾಂಶಗಳು ಕ್ಯಾಲ್ಸಿಯಂ ಜಿಂಕ್ ಕಬ್ಬಿಣ ಇತ್ಯಾದಿ ಕೊರತೆ',
        'ಆದರೆ ಬಿಸಿಸಿಐ ಹಾಗೂ ತಮ್ಮ ಪರ ವಕೀಲರೊಂದಿಗೆ ನಿರಂತರವಾಗಿ ಸಂಪರ್ಕದಲ್ಲಿದ್ದಾರೆ']
        ), sep='\n')
    
    telugu = Punctuation('te')
    print(*telugu.punctuate_text(
        ['జీనియస్','ఈ ఫిర్యాదుపై ఈ ఏడాది లాడౌ అనంతరం విచారణ జరిపిన హిస్సార్ పోలీసులు యువరాపై ఎస్సీ, ఎస్టీ అట్రాసిటీ కింద కేసు నమోదు చేసారు']
        ), sep='\n')

    gujarati = Punctuation('gu')
    print(*gujarati.punctuate_text(
        ['તું શું કરે છે', 'ઘણા દેશોએ રોગચાળાને કારણે બંધ થયાના લગભગ બે વર્ષ પછી હવે આંતરરાષ્ટ્રીય પ્રવાસીઓ માટે તેમની સરહદો ફરીથી ખોલી છે']
        ), sep='\n')

    marathi = Punctuation('mr')
    print(*marathi.punctuate_text(
        ['तू काय करत आहेस','साथीच्या आजारामुळे बंद झाल्यावर जवळजवळ दोन वर्षांनी अनेक देशांनी आता आंतरराष्ट्रीय पर्यटकांसाठी त्यांच्या सीमा पुन्हा उघडल्या आहेत']
        ), sep='\n')

                                    
