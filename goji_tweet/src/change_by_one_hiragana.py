import random

import jaconv
from goji_tweet.src.config import (
    HIRAGANA_RULES_DICT,
    suggest_homonym_list,
)


def generate_furigana_candidate(hiragana_form: str) -> list[str]:
    # make possible mistypes list according to mistype rules
    candidate_furigana_list = []
    replace_pos_list = [i for i in range(len(hiragana_form))]
    replace_pos_list_shuffled = random.sample(replace_pos_list, len(replace_pos_list))

    for idx in replace_pos_list_shuffled:
        cur_hiragana = hiragana_form[idx]  # e.g. idx==2 -> へん「か」ん
        if cur_hiragana not in HIRAGANA_RULES_DICT.keys():  # only 清音 will be replaced
            continue
        zenhan = hiragana_form[:idx]  # e.g. 「へん」かん
        kouhan = hiragana_form[idx + 1 :]  # e.g. へんか「ん」
        mistype_list = (
            HIRAGANA_RULES_DICT[cur_hiragana][0] + HIRAGANA_RULES_DICT[cur_hiragana][1]
        )
        mistype_list_shuffled = random.sample(mistype_list, len(mistype_list))

        for mistype_candidate in mistype_list_shuffled:
            mistyped_hiragana = zenhan + mistype_candidate + kouhan  # e.g. へんあん, へんさん
            candidate_furigana_list.append(mistyped_hiragana)
    return candidate_furigana_list


def generate_goji_tweet_one_hira(
    surface: list[str], reading: list[str], noun_pos_shuffled: list[int]
) -> str:
    replaced_pos_id = -1  # noun id which should be replaced
    mistaken_idiom = ""

    for noun_pos in noun_pos_shuffled:
        # reading[noun_pos] is katakana and to send request we should convert it to hiragana
        hiragana_form = jaconv.kata2hira(reading[noun_pos])
        candidate_furigana_list = generate_furigana_candidate(hiragana_form)
        for yomigana in candidate_furigana_list:
            goji_candidate = suggest_homonym_list(
                hiragana_form=yomigana,
                original_kanji_form="",
                exclude_original_form=False,
            )
            if len(goji_candidate) != 0:
                replaced_pos_id = noun_pos
                mistaken_idiom = goji_candidate[0]
                # mistaken_idiom = random.choice(goji_candidate)
                # usually goji_candidate[0] provides frequently used idiom, so we need not to randomly choice other idioms
                break
        if replaced_pos_id != -1:
            break

    goji_tweet = ""
    for idx, item in enumerate(surface):
        if idx != replaced_pos_id:
            goji_tweet += item
        else:
            goji_tweet += mistaken_idiom
    return goji_tweet
