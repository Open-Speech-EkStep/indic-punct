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

from inverse_text_normalization.asm.data_loader_utils import get_abs_path
from inverse_text_normalization.asm.graph_utils import NEMO_NOT_SPACE, GraphFst, convert_space

# from inverse_text_normalization.lang_params import LANG
# lang_data_path = f'inverse_text_normalization/data/{LANG}_data/'
lang_data_path = 'data/'

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False


class WordFst(GraphFst):
    """
    Finite state transducer for classifying word
        e.g. sleep -> tokens { name: "sleep" }
    """

    def __init__(self):
        super().__init__(name="word", kind="classify")

        exceptions = pynini.string_file(get_abs_path(lang_data_path+"sentence_boundary_exceptions.txt"))
        word = (
            pynutil.insert("name: \"")
            + (pynini.closure(pynutil.add_weight(NEMO_NOT_SPACE, weight=0.1), 1) | convert_space(exceptions))
            + pynutil.insert("\"")
        )
        self.fst = word.optimize()
