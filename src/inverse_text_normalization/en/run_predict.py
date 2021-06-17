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

from argparse import ArgumentParser
from typing import List

from inverse_text_normalization.en.inverse_normalize import INVERSE_NORMALIZERS

'''
Runs denormalization prediction on text data
'''


def load_file(file_path: str) -> List[str]:
    """
    Load given text file into list of string.

    Args: 
        file_path: file path

    Returns: flat list of string
    """
    res = []
    with open(file_path, 'r') as fp:
        for line in fp:
            if line:
                res.append(line.strip())
    return res


def write_file(file_path: str, data: List[str]):
    """
    Writes out list of string to file.

    Args:
        file_path: file path
        data: list of string
        
    """
    with open(file_path, 'w') as fp:
        for line in data:
            fp.write(line + '\n')


def indian_format(word, digits='0123456789'):
    word_contains_digit = any(map(str.isdigit, word))
    currency_sign = ''
    if word_contains_digit:
        pos_of_first_digit_in_word = list(map(str.isdigit, word)).index(True)

        if pos_of_first_digit_in_word != 0:  # word can be like $90,00,936.59
            currency_sign = word[:pos_of_first_digit_in_word]
            word = word[pos_of_first_digit_in_word:]

        s, *d = str(word).partition(".")
        # getting [num_before_decimal_point, decimal_point, num_after_decimal_point]
        r = ",".join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        # adding commas after every 2 digits after the last 3 digits
        word = "".join([r] + d)  # joining decimal points as is

        if currency_sign:
            word = currency_sign + word
        return word
    else:
        return word


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--input", help="input file path", required=True, type=str)
    parser.add_argument("--output", help="output file path", required=True, type=str)
    parser.add_argument("--verbose", help="print denormalization info. For debugging", action='store_true')
    parser.add_argument("--inverse_normalizer", default='nemo', type=str)
    return parser.parse_args()


def inverse_normalize_text(text_list, verbose=False):
    inverse_normalizer = INVERSE_NORMALIZERS['nemo']
    inverse_normalizer_prediction = inverse_normalizer(text_list, verbose=verbose)
    # comma_sep_num_list = []
    # for sent in inverse_normalizer_prediction:
    #     comma_sep_num_list.append(
    #         ' '.join([indian_format(word) for word in sent.split(' ')]))
    return inverse_normalizer_prediction


if __name__ == "__main__":
    args = parse_args()
    file_path = args.input
    inverse_normalizer = INVERSE_NORMALIZERS[args.inverse_normalizer]

    print("Loading data: " + file_path)
    data = load_file(file_path)

    print("- Data: " + str(len(data)) + " sentences")
    inverse_normalizer_prediction = inverse_normalizer(data, verbose=args.verbose)
    write_file(args.output, inverse_normalizer_prediction)
    print(f"- Normalized. Writing out to {args.output}")
