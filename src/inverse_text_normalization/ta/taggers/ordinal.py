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

from inverse_text_normalization.ta.data_loader_utils import get_abs_path
from inverse_text_normalization.ta.graph_utils import NEMO_CHAR, GraphFst

# from inverse_text_normalization.lang_params import LANG
# data_path = f'inverse_text_normalization/data/{LANG}_data/'
data_path = 'data/'

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    PYNINI_AVAILABLE = False


class OrdinalFst(GraphFst):
    """
    Finite state transducer for classifying ordinal
        e.g. thirteenth -> ordinal { integer: "13" }

    Args:
        cardinal: Cardinal GraphFST
    """

    def __init__(self, cardinal: GraphFst):
        super().__init__(name="ordinal", kind="classify")

        cardinal_graph = cardinal.graph_no_exception
        graph_digit = pynini.string_file(get_abs_path(data_path+"ordinals/digit.tsv"))
        graph_teens = pynini.string_file(get_abs_path(data_path+"ordinals/teen.tsv"))
        # change to General UTF8
        graph = pynini.closure(NEMO_CHAR) + pynini.union(
            graph_digit, graph_teens, pynini.cross("tieth", "ty"), pynini.cross("th", "")
        )

        self.graph = graph @ cardinal_graph
        final_graph = pynutil.insert("integer: \"") + self.graph + pynutil.insert("\"")
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
