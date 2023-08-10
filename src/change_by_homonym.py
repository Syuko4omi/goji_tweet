import urllib.request
import urllib.parse
import ast


def suggest_homonym_list(hiragana_form: str, original_kanji_form: str) -> list[str]:
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
        homonym_list = ast.literal_eval(ret_string)  # convert str to list
        homonym_list_excluded_original_form = [
            item for item in homonym_list[0][1] if item != original_kanji_form
        ]
        return homonym_list_excluded_original_form


"""
if __name__ == "__main__":
    print(suggest_homonym_list("ヘンカン", "変換"))
"""
