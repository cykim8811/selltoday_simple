def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

def compare_strings(str1, str2):
    if type(str1) != str or type(str2) != str:
        return False
    min_str1 = str1.lower().replace(" ", "").replace("\n", "")
    min_str2 = str2.lower().replace(" ", "").replace("\n", "")

    return levenshtein_distance(min_str1, min_str2) / max(len(min_str1), len(min_str2)) < 0.3
    

def find_id_by_data(view, data):
    for idx, element in view["elements"].items():
        if compare_strings(element, data):
            return idx
    return None

def replace_data(view, data, new_data):
    if type(new_data) is not list:
        new_data = [new_data]
    for idx, element in view["elements"].items():
        if compare_strings(element, data):
            view["elements"][idx] = new_data.pop(0)
    else:
        print(f"Data not found: {data}")
    return view


def fill(view, data):
    replace_data(view, "이렇게 사용하시면 편리합니다.", data["how_to_use_sentence"])
    replace_data(view, "알루미늄캡을", [data[f"how_to_use_message{t+1}"].split("\\n")[0] for t in range(3)])
    replace_data(view, "화살표 방향으로", [data[f"how_to_use_message{t+1}"].split("\\n")[1] for t in range(3)])
    replace_data(view, "돌려주세요.", [data[f"how_to_use_message{t+1}"].split("\\n")[2] for t in range(3)])

    original_warnings = [
        "어린이 손에 닿지 않게 보관하세요.",
        "넘어진채로 방치되면 액이 흘러놀 수있습니다.",
        "직사광선이나 인화성물질, 열기에 노출시키지 마세요.",
        "내용물이 눈에 들어가지 않도록 주의하세요.",
    ]

    for idx, warning in enumerate(original_warnings):
        replace_data(view, warning, data["warning_message"].split("\\n")[idx])

    view["elements"]["image_3"]["props"]["data-template"] = True
    view["elements"]["image_4"]["props"]["data-template"] = True
    view["elements"]["image_5"]["props"]["data-template"] = True
    
    return view