# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import csv
import json
import os
from collections import defaultdict, namedtuple
from typing import Dict, List, Optional, Set, Tuple

EOS_TYPE = "EOS"
PUNCT_TYPE = "PUNCT"
PLAIN_TYPE = "PLAIN"
Instance = namedtuple('Instance', 'token_type un_normalized normalized')
known_types = [
    "PLAIN",
    "DATE",
    "CARDINAL",
    "LETTERS",
    "VERBATIM",
    "MEASURE",
    "DECIMAL",
    "ORDINAL",
    "DIGIT",
    "MONEY",
    "TELEPHONE",
    "ELECTRONIC",
    "FRACTION",
    "TIME",
    "ADDRESS",
]


def load_kaggle_text_norm_file(file_path: str) -> List[Instance]:
    """
    https://www.kaggle.com/richardwilliamsproat/text-normalization-for-english-russian-and-polish
    Loads text file in the Kaggle Google text normalization file format: <semiotic class>\t<unnormalized text>\t<`self` if trivial class or normalized text>
    E.g. 
    PLAIN   Brillantaisia   <self>
    PLAIN   is      <self>
    PLAIN   a       <self>
    PLAIN   genus   <self>
    PLAIN   of      <self>
    PLAIN   plant   <self>
    PLAIN   in      <self>
    PLAIN   family  <self>
    PLAIN   Acanthaceae     <self>
    PUNCT   .       sil
    <eos>   <eos>

    Args:
        file_path: file path to text file

    Returns: flat list of instances 
    """
    res = []
    with open(file_path, 'r') as fp:
        for line in fp:
            parts = line.strip().split("\t")
            if parts[0] == "<eos>":
                res.append(Instance(token_type=EOS_TYPE, un_normalized="", normalized=""))
            else:
                l_type, l_token, l_normalized = parts
                l_token = l_token.lower()
                l_normalized = l_normalized.lower()

                if l_type == PLAIN_TYPE:
                    res.append(Instance(token_type=l_type, un_normalized=l_token, normalized=l_token))
                elif l_type != PUNCT_TYPE:
                    res.append(Instance(token_type=l_type, un_normalized=l_token, normalized=l_normalized))
    return res


def load_files(file_paths: List[str], load_func=load_kaggle_text_norm_file) -> List[Instance]:
    """
    Load given list of text files using the `load_func` function.

    Args: 
        file_paths: list of file paths
        load_func: loading function

    Returns: flat list of instances
    """
    res = []
    for file_path in file_paths:
        res.extend(load_func(file_path=file_path))
    return res


def clean_generic(text: str) -> str:
    """
    Cleans text without affecting semiotic classes.

    Args:
        text: string

    Returns: cleaned string
    """
    text = text.strip()
    text = text.lower()
    return text


def evaluate(preds: List[str], labels: List[str], input: Optional[List[str]] = None, verbose: bool = True) -> float:
    """
    Evaluates accuracy given predictions and labels. 

    Args:
        preds: predictions
        labels: labels
        input: optional, only needed for verbosity
        verbose: if true prints [input], golden labels and predictions

    Returns accuracy
    """
    acc = 0
    nums = len(preds)
    for i in range(nums):
        pred_norm = clean_generic(preds[i])
        label_norm = clean_generic(labels[i])
        if pred_norm == label_norm:
            acc = acc + 1
        else:
            if input:
                print(f"inpu: {json.dumps(input[i])}")
            print(f"gold: {json.dumps(label_norm)}")
            print(f"pred: {json.dumps(pred_norm)}")
    return acc / nums


def training_data_to_tokens(
    data: List[Instance], category: Optional[str] = None
) -> Dict[str, Tuple[List[str], List[str]]]:
    """
    Filters the instance list by category if provided and converts it into a map from token type to list of un_normalized and normalized strings

    Args:
        data: list of instances
        category: optional semiotic class category name

    Returns Dict: token type -> (list of un_normalized strings, list of normalized strings)
    """
    result = defaultdict(lambda: ([], []))
    for instance in data:
        if instance.token_type != EOS_TYPE:
            if category is None or instance.token_type == category:
                result[instance.token_type][0].append(instance.un_normalized)
                result[instance.token_type][1].append(instance.normalized)
    return result


def training_data_to_sentences(data: List[Instance]) -> Tuple[List[str], List[str], List[Set[str]]]:
    """
    Takes instance list, creates list of sentences split by EOS_Token
    Args:
        data: list of instances
    Returns (list of unnormalized sentences, list of normalized sentences, list of sets of categories in a sentence)
    """
    # split data at EOS boundaries
    sentences = []
    sentence = []
    categories = []
    sentence_categories = set()

    for instance in data:
        if instance.token_type == EOS_TYPE:
            sentences.append(sentence)
            sentence = []
            categories.append(sentence_categories)
            sentence_categories = set()
        else:
            sentence.append(instance)
            sentence_categories.update([instance.token_type])
    un_normalized = [" ".join([instance.un_normalized for instance in sentence]) for sentence in sentences]
    normalized = [" ".join([instance.normalized for instance in sentence]) for sentence in sentences]
    return un_normalized, normalized, categories


def load_labels(rel_path):
    """
    loads relative path file as dictionary

    Args:
        rel_path: relative path

    Returns dictionary of mappings
    """
    label_tsv = open(get_abs_path(rel_path))
    labels = list(csv.reader(label_tsv, delimiter="\t"))
    return labels


def get_abs_path(rel_path):
    """
    Get absolute path

    Args:
        rel_path: relative path to this file
        
    Returns absolute path
    """
    return os.path.dirname(os.path.abspath(__file__)) + '/' + rel_path
