import ast
import re
import urllib.parse
import urllib.request

from janome.tokenizer import Tokenizer

KANJI_IDIOM_REGEX = "[一-龥]+"
HIRAGANA_RULES_DICT = {
    "あ": [["い", "う", "え", "お"], ["か", "た"]],
    "い": [["あ", "う", "え", "お"], ["き", "ち"]],
    "う": [["あ", "い", "え", "お"], ["く", "つ"]],
    "え": [["あ", "い", "う", "お"], ["け", "て"]],
    "お": [["あ", "い", "う", "え"], ["こ", "と"]],
    "か": [["き", "く", "け", "こ"], ["あ", "さ", "な"]],
    "き": [["か", "く", "け", "こ"], ["い", "し", "に"]],
    "く": [["か", "き", "け", "こ"], ["う", "す", "ぬ"]],
    "け": [["か", "き", "く", "こ"], ["え", "せ", "ね"]],
    "こ": [["か", "き", "く", "け"], ["お", "そ", "の"]],
    "さ": [["し", "す", "せ", "そ"], ["か", "は"]],
    "し": [["さ", "す", "せ", "そ"], ["き", "ひ"]],
    "す": [["さ", "し", "せ", "そ"], ["く", "ふ"]],
    "せ": [["さ", "し", "す", "そ"], ["け", "へ"]],
    "そ": [["さ", "し", "す", "せ"], ["こ", "ほ"]],
    "た": [["ち", "つ", "て", "と"], ["あ", "な", "ま"]],
    "ち": [["た", "つ", "て", "と"], ["い", "に", "み"]],
    "つ": [["た", "ち", "て", "と"], ["う", "ぬ", "む"]],
    "て": [["た", "ち", "つ", "と"], ["え", "ね", "め"]],
    "と": [["た", "ち", "つ", "て"], ["お", "の", "も"]],
    "な": [["に", "ぬ", "ね", "の"], ["か", "た", "は", "や"]],
    "に": [["な", "ぬ", "ね", "の"], ["き", "ち", "ひ"]],
    "ぬ": [["な", "に", "ね", "の"], ["く", "つ", "ふ", "ゆ"]],
    "ね": [["な", "に", "ぬ", "の"], ["け", "て", "へ"]],
    "の": [["な", "に", "ぬ", "ね"], ["こ", "と", "ほ", "よ"]],
    "は": [["ひ", "ふ", "へ", "ほ"], ["さ", "な", "ら"]],
    "ひ": [["は", "ふ", "へ", "ほ"], ["し", "に", "り"]],
    "ふ": [["は", "ひ", "へ", "ほ"], ["す", "ぬ", "る"]],
    "へ": [["は", "ひ", "ふ", "ほ"], ["せ", "ね", "れ"]],
    "ほ": [["は", "ひ", "ふ", "へ"], ["そ", "の", "ろ"]],
    "ま": [["み", "む", "め", "も"], ["た", "や"]],
    "み": [["ま", "む", "め", "も"], ["ち"]],
    "む": [["ま", "み", "め", "も"], ["つ", "ゆ"]],
    "め": [["ま", "み", "む", "も"], ["て"]],
    "も": [["ま", "み", "む", "め"], ["と", "よ"]],
    "や": [["ゆ", "よ"], ["な", "ま", "ら"]],
    "ゆ": [["や", "よ"], ["ぬ", "む", "る"]],
    "よ": [["や", "ゆ"], ["の", "も", "ろ"]],
    "ら": [["り", "る", "れ", "ろ"], ["は", "や"]],
    "り": [["ら", "る", "れ", "ろ"], ["ひ"]],
    "る": [["ら", "り", "れ", "ろ"], ["ふ", "ゆ"]],
    "れ": [["ら", "り", "る", "ろ"], ["へ"]],
    "ろ": [["ら", "り", "る", "れ"], ["ほ", "よ"]],
    "わ": [["を", "ん"], ["や"]],
    "を": [["わ", "ん"], [""]],
    "ん": [["わ", "を"], ["ゆ"]],
}


def is_kanji_idiom(idiom: str) -> bool:
    tokenizer = Tokenizer()
    pos_tag_list = [
        token.part_of_speech.split(",")[0] for token in tokenizer.tokenize(idiom)
    ]
    surface = [token.surface for token in tokenizer.tokenize(idiom)]

    flag = True
    for idx, word in enumerate(surface):
        # if the word is not noun or the word does not contain any kanji
        if pos_tag_list[idx] != "名詞" or re.match(KANJI_IDIOM_REGEX, word) is None:
            flag = False
            break
        else:
            # if some chars in the word are not kanji
            if re.match(KANJI_IDIOM_REGEX, word).group() != word:
                flag = False
                break
    return flag
    """
    flag = False
    if pos_tag_list == ["名詞"]:
        if re.match(KANJI_IDIOM_REGEX, idiom) is not None:
            if re.match(KANJI_IDIOM_REGEX, idiom).group() == idiom:
                flag = True
    return flag
    """


def suggest_homonym_list(
    hiragana_form: str, original_kanji_form: str, exclude_original_form: bool
) -> list[str]:
    """
    Given the original kanji form and furigana as inputs, this func returns homonyms
    Input:
        hiragana_form: furigana (e.g. さんらん)
        original_kanji_form: the original idiom which is going to be rewritten (e.g. 散乱)
    Output:
        homonym_list_excluded_original_form: idiom list that has same furigana but other than original_kanji_form
    """

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
        furigana_and_kanji_forms = ast.literal_eval(ret_string)  # convert str to list
        if len(furigana_and_kanji_forms) == 1 and exclude_original_form is True:
            homonym_list = [
                item
                for item in furigana_and_kanji_forms[0][1]
                if item != original_kanji_form and is_kanji_idiom(item) is True
            ]
        elif len(furigana_and_kanji_forms) == 1 and exclude_original_form is False:
            homonym_list = [
                item
                for item in furigana_and_kanji_forms[0][1]
                if is_kanji_idiom(item) is True
            ]
        else:  # those don't have any homonym or separated idioms are excluded
            homonym_list = []
        return homonym_list
