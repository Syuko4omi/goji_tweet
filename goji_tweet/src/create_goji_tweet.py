import random

from goji_tweet.src.change_by_homonym import generate_goji_tweet_hom
from goji_tweet.src.change_by_one_hiragana import generate_goji_tweet_one_hira
from goji_tweet.src.config import is_kanji_idiom
from janome.tokenizer import Tokenizer


def tweet_preprocesser(original_tweet: str) -> tuple[list[str], list[str], list[int]]:
    tokenizer = Tokenizer()

    # prepare surface, pos, reading
    surface_list = [token.surface for token in tokenizer.tokenize(original_tweet)]
    pos_tag_list = [
        token.part_of_speech.split(",")[0]
        for token in tokenizer.tokenize(original_tweet)
    ]
    reading_list = [token.reading for token in tokenizer.tokenize(original_tweet)]

    # select noun idx which consists of only kanji
    candidate_noun_pos_list = [
        idx
        for idx, item in enumerate(pos_tag_list)
        if item == "名詞" and is_kanji_idiom(surface_list[idx]) is True
    ]

    return surface_list, reading_list, candidate_noun_pos_list


def goji_tweet_generator(original_tweet: str, goji_type: str) -> str:
    surface, reading, candidate_noun_pos = tweet_preprocesser(original_tweet)
    # randomly select priority which noun should be replaced
    noun_pos_shuffled = random.sample(candidate_noun_pos, len(candidate_noun_pos))

    if goji_type == "homonym":
        after_tweet = generate_goji_tweet_hom(surface, reading, noun_pos_shuffled)
    else:
        after_tweet = generate_goji_tweet_one_hira(surface, reading, noun_pos_shuffled)
    return after_tweet


def omakase_goji(original_tweet: str) -> str:
    """
    Randomly decide which word should be mistaken and which type of mistake should be applied, and returns mistaken sentence

    Input:
        original_tweet: sentence that contains no mistake
    Output:
        goji_tweet: modified original sentence that has one mistake (goji)
    """
    if random.random() < 0.5:
        goji_tweet = goji_tweet_generator(original_tweet, "homonym")
    else:
        goji_tweet = goji_tweet_generator(original_tweet, "mistype_one_hiragana")
    return goji_tweet
