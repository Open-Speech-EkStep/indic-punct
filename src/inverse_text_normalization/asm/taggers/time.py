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
from inverse_text_normalization.asm.graph_utils import (
    GraphFst,
    convert_space,
    delete_extra_space,
    delete_space,
    insert_space,
)
# from inverse_text_normalization.lang_params import LANG
#
# lang_taggers = f'inverse_text_normalization.taggers.{LANG}_taggers'
# lang_data_path = f'inverse_text_normalization/data/{LANG}_data/'

lang_data_path = 'data/'
# lang_taggers = 'inverse_text_normalization.taggers.hi_taggers'
# exec(f"from {lang_taggers}.cardinal import CardinalFst")
from inverse_text_normalization.asm.taggers.cardinal import CardinalFst
# from taggers.cardinal import CardinalFst
from inverse_text_normalization.asm.utils import num_to_word

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False



class TimeFst(GraphFst):
    """
    Finite state transducer for classifying time
        e.g. twelve thirty -> time { hours: "12" minutes: "30" }
        e.g. twelve past one -> time { minutes: "12" hours: "1" }
        e.g. two o clock a m -> time { hours: "2" suffix: "a.m." }
    """

    def __init__(self):
        super().__init__(name="time", kind="classify")
        # hours, minutes, seconds, suffix, zone, style, speak_period

        suffix_graph = pynini.string_file(get_abs_path(lang_data_path+"time_suffix.tsv"))
        time_zone_graph = pynini.invert(pynini.string_file(get_abs_path(lang_data_path+"time_zone.tsv")))

        # only used for < 1000 thousand -> 0 weight
        cardinal = pynutil.add_weight(CardinalFst().graph_no_exception, weight=-0.7)

        labels_hour = [num_to_word(x) for x in range(0, 24)]
        labels_minute_single = [num_to_word(x) for x in range(1, 10)]
        labels_minute_double = [num_to_word(x) for x in range(10, 60)]

        graph_hour = pynini.union(*labels_hour) @ cardinal

        graph_minute_single = pynini.union(*labels_minute_single) @ cardinal
        graph_minute_double = pynini.union(*labels_minute_double) @ cardinal
        graph_minute_verbose = pynini.cross("half", "30") | pynini.cross("quarter", "15")
        oclock = pynini.cross(pynini.union("o' clock", "o clock", "o'clock", "oclock"), "")

        final_graph_hour = pynutil.insert("hours: \"") + graph_hour + pynutil.insert("\"")
        final_graph_minute = (
            pynutil.insert("minutes: \"")
            + (
                pynutil.insert("00")
                | oclock + pynutil.insert("00")
                | pynutil.delete("o") + delete_space + graph_minute_single
                | graph_minute_double
            )
            + pynutil.insert("\"")
        )
        final_suffix = pynutil.insert("suffix: \"") + convert_space(suffix_graph) + pynutil.insert("\"")
        final_suffix_optional = pynini.closure(delete_space + insert_space + final_suffix, 0, 1)
        final_time_zone_optional = pynini.closure(
            delete_space
            + insert_space
            + pynutil.insert("zone: \"")
            + convert_space(time_zone_graph)
            + pynutil.insert("\""),
            0,
            1,
        )

        # five o' clock
        # two o eight, two thiry five (am/pm)
        # two pm/am
        graph_hm = final_graph_hour + delete_extra_space + final_graph_minute
        # 10 past four, quarter past four, half past four
        graph_mh = (
            pynutil.insert("minutes: \"")
            + pynini.union(graph_minute_single, graph_minute_double, graph_minute_verbose)
            + pynutil.insert("\"")
            + delete_space
            + pynutil.delete("past")
            + delete_extra_space
            + final_graph_hour
        )
        final_graph = ((graph_hm | graph_mh) + final_suffix_optional + final_time_zone_optional).optimize()

        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
