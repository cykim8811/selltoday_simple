
import json
from utils import svg_to_json, json_to_svg

with open("data.json", "r") as file:
    total_data = json.load(file)

for single_data in total_data:
    template = single_data["template"]
    data = single_data["data"]

    import importlib
    module = importlib.import_module(f"templates.filler.{template}")
    fill = module.fill

    # import templates/view/{template}.svg
    svg_name = template.split("_")
    svg_name = f"{svg_name[0]}-{int(svg_name[1]):d}.svg"
    with open(f"templates/view/{svg_name}", "r") as file:
        svg_raw_data = file.read()
    svg_data = svg_to_json(svg_raw_data)

    # fill the view
    view = fill(svg_data, data)

    # # Convert all images to https://via.placeholder.com/640x480
    for idx, element in view["elements"].items():
        if type(element) is not dict:
            continue
        if "href" in element["props"] and "data-template" in element["props"]:
            view["elements"][idx]["props"]["href"] = "https://via.placeholder.com/640x480"
            element["props"]["preserveAspectRatio"] = "xMidYMid slice"

    # convert the view to SVG
    svg_output = json_to_svg(view)
    with open(f"output/{template}.svg", "w") as file:
        file.write(svg_output)

    print(f"Generated output/{template}.svg")

print("All templates are generated")


