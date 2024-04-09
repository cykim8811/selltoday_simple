
def compare_strings(str1, str2):
    if type(str1) != str or type(str2) != str:
        return False
    min_str1 = str1.lower().replace(" ", "").replace("\n", "")
    min_str2 = str2.lower().replace(" ", "").replace("\n", "")
    return min_str1 == min_str2

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
    replace_data(view, "품격높은 향기를구현하기 위해", data["one_message"])
    replace_data(view, "Premium", data["product_name"].split("\\n")[0])
    replace_data(view, "Fragrance", data["product_name"].split("\\n")[1])

    replace_data(view, "Premium Fragrance", data["product_name"].split("\\n")[0])

    replace_data(view, "프리미엄 프레그런스 디퓨저를 좀 더 쉽게 접할 수 있도록", data["client_message"].split("\\n")[0])
    replace_data(view, "불필요한 공정은 빼고 보다 합리적인 가격으로", data["client_message"].split("\\n")[1])
    replace_data(view, "오직 향기에만 집중하여 만들엇습니다", data["client_message"].split("\\n")[2])

    replace_data(view, "프리미엄 프레그런스 디퓨저는 오직", data["strong_message"].split("\\n")[0])
    replace_data(view, "품격있는 향기로 고객님께 다가갑니다.", data["strong_message"].split("\\n")[1])

    view["elements"]["image_2"]["props"]["data-template"] = True

    return view

