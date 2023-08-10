from change_by_homonym import suggest_homonym_list
from janome.tokenizer import Tokenizer
import random
import re
import jaconv
from config import KANJI_IDIOM_REGEX


def is_kanji_idiom(idiom: str) -> bool:
    flag = False
    if re.match(KANJI_IDIOM_REGEX, idiom) is not None:
        if re.match(KANJI_IDIOM_REGEX, idiom).group() == idiom:
            flag = True
    return flag


def tweet_preprocesser(original_tweet: str):
    tokenizer = Tokenizer()
    surface = [token.surface for token in tokenizer.tokenize(original_tweet)]
    pos_tag_list = [
        token.part_of_speech.split(",")[0]
        for token in tokenizer.tokenize(original_tweet)
    ]
    reading = [token.reading for token in tokenizer.tokenize(original_tweet)]
    noun_pos = [id for id, item in enumerate(pos_tag_list) if item == "名詞"]
    candidate_noun_pos = [
        idx for idx in noun_pos if is_kanji_idiom(surface[idx]) is True
    ]  # select noun which consists of only kanji
    return surface, reading, candidate_noun_pos


def goji_tweet_generator(original_tweet: str, goji_type: str) -> str:
    surface, reading, candidate_noun_pos = tweet_preprocesser(original_tweet)
    noun_pos_shuffled = random.sample(candidate_noun_pos, len(candidate_noun_pos))
    replaced_pos_id = 0
    mistaken_idiom = ""
    for noun_pos in noun_pos_shuffled:
        if goji_type == "homonym":
            goji_candidate = suggest_homonym_list(
                hiragana_form=jaconv.kata2hira(reading[noun_pos]),
                original_kanji_form=surface[noun_pos],
            )
            if len(goji_candidate) != 0:
                print(goji_candidate)
                goji_candidate = [
                    candidate
                    for candidate in goji_candidate
                    if is_kanji_idiom(candidate) is True
                ]
                print(goji_candidate)
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


if __name__ == "__main__":
    tokenizer = Tokenizer()
    original_tweet = "きええええぇえええ。。\n後30分でお出掛けなのに書類が散乱してるよぉおお😭😭😭"
    goji_tweet = goji_tweet_generator(original_tweet, "homonym")
    print(goji_tweet)
