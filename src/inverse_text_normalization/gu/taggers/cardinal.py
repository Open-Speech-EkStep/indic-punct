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


import pynini
from pynini.lib import pynutil, utf8

from inverse_text_normalization.gu.data_loader_utils import get_abs_path
from inverse_text_normalization.gu.graph_utils import (
    NEMO_DIGIT,
    NEMO_SIGMA,
    NEMO_SPACE,
    GraphFst,
    delete_space,
)
from inverse_text_normalization.gu.utils import num_to_word
# from inverse_text_normalization.lang_params import LANG
# data_path = f'data/{LANG}_data/'
data_path = 'data/'

def get_alternate_spellings(text):
    return

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False

class CardinalFst(GraphFst):
    """
    Finite state transducer for classifying cardinals
        e.g. minus twenty three -> cardinal { integer: "23" negative: "-" } }
    Numbers below thirteen are not converted. 
    """

    def __init__(self):
        super().__init__(name="cardinal", kind="classify")
        # integer, negative

        NEMO_CHAR = utf8.VALID_UTF8_CHAR
        NEMO_SIGMA = pynini.closure(NEMO_CHAR)
        NEMO_SPACE = " "
        NEMO_WHITE_SPACE = pynini.union(" ", "\t", "\n", "\r", u"\u00A0").optimize()
        NEMO_NOT_SPACE = pynini.difference(NEMO_CHAR, NEMO_WHITE_SPACE).optimize()
        # NEMO_NON_BREAKING_SPACE = u"\u00A0"

        hindi_digit_file = get_abs_path(data_path + 'numbers/digit.tsv')
        with open(hindi_digit_file) as f:
            digits = f.readlines()
        hindi_digits = ''.join([line.split()[-1] for line in digits])
        hindi_digits_with_zero = "0" + hindi_digits
        # print(f'hindi digits is {hindi_digits}')
        HINDI_DIGIT = pynini.union(*hindi_digits).optimize()
        HINDI_DIGIT_WITH_ZERO = pynini.union(*hindi_digits_with_zero).optimize()

        graph_zero = pynini.string_file(get_abs_path(data_path + "numbers/zero.tsv"))
        graph_tens = pynini.string_file(get_abs_path(data_path + "numbers/tens.tsv"))
        graph_digit = pynini.string_file(get_abs_path(data_path + "numbers/digit.tsv"))

        with open(get_abs_path(data_path + "numbers/hundred.tsv")) as f:
            hundred = f.read()
        with open(get_abs_path(data_path + "numbers/thousands.tsv")) as f:
            thousand = f.read()
        with open(get_abs_path(data_path + "numbers/lakh.tsv")) as f:
            lakh = f.read()

        with open(get_abs_path(data_path + "numbers/crore.tsv")) as f:
            crores = f.readlines()
        crore = crores[0]
        crore_alt = crores[1]

        # with open(get_abs_path(data_path + "numbers/hundred.tsv")) as f:
        #     hundred = f.read()

        graph_hundred = pynini.cross(hundred, "00")
        graph_crore = pynini.cross(crore, "0000000") | pynini.cross(crore_alt, "0000000")
        graph_lakh = pynini.cross(lakh, "00000")
        graph_thousand  = pynini.cross(thousand, "000")

        graph_hundred_component = pynini.union(graph_digit + delete_space + pynutil.delete(hundred) + delete_space,
                                               pynutil.insert("0"))
        graph_hundred_component += pynini.union(graph_tens, pynutil.insert("0") + (graph_digit | pynutil.insert("0")))

        # handling double digit hundreds like उन्निस सौ + digit/thousand/lakh/crore etc
        graph_hundred_component_prefix_tens = pynini.union(graph_tens + delete_space + pynutil.delete(hundred) + delete_space,)
                                                           # pynutil.insert("55"))
        graph_hundred_component_prefix_tens += pynini.union(graph_tens,
                                                            pynutil.insert("0") + (graph_digit | pynutil.insert("0")))

        # graph_hundred_component_at_least_one_none_zero_digit = graph_hundred_component @ (
        #         pynini.closure(HINDI_DIGIT_WITH_ZERO) + (HINDI_DIGIT_WITH_ZERO - "०") + pynini.closure(HINDI_DIGIT_WITH_ZERO)
        # )
        graph_hundred_component_non_hundred = pynini.union(graph_tens,
                                                           pynutil.insert("0") + (graph_digit | pynutil.insert("0")))

        graph_hundred_component = pynini.union(graph_hundred_component,
                                               graph_hundred_component_prefix_tens)

        graph_hundred_component_at_least_one_none_zero_digit = pynini.union(graph_hundred_component, graph_hundred_component_non_hundred)



        self.graph_hundred_component_at_least_one_none_zero_digit = (
            graph_hundred_component_at_least_one_none_zero_digit
        )

        graph_thousands_component = pynini.union(
            graph_hundred_component_at_least_one_none_zero_digit + delete_space + pynutil.delete(thousand),
            pynutil.insert("00", weight=0.1),
        )

        graph_lakhs_component = pynini.union(
            graph_hundred_component_at_least_one_none_zero_digit + delete_space + pynutil.delete(lakh),
            pynutil.insert("00", weight=0.1)
        )

        graph_crores_component = pynini.union(
            graph_hundred_component_at_least_one_none_zero_digit + delete_space + (pynutil.delete(crore) | pynutil.delete(crore_alt)),
            pynutil.insert("00", weight=0.1)
        )

        # fst = graph_thousands
        fst = pynini.union(
            graph_crores_component
            + delete_space
            + graph_lakhs_component
            + delete_space
            + graph_thousands_component
            + delete_space
            + graph_hundred_component,
            graph_zero,
        )

        fst_crore = fst+graph_crore # handles words like चार हज़ार करोड़
        fst_lakh = fst+graph_lakh # handles words like चार हज़ार लाख
        fst = pynini.union(fst, fst_crore, fst_lakh, graph_crore, graph_lakh, graph_thousand, graph_hundred)


        self.graph_no_exception = fst

        self.graph = (pynini.project(fst, "input")) @ fst

        optional_minus_graph = pynini.closure(
            pynutil.insert("negative: ") + pynini.cross("minus", "\"-\"") + NEMO_SPACE, 0, 1
        )

        final_graph = optional_minus_graph + pynutil.insert("integer: \"") + self.graph + pynutil.insert("\"")

        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
