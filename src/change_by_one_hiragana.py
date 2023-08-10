import urllib.request
import urllib.parse
import ast
import jaconv
import random
from config import hiragana_rules_dict
from config import KANJI_IDIOM_REGEX
import re
from janome.tokenizer import Tokenizer


def is_kanji_idiom(idiom: str) -> bool:
    tokenizer = Tokenizer()
    pos_tag_list = [
        token.part_of_speech.split(",")[0] for token in tokenizer.tokenize(idiom)
    ]
    flag = False
    if pos_tag_list == ["名詞"]:
        if re.match(KANJI_IDIOM_REGEX, idiom) is not None:
            if re.match(KANJI_IDIOM_REGEX, idiom).group() == idiom:
                flag = True
    return flag


def generate_furigana_candidate(hiragana_form: str):
    candidate_list = []
    L = [i for i in range(len(hiragana_form))]
    L_shuffled = random.sample(L, len(L))
    for idx in L_shuffled:
        hiragana = hiragana_form[idx]
        if hiragana_form[idx] not in hiragana_rules_dict.keys():
            continue
        zenhan = hiragana_form[:idx]
        kouhan = hiragana_form[idx + 1 :]
        mistype_list = (
            hiragana_rules_dict[hiragana][0] + hiragana_rules_dict[hiragana][1]
        )
        mistype_list = random.sample(mistype_list, len(mistype_list))
        for mistype_candidate in mistype_list:
            mistyped_hiragana = zenhan + mistype_candidate + kouhan
            candidate_list.append(mistyped_hiragana)
    return candidate_list


def suggest_homonym_list(hiragana_form: str) -> list[str]:
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
            homonym_list_excluded_original_form = [item for item in homonym_list[0][1]]
        else:  # those don't have any homonym or separated idioms are excluded
            homonym_list_excluded_original_form = []
        return homonym_list_excluded_original_form


def generate_goji_tweet_one_hira(surface, reading, noun_pos_shuffled):
    replaced_pos_id = -1
    mistaken_idiom = ""
    for noun_pos in noun_pos_shuffled:
        hiragana_form = jaconv.kata2hira(reading[noun_pos])
        furigana_candidate = generate_furigana_candidate(hiragana_form)
        print(furigana_candidate)
        for item in furigana_candidate:
            goji_candidate = suggest_homonym_list(hiragana_form=jaconv.kata2hira(item))
            goji_candidate = [
                candidate
                for candidate in goji_candidate
                if is_kanji_idiom(candidate) is True
            ]
            if len(goji_candidate) != 0:
                print(item, goji_candidate)
                replaced_pos_id = noun_pos
                mistaken_idiom = random.choice(goji_candidate)
                break
        if replaced_pos_id != -1:
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
