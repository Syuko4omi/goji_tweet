import urllib.request
import urllib.parse
import ast
import jaconv
import random
from config import KANJI_IDIOM_REGEX
import re


def is_kanji_idiom(idiom: str) -> bool:
    flag = False
    if re.match(KANJI_IDIOM_REGEX, idiom) is not None:
        if re.match(KANJI_IDIOM_REGEX, idiom).group() == idiom:
            flag = True
    return flag


def suggest_homonym_list(hiragana_form: str, original_kanji_form: str) -> list[str]:
    """
    Given the original kanji form and furigana as inputs, this func returns homonyms
    Input:
        hiragana_form: furigana (e.g. さんらん)
        original_kanji_form: the original idiom which is going to be rewritten (e.g. 散乱)
    Output:
        homonym_list_excluded_original_form: idiom list that has same furigana but other than original_kanji_form
    """

    url_encoded_form = urllib.parse.quote(
        hiragana_form, "utf-8"
    )  # we need to encode furigana, as it is used in URL
    query_url = (
        "http://www.google.com/transliterate?langpair=ja-Hira|ja&text={}".format(
            url_encoded_form
        )
    )
    request = urllib.request.Request(
        query_url
    )  # post request (https://www.google.co.jp/ime/cgiapi.html)

    with urllib.request.urlopen(request) as res:
        ret_string: str = res.readline().decode(
            "utf-8"
        )  # return should be one-line string
        homonym_list = ast.literal_eval(ret_string)  # convert str to list
        if len(homonym_list) == 1:
            homonym_list_excluded_original_form = [
                item for item in homonym_list[0][1] if item != original_kanji_form
            ]
        else:  # those don't have any homonym or separated idioms are excluded
            homonym_list_excluded_original_form = []
        return homonym_list_excluded_original_form


def generate_goji_tweet_hom(surface, reading, noun_pos_shuffled):
    replaced_pos_id = 0
    mistaken_idiom = ""
    for noun_pos in noun_pos_shuffled:
        goji_candidate = suggest_homonym_list(
            hiragana_form=jaconv.kata2hira(reading[noun_pos]),
            original_kanji_form=surface[noun_pos],
        )
        if len(goji_candidate) != 0:
            goji_candidate = [
                candidate
                for candidate in goji_candidate
                if is_kanji_idiom(candidate) is True
            ]
            replaced_pos_id = noun_pos
            mistaken_idiom = random.choice(goji_candidate)
            break
    after_tweet = ""
    for idx, item in enumerate(surface):
        if idx != replaced_pos_id:
            after_tweet += item
        else:
            after_tweet += mistaken_idiom
    return after_tweet


"""
if __name__ == "__main__":
    print(suggest_homonym_list("ヘンカン", "変換"))
"""
