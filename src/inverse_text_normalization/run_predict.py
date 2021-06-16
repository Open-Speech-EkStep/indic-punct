from inverse_text_normalization.hi.run_predict import inverse_normalize_text as hi_itn
from inverse_text_normalization.en.run_predict import inverse_normalize_text as en_itn


def inverse_normalize_text(text_list, lang):
    if lang == 'hi':
        return hi_itn(text_list)
    elif lang == 'en':
        return en_itn(text_list)
