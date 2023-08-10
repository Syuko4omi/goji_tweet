KANJI_IDIOM_REGEX = "[一-龥]+"
hiragana_rules_dict = {
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
