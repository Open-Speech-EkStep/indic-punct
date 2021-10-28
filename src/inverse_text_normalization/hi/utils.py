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

_inflect = inflect.engine()

from inverse_text_normalization.hi.data_loader_utils import get_abs_path

data_path = 'data/'
def num_to_word(x: Union[str, int]):
    """
    converts integer to spoken representation

    Args
        x: integer

    Returns: spoken representation
    """
    if isinstance(x, int):
        x = str(x)
        # x = _inflect.number_to_words(str(x)).replace("-", " ").replace(",", "")
        with open(get_abs_path(data_path + "numbers/digit.tsv")) as f:
            lines = f.readlines()
        for line in lines:

            if line.split('\t')[1].strip() == x.strip():
                x = line.split('\t')[0].strip()

    return x
