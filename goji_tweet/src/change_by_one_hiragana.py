import jaconv
import random
from goji_tweet.src.config import (
    HIRAGANA_RULES_DICT,
    is_kanji_idiom,
    suggest_homonym_list,
)


def generate_furigana_candidate(
    hiragana_form: str,
) -> list[str]:  # make possible mistypes list
    candidate_list = []
    replace_pos_list = [i for i in range(len(hiragana_form))]
    replace_pos_list_shuffled = random.sample(replace_pos_list, len(replace_pos_list))
    for idx in replace_pos_list_shuffled:
        cur_hiragana = hiragana_form[idx]
        if cur_hiragana not in HIRAGANA_RULES_DICT.keys():  # only 清音 will be replaced
            continue
        zenhan = hiragana_form[:idx]
        kouhan = hiragana_form[idx + 1 :]
        mistype_list = (
            HIRAGANA_RULES_DICT[cur_hiragana][0] + HIRAGANA_RULES_DICT[cur_hiragana][1]
        )
        mistype_list = random.sample(mistype_list, len(mistype_list))
        for mistype_candidate in mistype_list:
            mistyped_hiragana = zenhan + mistype_candidate + kouhan
            candidate_list.append(mistyped_hiragana)
    return candidate_list


def generate_goji_tweet_one_hira(surface, reading, noun_pos_shuffled):
    replaced_pos_id = -1
    mistaken_idiom = ""
    for noun_pos in noun_pos_shuffled:
        hiragana_form = jaconv.kata2hira(reading[noun_pos])
        furigana_candidate = generate_furigana_candidate(hiragana_form)
        for yomigana in furigana_candidate:
            goji_candidate = suggest_homonym_list(
                hiragana_form=jaconv.kata2hira(yomigana),
                original_kanji_form="",
                exclude_original_form=False,
            )
            goji_candidate = [
                candidate
                for candidate in goji_candidate
                if is_kanji_idiom(candidate) is True
            ]
            if len(goji_candidate) != 0:
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
