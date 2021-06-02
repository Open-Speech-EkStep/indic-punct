import torch
from transformers import AlbertForTokenClassification, AlbertTokenizer
import numpy as np
import json
import torch.nn as nn
from indicnlp.tokenize import indic_tokenize
import os
import wget
import sys


class Punctuation:
    def __init__(self, language_code):
        self.language_code = language_code
        self.model_path = 'model_data/' + self.language_code + '.pt'
        self.encoder_path = 'model_data/' + self.language_code + '.json'
        self.dict_map = 'model_data/' + self.language_code + '_dict.json'
        self.device = "cuda" if torch.cuda.is_available() else "cpu"


    def bar_thermometer(self, current, total, width=80):
        progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    def download_model_data(self):

        if not os.path.exists('model_data'):
            os.makedirs('model_data', exist_ok=True)

        if not os.path.exists(self.model_path):
            wget.download(
                'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/hi/hi.pt',
                self.model_path, bar=self.bar_thermometer)

        if not os.path.exists(self.encoder_path):
            wget.download(
                'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/hi/hi.json',
                self.encoder_path, bar=self.bar_thermometer)

        if not os.path.exists(self.dict_map):
            wget.download(
                'https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/hi/hi_dict.json',
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

        model.eval()
        return tokenizer, model

    def get_tokens_and_labels_indices_from_text(self, text):

        tokenizer, model = self.load_model_parameters()

        tokenized_sentence = tokenizer.encode(text)
        input_ids = torch.tensor([tokenized_sentence]).to(self.device)
        with torch.no_grad():
            output = model(input_ids)
        label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)
        tokens = tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
        return tokens, label_indices

    def punctuate_text(self, text):
        tokens, label_indices = self.get_tokens_and_labels_indices_from_text(text)
        with open(self.encoder_path) as label_encoder:
            train_encoder = json.load(label_encoder)

        with open(self.dict_map) as dict_map:
            punctuation_dict = json.load(dict_map)

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
        tokenized_text = indic_tokenize.trivial_tokenize_indic(text)

        if len(tokenized_text) == len(new_labels):
            full_text_tokens = tokenized_text
        else:
            full_text_tokens = new_tokens

        for word, punctuation in zip(full_text_tokens, new_labels):
            full_text = full_text + word + punctuation_dict[punctuation]
        return full_text


if __name__ == "__main__":
    print(Punctuation('hi').punctuate_text('नीरव मोदी को लंदन में पकड़ लिया गया था लेकिन मेहुल चोकसी लगातार एंटीगुआ में छिपा हुआ था मेहुल को भारत को सौंप दिया जाए'))
