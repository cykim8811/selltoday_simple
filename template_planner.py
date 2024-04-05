
import os
import random
import json

from claude import ChatContext, getUsage

model = "sonnet"

exchange_rate = 1350

# target_template = "01_07"
target_template = None

available_templates = {
    '원메세지 제품 설명 템플릿': ['01_04', '01_07'],
    '제품 주요 성분 나열 템플릿': ['01_02', '02_04', '02_05', '02_06'],
    '제품 장점 나열 템플릿': ['01_06', '03_03', '04_06'],
    '귀사 유사 제품 홍보 템플릿': ['01_08', '05_07'],
    '자세한 제품 설명 템플릿': ['01_09', '05_08'],
    '브랜드 소개 템플릿': ['06_02'],
    '상품 구성 템플릿': [],
    '구매 후기 템플릿': ['03_06'],
    '정품 인증 템플릿': ['04_05'],
    '사용 방법 템플릿': ['04_07', '06_07'],
    '임상 실험 검증 템플릿': ['05_05'],
    '사용 전/후 비교 템플릿': ['06_03'],
    '배송 관련 템플릿': [],
    '프로모션 템플릿': [],
    '누적 판매량 강조 템플릿': [],
    'FAQ 템플릿': [],
    '추천 템플릿': [],
    '교환 및 반품 안내 템플릿': [],
}

def template_planner():

    with open("total_plan.txt", "r") as f:
        total_plan = f.read()

    with open("template_plan.json", "r") as f:
        template_plans = json.load(f)

    total_result = []

    for template_plan in template_plans:
        template_name = template_plan["template_name"]
        if template_name not in available_templates:
            print(f"Template '{template_name}' does not exist")
            continue
        if not available_templates[template_name]:
            print(f"Template '{template_name}' is empty")
            continue
        
        shuffled_templates = available_templates[template_name]
        random.shuffle(shuffled_templates)

        for template in shuffled_templates:
            if target_template and template != target_template:
                continue
            if os.path.exists(f"templates/format/{template}.json"):
                break
        else:
            print(f"Template '{template_name}' is not available")
            continue

        with open(f"templates/format/{template}.json", "r") as f:
            template_format = json.load(f)

        prompt = """
        안녕. 너는 세계 최고의 마케터이고, 온라인 상품 판매 시 제품 소개에 필요한 '상세페이지' 내
        하나의 템플릿 제작을 돕는 역할을 할꺼야. 아래와 같은 순서로 너는 일을 진행할꺼야
        1. 어떤 템플릿의 구조에 대해 전달받는다.
        2. 특정 제품의 다양한 정보가 담긴 제품의 '전체 상세페이지 기획서'와, 각 템플릿 작성 요령이 담긴 '템플릿 제작 기획서'를 전달받는다.
        3. 위 2번에서 전달받은 두 기획서를 토대로 1번에서 설명한 템플릿의 카피라이팅을 완성한다.

        1,2번정보는 내가 전달해 줄 것이고, 3번은 어떠한 내용과 카피라이팅, 이미지로 구성되어야 하는지 템플릿 작성 
        방법을 알려줘. 너가 작성한 내용 토대로 인터넷에 상세페이지로 사용할 거니까 그에 맞는 적절한 말투로 작성을 
        부탁한다. 이제 템플릿 구조와 두 기획서를 제공할께.
        

        #전체 상세페이지 기획서
        {total_plan}

        # 템플릿 제작 기획서
        {template_plan}

        # 출력 포맷
        {output_format}

        # 예시
        ```json
        {example}
        ```"""

        user_prompt = """위 템플릿 구조에 맞게 카피라이팅 작성을 해줘. 구조대로 작내가 제공한 내용에서 너무 새로운 내용을 추가하지 않길 바래.
        카피라이팅 작성 시 너무 AI가 만든게 아닌 사람이 만든것 처럼 제공해주면 고맙겠어.
        주의: 출력은 json 형식으로 제공하며 json 데이터 외의 내용은 포함하지 않아야 한다.
        """


        output_format = ""
        for key in template_format:
            output_format += f"- {key}: {template_format[key]["description"]}\n"
            output_format += f"  - restriction: {template_format[key]['restriction']}\n"

        example = {
            key: template_format[key]["examples"][0] for key in template_format
        }
        example = json.dumps(example, indent=4, ensure_ascii=False)

        final_prompt = prompt.format(total_plan=total_plan, template_plan=template_plan, output_format=output_format, example=example)

        ai = ChatContext(final_prompt, model=model)
        res = ai.ask(user_prompt, force_format="{\n    \"")

        try:
            total_result.append({
                "template": template,
                "data": json.loads(res)
            })
            print(f"Template '{template}' completed")
        except:
            print(f"Fails to parse the result of template '{template}'")
        finally:
            print(f"- Usage: {getUsage() * exchange_rate:.1f}원")
        
    with open("data.json", "w") as f:
        json.dump(total_result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    template_planner()
