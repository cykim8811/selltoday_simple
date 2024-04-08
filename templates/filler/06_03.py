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
    for idx, element in view["elements"].items():
        if compare_strings(element, data):
            view["elements"][idx] = new_data
            break
    else:
        print(f"Data not found: {data}")
    return view


def fill(view, data):
    replace_data(view, "BRAND STORY", data["brand_name"])
    replace_data(view, "우리 가구는 안전합니다.", data["before_after_sentence"].split("\\n")[0])
    replace_data(view, "친환경목재 SEO를 사용합니다.", data["before_after_sentence"].split("\\n")[1])

    replace_data(view, "친환경 목재를 사용하여 안전합니다.", data["before_after_message"].split("\\n")[0])
    replace_data(view, '친환경목재 등급', "“" + data["before_after_message"].split("\\n")[1])
    replace_data(view, 'SEO', "")

    return view