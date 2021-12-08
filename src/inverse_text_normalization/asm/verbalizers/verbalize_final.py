# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright 2015 and onwards Google, Inc.
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

from inverse_text_normalization.asm.graph_utils import GraphFst, delete_extra_space, delete_space
from inverse_text_normalization.asm.verbalizers.punctuation import PunctuationFst
from inverse_text_normalization.asm.verbalizers.verbalize import VerbalizeFst
from inverse_text_normalization.asm.verbalizers.word import WordFst

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False


class VerbalizeFinalFst(GraphFst):
    """
    Finite state transducer that verbalizes an entire sentence
        e.g. tokens { name: "its" } tokens { time { hours: "12" minutes: "30" } } tokens { name: "now" } tokens { name: "." pause_length: "PAUSE_LONG phrase_break: true type: PUNCT" }
            -> its 12:30 now .
    """

    def __init__(self):
        super().__init__(name="verbalize_final", kind="verbalize")
        verbalize = VerbalizeFst().fst
        punct = PunctuationFst().fst
        word = WordFst().fst
        types = verbalize | word | punct
        graph = (
            pynutil.delete("tokens")
            + delete_space
            + pynutil.delete("{")
            + delete_space
            + types
            + delete_space
            + pynutil.delete("}")
        )
        graph = delete_space + pynini.closure(graph + delete_extra_space) + graph + delete_space
        self.fst = graph
