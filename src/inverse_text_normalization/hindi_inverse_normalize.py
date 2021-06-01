import pynini
from pynini.lib import pynutil, utf8

from inverse_text_normalization.graph_utils import delete_space


def remove_starting_zeros(word, hindi_digits_with_zero):
    if word[0] in hindi_digits_with_zero and len(word) > 1:
        first_non_zero_num = min([pos for pos, word in enumerate(list(word)) if word != "०"])
        word = word[first_non_zero_num:]

    return word


if __name__ == '__main__':

    NEMO_CHAR = utf8.VALID_UTF8_CHAR
    NEMO_SIGMA = pynini.closure(NEMO_CHAR)
    NEMO_SPACE = " "
    NEMO_WHITE_SPACE = pynini.union(" ", "\t", "\n", "\r", u"\u00A0").optimize()
    NEMO_NOT_SPACE = pynini.difference(NEMO_CHAR, NEMO_WHITE_SPACE).optimize()
    # NEMO_NON_BREAKING_SPACE = u"\u00A0"

    hindi_digit_file = './data/numbers/digit.tsv'
    with open(hindi_digit_file) as f:
        digits = f.readlines()
    hindi_digits = ''.join([line.split()[-1] for line in digits])
    hindi_digits_with_zero = "०" + hindi_digits
    print(f'hindi digits is {hindi_digits}')
    HINDI_DIGIT = pynini.union(*hindi_digits).optimize()
    HINDI_DIGIT_WITH_ZERO = pynini.union(*hindi_digits_with_zero).optimize()

    graph_zero = pynini.string_file("./data/numbers/zero.tsv")
    graph_digit = pynini.string_file("./data/numbers/digit.tsv")
    graph_tens = pynini.string_file("./data/numbers/hindi_tens.tsv")
    # exceptions = pynini.string_file("./data/sentence_boundary_exceptions.txt")

    graph_hundred = pynini.cross("सौ", "")

    graph_hundred_component = pynini.union(graph_digit + delete_space + graph_hundred, pynutil.insert("०"))
    graph_hundred_component += delete_space
    graph_hundred_component += pynini.union(graph_tens, pynutil.insert("०") + (graph_digit | pynutil.insert("०")))
    # graph_hundred_component += pynini.union((graph_tens | pynutil.insert("०")) + delete_space + (graph_digit | pynutil.insert("०")),)

    graph_hundred_component_at_least_one_none_zero_digit = graph_hundred_component @ (
            pynini.closure(HINDI_DIGIT) + (HINDI_DIGIT - "०") + pynini.closure(HINDI_DIGIT)
    )

    graph_thousands = pynini.union(
        graph_hundred_component + delete_space + pynutil.delete("हज़ार"),
        pynutil.insert("०००", weight=0.1)
    )

    # fst = graph_thousands
    fst = pynini.union(
        graph_thousands
        + delete_space
        + graph_hundred_component,
        graph_zero,
    )
    # fst = fst @ pynini.union(
    #     pynutil.delete(pynini.closure("०")) + pynini.difference(HINDI_DIGIT_WITH_ZERO, "०") + pynini.closure(HINDI_DIGIT_WITH_ZERO), "०"
    # )

    word = pynini.closure(pynutil.add_weight(NEMO_NOT_SPACE, weight=0.1), 1)

    word_fst = word.optimize()

    fst = pynini.cdrewrite(fst, "", "", NEMO_SIGMA)
    fst = fst.optimize()

    final_graph = (
            pynutil.add_weight(fst, 1.1)
            | pynutil.add_weight(word_fst, 100)
    )
    final_graph = final_graph.optimize()

    file_path = './sample_input.txt'

    with open(file_path) as f:
        lines = f.readlines()

    print("Printing output lines \n")
    for line in lines:
        s = pynini.escape(line.strip())

        ans = s @ final_graph
        # print("***********")
        # print("ans is \n")
        # print(ans)
        astr = pynini.shortestpath(ans).string()

        astr = ' '.join([remove_starting_zeros(word, hindi_digits_with_zero) for word in astr.split()])
        print(f'Original: {s} Output: {astr}')
