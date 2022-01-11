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
import sysconfig
import string
import shutil
cache = sysconfig.get_path('purelib') + '/'


class Punctuation:
    def __init__(self, language_code):
        self.language_code = language_code
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.language_code in ['en', 'en_bio']:
            os.environ["TRANSFORMERS_CACHE"] = str(cache + 'deployed_models/model_data/transformers_cache')
            self.model_path = cache+'deployed_models/model_data/punctuation_en_distilbert.nemo'
            self.download_model_data()
            self.model = PunctuationCapitalizationModel.restore_from(self.model_path)
            self.model = self.model.to(self.device)
        else:
            self.model_path = cache + 'deployed_models/model_data/' + self.language_code + '.pt'
            self.albert_metadata = cache + 'deployed_models/model_data/albert_metadata/'
            self.encoder_path = cache + 'deployed_models/model_data/' + self.language_code + '.json'
            self.dict_map = cache + 'deployed_models/model_data/' + self.language_code + '_dict.json'
            self.tokenizer, self.model, self.train_encoder, self.punctuation_dict = self.load_model_parameters()

    def bar_thermometer(self, current, total, width=80):
        progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    def download_model_data(self):
        
        if not os.path.exists(cache + 'deployed_models/model_data/transformers_cache'):
            os.makedirs(cache + 'deployed_models/model_data/transformers_cache')

        if not os.path.exists(cache+'deployed_models/model_data'):
            os.makedirs(cache+'deployed_models/model_data', exist_ok=True)

        if not os.path.exists(cache + 'deployed_models/model_data/albert_metadata'):
            os.makedirs(cache + 'deployed_models/model_data/albert_metadata/', exist_ok=True)

        if self.language_code in ['en', 'en_bio']:
            if len(os.listdir(cache + 'deployed_models/model_data/transformers_cache')) != 15:
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/en/distilbert_base_uncased_huggingface_files.zip',
                    cache + 'deployed_models/model_data/', bar=self.bar_thermometer
                )
                shutil.unpack_archive(cache + 'deployed_models/model_data' + '/distilbert_base_uncased_huggingface_files.zip',
                                      cache + 'deployed_models/model_data/transformers_cache/')
                
            if not os.path.exists(self.model_path):
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/{self.language_code}/punctuation_en_distilbert.nemo',
                    self.model_path, bar=self.bar_thermometer)
        else:
            if len(os.listdir(self.albert_metadata)) != 4:
                wget.download(
                    'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/albert_metadata/config.json',
                    self.albert_metadata + 'config.json', bar=self.bar_thermometer
                )
                wget.download(
                    'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/albert_metadata/pytorch_model.bin',
                    self.albert_metadata + 'pytorch_model.bin', bar=self.bar_thermometer
                )
                wget.download(
                    'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/albert_metadata/spiece.model',
                    self.albert_metadata + 'spiece.model', bar=self.bar_thermometer
                )
                wget.download(
                    'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/albert_metadata/spiece.vocab',
                    self.albert_metadata + 'spiece.vocab', bar=self.bar_thermometer
                )

            if not os.path.exists(self.model_path):
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/{self.language_code}/{self.language_code}.pt',
                    self.model_path, bar=self.bar_thermometer
                )
            if not os.path.exists(self.encoder_path):
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/{self.language_code}/{self.language_code}.json',
                    self.encoder_path, bar=self.bar_thermometer
                )
            if not os.path.exists(self.dict_map):
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/{self.language_code}/{self.language_code}_dict.json',
                    self.dict_map, bar=self.bar_thermometer
                )

    def load_model_parameters(self):
        self.download_model_data()
        with open(self.encoder_path) as label_encoder:
            train_encoder = json.load(label_encoder)
        with open(self.dict_map) as dict_map:
            punctuation_dict = json.load(dict_map)

        tokenizer = AlbertTokenizer.from_pretrained(self.albert_metadata)

        model = AlbertForTokenClassification.from_pretrained(self.albert_metadata,
                                                             num_labels=len(train_encoder),
                                                             output_attentions=False,
                                                             output_hidden_states=False)

        model = nn.DataParallel(model)
        checkpoint = torch.load(self.model_path, map_location=self.device)
        model.load_state_dict(checkpoint['state_dict'])
        model = model.module.to(self.device)

        model.eval()
        return tokenizer, model, train_encoder, punctuation_dict

    def get_tokens_and_labels_indices_from_text(self, text):

        tokenized_sentence = self.tokenizer.encode(text)
        input_ids = torch.tensor([tokenized_sentence]).to(self.device)
        with torch.no_grad():
            output = self.model(input_ids)
        label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
        return tokens, label_indices

    def punctuate_text_others_sentence(self, sentence):

        tokens, label_indices = self.get_tokens_and_labels_indices_from_text(sentence)

        new_tokens = []
        new_labels = []
        for i in range(1, len(tokens) - 1):
            if tokens[i].startswith("▁"):
                current_word = tokens[i][1:]
                new_labels.append(list(self.train_encoder.keys())[list(self.train_encoder.values()).index(label_indices[0][i])])
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
            full_text = full_text + word + self.punctuation_dict[punctuation]

        return full_text

    def punctuate_text_others_buffer(self, sentence, buffer_length=400):
        words = sentence.split()
        sentence_length = len(words)
        txt = ''
        beg_word = 0
        i = 1
        while sentence_length > buffer_length:
            sentence_segment = ' '.join(words[beg_word:i*buffer_length])
            txt = txt + self.punctuate_text_others_sentence(sentence_segment) + ' '
            full_stop_position = len(txt) - txt[::-1].find('.') - 1
            viram_position = len(txt) - txt[::-1].find('।') - 1
            question_mark_position = len(txt) - txt[::-1].find('?') - 1
            end_position = max([full_stop_position, viram_position, question_mark_position])
            beg_word = len(txt[:end_position].translate(str.maketrans('', '', string.punctuation + '।')).split())
            sentence_length = sentence_length - beg_word
            i = i + 1
            sentence = ' '.join(words[beg_word:])
        return txt + self.punctuate_text_others_sentence(sentence)

    def punctuate_text_others(self, text):
        sentences = []
        for sentence in text:
            sentences.append(self.punctuate_text_others_buffer(sentence))
        return sentences

    def punctuate_english_sentence(self, sentence, buffer_length=400):
        words = sentence.split()
        sentence_length = len(words)
        txt = ''
        beg_word = 0
        i = 1
        while sentence_length > buffer_length:
            sentence_segment = ' '.join(words[beg_word:i*buffer_length])
            txt = txt + self.model.add_punctuation_capitalization([sentence_segment])[0] + ' '
            full_stop_position = len(txt) - txt[::-1].find('.') - 1
            question_mark_position = len(txt) - txt[::-1].find('?') - 1
            end_position = full_stop_position if full_stop_position >= question_mark_position else question_mark_position
            beg_word = len(txt[:end_position].translate(str.maketrans('', '', string.punctuation + '।')).split())
            sentence_length = sentence_length - beg_word
            i = i + 1
            sentence = ' '.join(words[beg_word:])

        return txt + self.model.add_punctuation_capitalization([sentence])[0]

    def punctuate_text_english(self, text):
        sentences = []
        for sentence in text:
            sentences.append(self.punctuate_english_sentence(sentence))
        return sentences

    def punctuate_text(self, text):
        if self.language_code in ['en', 'en_bio']:
            return self.punctuate_text_english(text)
        elif self.language_code in ['hi', 'gu', 'te', 'mr', 'kn', 'pa', 'ta', 'bn', 'or', 'ml', 'as']:
            return self.punctuate_text_others(text)


if __name__ == "__main__":
    
    '''

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
        ['तू काय करत आहेस','साथीच्या आजारामुळे बंद झाल्यावर जवळजवळ दोन वर्षांनी अनेक देशांनी आता आंतरराष्ट्रीय पर्यटकांसाठी त्यांच्या सीमा पुन्हा उघडल्या आहेत']), sep='\n')


    '''
    english = Punctuation('en-bio')
    print(*english.punctuate_text(['how are you']))