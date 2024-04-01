
import json
from claude import ChatContext, getUsage

index = 0

with open("total_plan.txt", "r") as f:
    total_plan = f.read()

with open("template_plan.json", "r") as f:
    template_plan = json.load(f)[index]

prompt = """
안녕. 너는 세계 최고의 마케터이고, 온라인 상품 판매 시 제품 소개에 필요한 '상세페이지' 내
하나의 템플릿 제작을 돕는 역할을 할꺼야. 아래와 같은 순서로 너는 일을 진행할꺼야
1. 어떤 템플릿의 구조에 대해 전달받는다.
2. 특정 제품의 다양한 정보가 담긴 제품의 '전체 상세페이지 기획서'와, 각 템플릿 작성 요령이 담긴 '템플릿 제작 기획서'를 전달받는다.
3. 위 2번에서 전달받은 두 기획서를 토대로 1번에서 설명한 템플릿의 카피라이팅을 완성한다.

1,2번정보는 내가 전달해 줄 것이고, 3번은 어떠한 내용과 카피라이팅, 이미지로 구성되어야 하는지 템플릿 작성 
방법을 알려줘. 너가 작성한 내용 토대로 인터넷에 상세페이지로 사용할 거니까 그에 맞는 적절한 말투로 작성을 
부탁한다. 이제 템플릿 구조와 두 기획서를 제공할께.
 
# 템플릿의 구조
- 템플릿 종류: 원메세지 제품 설명 템플릿
- 제품명: 제품명
- 제품의 핵심을 담은 한 문장: 제품의 특징과 강점을 한문장에 담은 원메시지
- 제품의 이미지

#전체 상세페이지 기획서
{total_plan}

# 템플릿 제작 기획서
{template_plan}

# 출력 포맷
{output_format}
"""

user_prompt = """위 템플릿 구조에 맞게 카피라이팅 작성을 해줘. 구조대로 작내가 제공한 내용에서 너무 새로운 내용을 추가하지 않길 바래.
카피라이팅 작성 시 너무 AI가 만든게 아닌 사람이 만든것 처럼 제공해주면 고맙겠어."""

output_format = """
{
    "one_message": "제품을 사고 싶게 만드는 한마디",
    "product_name": "제품의 이름(영어)",
    "client_message": "제품의 소구점 및 특징을 강조하는 세 줄의 한 문장으로 구성된 메시지",
    "strong_message": "고객에게 진심을 전할 수 있도록 두 줄의 한 문장으로 구성된 메시지"
}
"""

ai = ChatContext(prompt.format(total_plan=total_plan, template_plan=template_plan, output_format=output_format))
res = ai.ask(user_prompt, force_format="{\n    \"")

print(res)
