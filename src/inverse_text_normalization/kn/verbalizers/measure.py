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

from inverse_text_normalization.kn.graph_utils import NEMO_CHAR, GraphFst, delete_space
from inverse_text_normalization.kn.verbalizers.cardinal import CardinalFst
from inverse_text_normalization.kn.verbalizers.decimal import DecimalFst

try:
    import pynini
    from pynini.lib import pynutil

    decimal = DecimalFst()
    cardinal = CardinalFst()

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    # Add placeholders
    decimal = None
    cardinal = None

    PYNINI_AVAILABLE = False


class MeasureFst(GraphFst):
    """
    Finite state transducer for verbalizing measure, 
        e.g. tokens { measure { negative: "true" cardinal { integer: "12" } units: "kg" } } -> -12 kg
    """

    def __init__(self):
        super().__init__(name="measure", kind="verbalize")
        optional_sign = pynini.closure(pynini.cross("negative: \"true\"", "-"), 0, 1)
        unit = (
            pynutil.delete("units:")
            + delete_space
            + pynutil.delete("\"")
            + pynini.closure(NEMO_CHAR - " ", 1)
            + pynutil.delete("\"")
            + delete_space
        )
        graph_decimal = (
            pynutil.delete("decimal {")
            + delete_space
            + optional_sign
            + delete_space
            + decimal.numbers
            + delete_space
            + pynutil.delete("}")
        )
        graph_cardinal = (
            pynutil.delete("cardinal {")
            + delete_space
            + optional_sign
            + delete_space
            + cardinal.numbers
            + delete_space
            + pynutil.delete("}")
        )
        graph = (graph_cardinal | graph_decimal) + delete_space + pynutil.insert(" ") + unit
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()
