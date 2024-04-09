
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Selltoday</title>
    </head>
    <body>
        <div style="display: flex; flex-direction: column; align-items: center;">
            {templates}
        </div>
    </body>
</html>
"""

import re
def search_fonts(data, idx):
    fonts = []
    if isinstance(data["elements"][idx], str):
        font_regexp = re.compile(r"font-family:([^;]+);")
        matches = font_regexp.findall(data["elements"][idx])
        for match in matches:
            print(match)
            for t in match.split(","):
                fonts.append(t.strip().replace('"', "").replace("'", ""))
        return fonts
    if data["elements"][idx]["tag"] == "text":
        if "style" in data["elements"][idx]["props"] and "font-family" in data["elements"][idx]["props"]["style"]:
            fonts.append(data["elements"][idx]["props"]["style"]["font-family"])
    if "children" in data["elements"][idx]:
        for child in data["elements"][idx]["children"]:
            fonts.extend(search_fonts(data, child))
    return fonts

import json
import os
from utils import svg_to_json, json_to_svg
def construct_whole():
    templates_text = ""
    # templates_format = "<img src='output/{template}.svg' style='width: 560px; height: auto; border: 2px solid #ddd;'>"
    # templates_format = "<div style='width: 560px; height: auto; border: 2px solid #ddd;'>{svg_data}</div>"
    templates_format = "<object data='output/{template}.svg' type='image/svg+xml' style='width: 560px; height: auto; border: 2px solid #ddd;'></object>"
    with open("data.json", "r") as f:
        template_plans = json.load(f)
        for template_plan in template_plans:
            template_id = template_plan["template"]
            if not os.path.exists(f"output/{template_id}.svg"):
                continue
            # templates_text += templates_format.format(svg_data=svg_raw_data)
            templates_text += templates_format.format(template=template_id)
        
    return html.format(templates=templates_text)


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return construct_whole()

@app.get("/output/{template_id}.svg")
async def read_item(template_id: str):
    if not os.path.exists(f"output/{template_id}.svg"):
        return JSONResponse(status_code=404, content={"error": "Template not found"})
    with open(f"output/{template_id}.svg", "r") as file:
        svg_raw_data = file.read()
    data = svg_to_json(svg_raw_data)
    used_fonts = search_fonts(data, "0")
    fonts_text = ""
    for font in used_fonts:
        fonts_text += f'''
@font-face {{
    font-family: '{font}';
    src: url('https://sprintchallenge.cykim.site/api/font/{font.replace(" ", "+")}') format('woff2');
}}
'''
    style_element = {
        "tag": "style",
        "props": {
            "type": "text/css"
        },
        "children": ["font_text"]
    }
    defs_element = {
        "tag": "defs",
        "props": {},
        "children": ["style_element"]
    }
    data["elements"]["0"]["children"] = ["defs_element"] + data["elements"]["0"]["children"]
    data["elements"]["style_element"] = style_element
    data["elements"]["defs_element"] = defs_element
    data["elements"]["font_text"] = fonts_text
    svg_output = json_to_svg(data)
    print(type(svg_output))
    from fastapi.responses import StreamingResponse
    return StreamingResponse(content=svg_output, media_type="image/svg+xml")

@app.get("/output/{file_name}")
async def read_item(file_name: str):
    return FileResponse(f"output/{file_name}")

from fontTools.ttLib import TTFont
from fontTools.ttLib.woff2 import compress
@app.get("/api/font/{font_name:path}")
async def get_font(font_name: str):
    if ".." in font_name or "/" in font_name:
        return JSONResponse(status_code=403, content={"error": "Invalid path"})
    font_name = font_name.replace(".woff2", "").replace("+", " ")
    output = f"fonts/woff2/{font_name}.woff2"
    if os.path.exists(output):
        return FileResponse(output)
    with open("available_fonts.json", "r") as file:
        fonts = json.load(file)
    if font_name in fonts:
        compress(fonts[font_name], output)
        return FileResponse(output)
    else:
        return {"error": "Font not found"}
