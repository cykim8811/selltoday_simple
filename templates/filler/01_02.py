
"""

    "strength_point_message1": {
        "description": "제품의 장점 중 1번 장점을 표현하는 한 문장의 메세지",
        "restriction": "명사형으로 끝남, 두 줄로 구성, \\n로 구분, 줄당 9글자 이내 ",
        "examples": [
            "곡물에서 발효한\\n식물성 에탄올 베이스"
        ]
    },
    "strength_point_message2": {
        "description": "제품의 장점 중 2번 장점을 표현하는 한 문장의 메세지",
        "restriction": "명사형으로 끝남, 두 줄로 구성, \\n로 구분, 줄당 9글자 이내 ",
        "examples": [
            "전문 연구소 기술로\\n구현한 최적의 발향력"
        ]
    },
    "strength_point_message3": {
        "description": "제품의 장점 중 3번 장점을 표현하는 한 문장의 메세지",
        "restriction": "명사형으로 끝남, 두 줄로 구성, \\n로 구분, 줄당 9글자 이내 ",
        "examples": [
            "인테리어를 고급스럽게\\n만드는 오브제"
        ]
    }
"""

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
    # replace_data(view, "BRAND STORY", data["brand_name"])
    # replace_data(view, "우리 가구는 안전합니다.", data["before_after_sentence"].split("\\n")[0])
    # replace_data(view, "친환경목재 SEO를 사용합니다.", data["before_after_sentence"].split("\\n")[1])

    # replace_data(view, "친환경 목재를 사용하여 안전합니다.", data["before_after_message"].split("\\n")[0])
    # replace_data(view, '친환경목재 등급', "“" + data["before_after_message"].split("\\n")[1])
    # replace_data(view, 'SEO', "")

    # Premium
    # Fragrance

    replace_data(view, "Premium", data["product_name"].split("\\n")[0])
    replace_data(view, "Fragrance", data["product_name"].split("\\n")[1])

    replace_data(view, "품격높은 향기를구현하기 위해 자연에서 얻은 원료", data["simple_desc"])

    # 은은하게 퍼지는 향기
    # 숲 속의 검은색
    # 묵직한우디, 차분

    replace_data(view, "은은하게 퍼지는 향기", [data[f"title{t+1}"] for t in range(3)])
    replace_data(view, "숲 속의 검은색", [data[f"desc{t+1}"].split("\\n")[0] for t in range(3)])
    replace_data(view, "묵직한 우디, 차분", [data[f"desc{t+1}"].split("\\n")[1] for t in range(3)])

    return view