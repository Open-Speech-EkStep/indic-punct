from inverse_text_normalization.hi.run_predict import inverse_normalize_text as hi_itn
from inverse_text_normalization.en.run_predict import inverse_normalize_text as en_itn
from inverse_text_normalization.gu.run_predict import inverse_normalize_text as gu_itn
from inverse_text_normalization.te.run_predict import inverse_normalize_text as te_itn
from inverse_text_normalization.mr.run_predict import inverse_normalize_text as mr_itn
from inverse_text_normalization.pa.run_predict import inverse_normalize_text as pa_itn
from inverse_text_normalization.ta.run_predict import inverse_normalize_text as ta_itn
from inverse_text_normalization.bn.run_predict import inverse_normalize_text as bn_itn
from inverse_text_normalization.ml.run_predict import inverse_normalize_text as ml_itn
from inverse_text_normalization.ori.run_predict import inverse_normalize_text as or_itn
from inverse_text_normalization.asm.run_predict import inverse_normalize_text as as_itn
from inverse_text_normalization.kn.run_predict import inverse_normalize_text as kn_itn

def format_numbers_with_commas(sent, lang):
    words = []
    for word in sent.split(' '):
        word_contains_digit = any(map(str.isdigit, word))
        currency_sign = ''
        if word_contains_digit:
            if len(word) > 4 and ':' not in word:
                pos_of_first_digit_in_word = list(map(str.isdigit, word)).index(True)

                if pos_of_first_digit_in_word != 0:  # word can be like $90,00,936.59
                    currency_sign = word[:pos_of_first_digit_in_word]
                    word = word[pos_of_first_digit_in_word:]

                s, *d = str(word).partition(".")
                # getting [num_before_decimal_point, decimal_point, num_after_decimal_point]
                if lang == 'hi':
                    # adding commas after every 2 digits after the last 3 digits
                    r = ",".join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
                else:
                    r = ",".join([s[x - 3:x] for x in range(-3, -len(s), -3)][::-1] + [s[-3:]])

                word = "".join([r] + d)  # joining decimal points as is

                if currency_sign:
                    word = currency_sign + word
                words.append(word)
            else:
                words.append(word)
        else:
            words.append(word)
    return ' '.join(words)


def inverse_normalize_text(text_list, lang):
    if lang == 'hi':
        itn_results = hi_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang=lang) for sent in itn_results]
        return itn_results_formatted
    elif lang in ['en', 'en_bio']:
        itn_results = en_itn(text_list)
        keywords_for_en_format = ["million", "billion", "trillion", "quadrillion", "quintillion", "sextillion"]
        itn_results_formatted = []
        for orig_sent, itn_sent in zip(text_list, itn_results):
            use_en_format = any(item in orig_sent.split(' ') for item in keywords_for_en_format)
            if use_en_format == 1:
                lang_format = 'en'
            else:
                lang_format = 'hi'
            itn_results_formatted.append(format_numbers_with_commas(sent=itn_sent, lang=lang_format))

        return itn_results_formatted
    elif lang == 'gu':
        itn_results = gu_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted

    elif lang == 'te':

        itn_results = te_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted

    elif lang == 'mr':

        itn_results = mr_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted

    elif lang == 'pa':

        itn_results = pa_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted

    elif lang == 'ta':

        itn_results = ta_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted

    elif lang == 'bn':

        itn_results = bn_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted

    elif lang == 'ml':

        itn_results = ml_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted

    elif lang == 'or':

        itn_results = or_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted

    elif lang == 'as':

        itn_results = as_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted

    
    elif lang == 'kn':

        itn_results = kn_itn(text_list)
        itn_results_formatted = [format_numbers_with_commas(sent=sent, lang='hi') for sent in itn_results]
        return itn_results_formatted
