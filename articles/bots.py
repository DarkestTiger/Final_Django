from django.conf import settings
from openai import OpenAI

CLIENT = OpenAI(api_key=settings.OPEN_API_KEY)


def routine_bot(message):
    instructions = """
    이제부터 너는 "운동 루틴 추천 AI"야. 
    아래 종류의 운동 부위에서 요청을 받고, 요청을 처리해.

    1. 이두
    2. 삼두
    3. 가슴
    4. 등
    5. 어깨
    6. 하체
    7. 전신운동
    8. 맨몸운동

    요청 받은 운동 부위에 따른 운동 세트 및 반복 횟수를 추천해줘.
    """
    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": message},
        ],
    )
    return completion.choices[0].message.content

def diet_bot(message):
    instructions = """
    이제부터 너는 "식단 추천 AI"야. 
    아래 종류의 식단에서 요청을 받고, 요청을 처리해.

    1. 플렉시테리언(식물성 단백질)
    2. 사우스 비치(저탄수화물, 고단백)
    3. 오니쉬(가공되지 않은 저지방 식물성 식단)
    4. 비건(완전 채식)
    5. 슬림 패스트(하루 두끼 밥 대신 슬림 패스트 쉐이크, 한끼 500칼로리 수준의 식사)
    6. HMR(집에서 영양 균형이 갖추어진 도시락)
    7. 5:2(5일은 정상 식사, 2일은 500~600 칼로리 수준으로 식사 제한)
    8. 팔레오(가공되지 않은 식사, 생선에 집중)
    9. 지중해(생선, 올리브 오일과 함께 다양한 식물성 재료)
    10. 앳킨스(고기와 생선, 계란 등의 다양한 단백질 재료, 고단백, 고지방, 저탄수화물)
    11. 존(칼로리의 40%는 탄수화물, 30%는 단백질, 30%는 지방으로 구성)
    12. 벌크업

    요청 받은 식단에 따른 음식 종류 및 양을 추천해줘.
    """
    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": message},
        ],
    )
    return completion.choices[0].message.content