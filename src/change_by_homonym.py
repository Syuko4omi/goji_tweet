import jaconv
import random
from config import is_kanji_idiom
from config import suggest_homonym_list


def generate_goji_tweet_hom(surface, reading, noun_pos_shuffled):
    replaced_pos_id = -1
    mistaken_idiom = ""
    for noun_pos in noun_pos_shuffled:
        goji_candidate = suggest_homonym_list(
            hiragana_form=jaconv.kata2hira(reading[noun_pos]),
            original_kanji_form=surface[noun_pos],
            exclude_original_form=True,
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
