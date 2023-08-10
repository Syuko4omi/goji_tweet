from janome.tokenizer import Tokenizer
import random
from change_by_homonym import generate_goji_tweet_hom
from change_by_one_hiragana import generate_goji_tweet_one_hira
from config import is_kanji_idiom


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
    if goji_type == "homonym":
        after_tweet = generate_goji_tweet_hom(surface, reading, noun_pos_shuffled)
    else:
        after_tweet = generate_goji_tweet_one_hira(surface, reading, noun_pos_shuffled)
    return after_tweet


if __name__ == "__main__":
    tokenizer = Tokenizer()
    original_tweet = "きええええぇえええ。。\n後30分でお出掛けなのに書類が散乱してるよぉおお😭😭😭"
    goji_tweet = goji_tweet_generator(original_tweet, "homonym")
    # goji_tweet = goji_tweet_generator(original_tweet, "hiragana")
    print(goji_tweet)
