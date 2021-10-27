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

from typing import Union

import inflect
from inverse_text_normalization.pa.data_loader_utils import get_abs_path
_inflect = inflect.engine()

data_path = 'data/numbers/'
def num_to_word(x: Union[str, int]):
    """
    converts integer to spoken representation

    Args
        x: integer

    Returns: spoken representation
    """
    if isinstance(x, int):
        x = str(x)
        x = _inflect.number_to_words(str(x)).replace("-", " ").replace(",", "")
    return x

'''
def num_to_word(x: Union[str, int]):
    """
    converts integer to spoken representation

    Args
        x: integer

    Returns: spoken representation 
    """
    d={}
    if isinstance(x, int):
        x = str(x)
        with open(get_abs_path(data_path+"digit.tsv"),encoding="UTF-8") as f:
            line = f.readlines()
        word_list = [w.strip().split("\t")[0] for w in line]
        num_list = [num.strip().split("\t")[1] for num in line]
        ix = num_list.index(x)

        # d={item[1]:item[0] for item in word}
        # x = _inflect.number_to_words(str(x)).replace("-", " ").replace(",", "")
    return word_list[ix]
'''