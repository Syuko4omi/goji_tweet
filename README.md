# goji_tweet
Super Funny Japanese Typo Tweet (Post) Generator

## Install
```
pip install git+https://github.com/Syuko4omi/goji_tweet
```

## How to use
We first need to prepare a sentence which we want to inject typo.  
The results may vary with each attempt.
### Automatically generate typo
```
from goji_tweet.src.create_goji_tweet import omakase_goji
original_tweet = "家の電灯ぶっ壊しちゃった…\n泣きたいです"
omakase_goji(original_tweet)
# 家の伝統ぶっ壊しちゃった…
# 泣きたいです
```

## Method
There are two ways for generating typo.
### Homonym (同音異義語)
Same pronunciation, but written in different ways
- 「散乱（さんらん）」vs「産卵（さんらん）」
- 「紫外線（しがいせん）」vs「市街戦（しがいせん）」

```
from goji_tweet.src.create_goji_tweet import goji_tweet_generator
original_sentence = "きええええぇえええ。。\n後30分でお出掛けなのに書類が散乱してるよぉおお😭😭😭"
goji_tweet_generator(original_sentence, "homonym")
# きええええぇえええ。。\n後30分でお出掛けなのに書類が産卵してるよぉおお😭😭😭
```

### Change one hiragana
Change one hiragana and convert it to different idiom
- 「からし」vs「彼氏（かれし）」
- 「花粉（かふん）」vs「古墳（こふん）」
- 「蜘蛛（くも）」vs「熊（くま）」

```
from goji_tweet.src.create_goji_tweet import goji_tweet_generator
original_sentence = "もしかして今日めちゃくちゃ花粉飛んでます？"
goji_tweet_generator(original_sentence, "mistype_one_hiragana")
# もしかして今日めちゃくちゃ古墳飛んでます？
```

## External resource
- Janome
    - Japanese morphological analyzer
- Google CGI API for Japanese Input
    - hiragana -> kanji converter
- jaconv
    - katakana -> hiragana converter