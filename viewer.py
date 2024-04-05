
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

import json
def construct_whole():
    templates_text = ""
    templates_format = "<img src='output/{template}.svg' style='width: 50%; border: 2px solid #ddd;'>"
    with open("data.json", "r") as f:
        template_plans = json.load(f)
        for template_plan in template_plans:
            template_id = template_plan["template"]
            templates_text += templates_format.format(template=template_id)
    return html.format(templates=templates_text)


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return construct_whole()

@app.get("/output/{template_id}.svg")
async def read_item(template_id: str):
    return FileResponse(f"output/{template_id}.svg")
