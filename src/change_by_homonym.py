import urllib.request
import urllib.parse
import ast


def suggest_homonym_list(hiragana_form: str, original_kanji_form: str) -> list[str]:
    url_encoded_form = urllib.parse.quote(hiragana_form, "utf-8")
    # https://www.google.co.jp/ime/cgiapi.html
    query_url = (
        "http://www.google.com/transliterate?langpair=ja-Hira|ja&text={}".format(
            url_encoded_form
        )
    )
    request = urllib.request.Request(query_url)

    with urllib.request.urlopen(request) as res:
        ret_string = res.readline().decode("utf-8")
        homonym_list = ast.literal_eval(ret_string)
        homonym_list_excluded_original_form = [
            item for item in homonym_list[0][1] if item != original_kanji_form
        ]
        return homonym_list_excluded_original_form


if __name__ == "__main__":
    print(suggest_homonym_list("ヘンカン", "変換"))
