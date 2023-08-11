import random

import jaconv
from goji_tweet.src.config import suggest_homonym_list


def generate_goji_tweet_hom(
    surface: list[str], reading: list[str], noun_pos_shuffled: list[int]
) -> str:
    replaced_pos_id = -1  # noun id which should be replaced
    mistaken_idiom = ""

    for noun_pos in noun_pos_shuffled:
        goji_candidate = suggest_homonym_list(
            hiragana_form=jaconv.kata2hira(reading[noun_pos]),
            original_kanji_form=surface[noun_pos],
            exclude_original_form=True,
        )
        if len(goji_candidate) != 0:
            replaced_pos_id = noun_pos
            mistaken_idiom = goji_candidate[0]
            # mistaken_idiom = random.choice(goji_candidate)
            break

    goji_tweet = ""
    for idx, item in enumerate(surface):
        if idx != replaced_pos_id:
            goji_tweet += item
        else:
            goji_tweet += mistaken_idiom
    return goji_tweet
