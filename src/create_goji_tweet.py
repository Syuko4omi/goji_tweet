from change_by_homonym import suggest_homonym_list
from janome.tokenizer import Tokenizer
import random
import re
import jaconv


if __name__ == "__main__":
    tokenizer = Tokenizer()
    original_tweet = "きええええぇえええ。。\n後30分でお出掛けなのに書類が散乱してるよぉおお😭😭😭"
    surface = [token.surface for token in tokenizer.tokenize(original_tweet)]
    pos_tag_list = [
        token.part_of_speech.split(",")[0]
        for token in tokenizer.tokenize(original_tweet)
    ]
    reading = [token.reading for token in tokenizer.tokenize(original_tweet)]
    noun_pos = [id for id, item in enumerate(pos_tag_list) if item == "名詞"]
    print(surface)
    print(pos_tag_list)
    print(noun_pos)
    regex = "[一-龥]+"
    candidate_noun_pos = [
        idx
        for idx in noun_pos
        if re.match(regex, surface[idx]) is not None
        and re.match(regex, surface[idx]).group() == surface[idx]
    ]
    print(candidate_noun_pos)
    noun_pos_shuffled = random.sample(candidate_noun_pos, len(candidate_noun_pos))
    hogehogehoge_id = 0
    hogehogehoge = ""
    for noun_pos in noun_pos_shuffled:
        print(jaconv.kata2hira(reading[noun_pos]), surface[noun_pos])
        goji_candidate = suggest_homonym_list(
            hiragana_form=jaconv.kata2hira(reading[noun_pos]),
            original_kanji_form=surface[noun_pos],
        )
        if len(goji_candidate) != 0:
            print(goji_candidate)
            hogehogehoge_id = noun_pos
            hogehogehoge = random.choice(goji_candidate)
            break
    after_tweet = ""
    for idx, item in enumerate(surface):
        if idx != hogehogehoge_id:
            after_tweet += item
        else:
            after_tweet += hogehogehoge
    print(after_tweet)
