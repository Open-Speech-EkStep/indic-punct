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

from inverse_text_normalization.bn.data_loader_utils import get_abs_path
from inverse_text_normalization.bn.graph_utils import (
    NEMO_DIGIT,
    NEMO_SIGMA,
    GraphFst,
    convert_space,
    delete_extra_space,
    delete_space,
    get_singulars,
    insert_space,
)

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False

# from inverse_text_normalization.lang_params import LANG
# lang_data_path = f'inverse_text_normalization/data/{LANG}_data/'
lang_data_path = 'data/'

class MoneyFst(GraphFst):
    """
    Finite state transducer for classifying money
        e.g. twelve dollars and five cents -> money { integer_part: "12" fractional_part: 05 currency: "$" }

    Args:
        cardinal: Cardinal GraphFST
        decimal: Decimal GraphFST
    """

    def __init__(self, cardinal: GraphFst, decimal: GraphFst):
        super().__init__(name="money", kind="classify")
        # quantity, integer_part, fractional_part, currency, style(depr)

        cardinal_graph = cardinal.graph_no_exception
        graph_decimal_final = decimal.final_graph_wo_negative

        unit = pynini.string_file(get_abs_path(lang_data_path+"currency.tsv"))
        unit_singular = pynini.invert(unit)
        unit_plural = get_singulars(unit_singular)

        graph_unit_singular = pynutil.insert("currency: \"") + convert_space(unit_singular) + pynutil.insert("\"")
        graph_unit_plural = pynutil.insert("currency: \"") + convert_space(unit_plural) + pynutil.insert("\"")

        add_leading_zero_to_double_digit = (NEMO_DIGIT + NEMO_DIGIT) | (pynutil.insert("0") + NEMO_DIGIT)
        # twelve dollars (and) fifty cents, zero cents
        cents_standalone = (
            pynutil.insert("fractional_part: \"")
            + pynini.union(
                pynutil.add_weight(((NEMO_SIGMA - "one") @ cardinal_graph), -0.7) @ add_leading_zero_to_double_digit
                + delete_space
                + pynutil.delete("cents"),
                pynini.cross("one", "01") + delete_space + pynutil.delete("cent"),
            )
            + pynutil.insert("\"")
        )

        optional_cents_standalone = pynini.closure(
            delete_space
            + pynini.closure(pynutil.delete("and") + delete_space, 0, 1)
            + insert_space
            + cents_standalone,
            0,
            1,
        )
        # twelve dollars fifty, only after integer
        optional_cents_suffix = pynini.closure(
            delete_extra_space
            + pynutil.insert("fractional_part: \"")
            + pynutil.add_weight(cardinal_graph @ add_leading_zero_to_double_digit, -0.7)
            + pynutil.insert("\""),
            0,
            1,
        )

        graph_integer = (
            pynutil.insert("integer_part: \"")
            + ((NEMO_SIGMA - "one") @ cardinal_graph)
            + pynutil.insert("\"")
            + delete_extra_space
            + (graph_unit_plural | graph_unit_singular)
            + (optional_cents_standalone | optional_cents_suffix)
        )
        graph_integer |= (
            pynutil.insert("integer_part: \"")
            + pynini.cross("one", "1")
            + pynutil.insert("\"")
            + delete_extra_space
            + graph_unit_singular
            + (optional_cents_standalone | optional_cents_suffix)
        )
        graph_decimal = graph_decimal_final + delete_extra_space + graph_unit_plural
        graph_decimal |= pynutil.insert("currency: \"$\" integer_part: \"0\" ") + cents_standalone
        final_graph = graph_integer | graph_decimal
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
