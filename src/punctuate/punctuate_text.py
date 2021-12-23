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
import string
import shutil

class Punctuation:
    def __init__(self, language_code):
        self.language_code = language_code
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.transformers_cache = os.environ.get('TRANSFORMERS_CACHE')
        if self.language_code == 'en':
            #os.environ["TRANSFORMERS_CACHE"] = str('deployed_models/model_data/transformers_cache')
            self.model_path = 'deployed_models/model_data/punctuation_en_distilbert.nemo'
            self.download_model_data()
            print(f"Transformers Cache : {self.transformers_cache}")
            self.model = PunctuationCapitalizationModel.restore_from(self.model_path)
            self.model = self.model.to(self.device)
            
        else:
            self.model_path = 'deployed_models/model_data/' + self.language_code + '.pt'
            self.albert_metadata = 'deployed_models/model_data/albert_metadata/'
            self.encoder_path = 'deployed_models/model_data/' + self.language_code + '.json'
            self.dict_map = 'deployed_models/model_data/' + self.language_code + '_dict.json'
            self.tokenizer, self.model, self.train_encoder, self.punctuation_dict = self.load_model_parameters()

    def bar_thermometer(self, current, total, width=80):
        progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    def download_model_data(self):

        if self.language_code == 'en':
            
            if not os.path.exists(self.transformers_cache):
                print(f"Folder does not exist at {self.transformers_cache}")
                os.makedirs(self.transformers_cache)
                
            if not os.path.exists(self.transformers_cache):
                print(f'Downloading Transformers cache to {self.transformers_cache}')
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/en/distilbert_base_uncased_huggingface_files.zip',
                    'deployed_models/model_data/', bar=self.bar_thermometer
                )
                shutil.unpack_archive('deployed_models/model_data' + '/distilbert_base_uncased_huggingface_files.zip',
                                      self.transformers_cache)
                
            if not os.path.exists(self.model_path):
                print(f"Model does not exist at {self.model_path}")
                wget.download(
                    f'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/{self.language_code}/punctuation_en_distilbert.nemo',
                    self.model_path, bar=self.bar_thermometer)
        else:
            
            if not os.path.exists('deployed_models/model_data'):
                os.makedirs('deployed_models/model_data', exist_ok=True)

            if not os.path.exists('deployed_models/model_data/albert_metadata'):
                os.makedirs('deployed_models/model_data/albert_metadata/', exist_ok=True)
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
        if self.language_code == 'en':
            return self.punctuate_text_english(text)
        elif self.language_code in ['hi', 'gu', 'te', 'mr', 'kn', 'pa', 'ta', 'bn', 'or', 'ml', 'as']:
            return self.punctuate_text_others(text)


if __name__ == "__main__":
    english = Punctuation('en')
    print(english.punctuate_text(['how are you']))
