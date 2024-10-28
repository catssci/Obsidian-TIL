import os
import pandas as pd
from dotenv import load_dotenv
import json
import datetime
import vertexai
from vertexai.generative_models import GenerativeModel
from concurrent.futures import ThreadPoolExecutor

class Evaluator:
    def __init__(self, model = 'pro'):
        # .env 파일 활성화
        load_dotenv()

        # 프로젝트 ID와 위치 정보 가져오기
        self.PROJECT_ID = os.getenv('project_id')
        self.LOCATION = os.getenv('location')

        # 환경 변수가 제대로 로드되었는지 확인
        if not all([self.PROJECT_ID, self.LOCATION]):
            raise ValueError("일부 필수 환경 변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")

        # Vertex AI multimodal model initialize
        vertexai.init(project=self.PROJECT_ID, location=self.LOCATION)
        if model == 'pro':
            self.model_gemini = GenerativeModel("gemini-1.5-pro-002")
        elif model == 'flash':
            self.model_gemini = GenerativeModel("gemini-1.5-flash-002")

        self.today = datetime.datetime.today().strftime('%Y-%m-%d')

    def get_test_data(self):
        df = pd.read_csv('data/test_data.csv')
        return df

    def get_eval_prompt(self, action='recommend', recent_goods=None, query=None, recommend_results=None):
        """
            action: 'recommend' or 'search'
            recent_goods: 최근 본 상품
            query: 검색 쿼리
            recommend_results: 추천 결과
        """
        if action == 'recommend':
            prompt = f"""
                목적: 추천결과를 평가하는 역할
                데이터 형태:  
                - recent_goods: 최근 본 상품
                - result: 추천 결과

                평가 순서
                1. 최근 본 상품과 추천 결과의 연관성 분류
                    - 연관성은 0과 10 사이의 값으로 구분한다.
                    - 높을수록 연관성이 높다.
                2. 연관성 분류 이유 설명

                형식은 json 포맷으로 해줘.
                json 포맷은 다음과 같다.
                {{
                    "recent_goods": "최근 본 상품",
                    "results": [
                        {{   
                            "goodsnm": "상품명",
                            "score": 0,
                            "reason": "이유"
                        }}, 
                        {{
                            "goodsnm": "상품명",
                            "score": 0,
                            "reason": "이유"
                        }},
                        ...
                    ]
                }}

                recent_goods: {recent_goods},

                result: {recommend_results}
            """
        elif action == 'search':
            prompt = f"""
                목적: 추천결과를 평가하는 역할
                데이터 형태:  
                - query: 검색 쿼리
                - result: 검색 결과

                평가 순서
                1. 검색 쿼리 의도 분석
                    - 검색 쿼리의 의도를 분석한다.
                    - 의도는 다음과 같은 것들이 있다. (중복 가능)
                        - 상품 찾기
                        - 컬러 찾기
                        - 브랜드 찾기
                        - 가격 찾기
                        - 스타일 찾기
                        - 소재 찾기
                        - 분위기 찾기
                        - TPO 찾기
                        - 기타
                2. 검색 쿼리와 검색 결과의 연관성 분류
                    - 연관성은 0과 10 사이의 값으로 구분한다.
                    - 높을수록 연관성이 높다.
                    - 영문으로 검색을 해도 한글 의미가 같으면 연관성이 높다.
                    - 영문으로 검색을 해도 한글 의미가 다르면 연관성이 낮다.
                    - 일관성 있게 평가해야 한다.
                    - 의도에 맞는 검색 결과는 연관성이 높다.
                    - 검색어에 계절 정보가 없는 경우 현재 한국 날짜를 반영하여 평가한다.
                    - 검색어에 계절 정보가 있는 경우 입력된 계절 정보를 반영하여 평가한다.
                3. 연관성 분류 이유 설명
                    - 일관성 있는 이유를 설명해야 한다.
                4. 출력 형식
                    - 형식은 json 포맷으로 해줘.
                    - json 포맷은 다음과 같다.
                    {{
                        "query": "검색 쿼리",
                        "query_detail": "검색 쿼리 의도",
                        "results": [
                            {{   
                                "goodsnm": "상품명",
                                "brand": "브랜드",
                                "score": 0,
                                "reason": "이유"
                            }}, 
                            {{
                                "goodsnm": "상품명",
                                "brand": "브랜드",
                                "score": 0,
                                "reason": "이유"
                            }},
                            ...
                        ]
                    }}

                query: {query},
                result: {recommend_results},
                현재 한국 날짜: {self.today}
            """
        return prompt

    def get_summary_prompt(self, action = 'search', eval_results=None):
        prompt = f"""
            목적: 추천평가 리스트를 요약하는 역할
            데이터 형태:  
                - eval_results: 추천평가 리스트

            요약 순서
            1. 추천평가 리스트를 요약한다.
            2. 요약 내용은 줄바꿈을 하지 않고 한줄로 표현한다.

            형식은 json 포맷으로 해줘.
            json 포맷은 다음과 같다.
            {{
                "summary": "요약 내용"
            }}

            eval_results: {eval_results}
        """
        return prompt

    def get_response(self, prompt):
        responses = self.model_gemini.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.9,
            }
        )
        return responses

    def process_row(self, row, mode=None):
        try:
            if row['action'] == 'recommend':
                eval_prompt = self.get_eval_prompt(action='recommend', recent_goods=row['input'], recommend_results=row['recommend'])
            elif row['action'] == 'search':
                eval_prompt = self.get_eval_prompt(action='search', query=row['input'], recommend_results=row['recommend'])

            response = self.get_response(eval_prompt)
            result = response.text.replace("```json", "").replace("```", "").strip()

            if mode == 'test':
                print(result)

            result_json = json.loads(result)

            summary_prompt = self.get_summary_prompt(action='search', eval_results=result_json['results'])
            response_summary = self.get_response(summary_prompt)
            result_summary = response_summary.text.replace("```json", "").replace("```", "").strip()

            result_summary_json = json.loads(result_summary)

        except Exception as e:
            result_json, result_summary_json = {}, {}
            result_json['results'] = str(e)
            result_summary_json['summary'] = str(e)

        if mode == 'test':
            for idx, result in enumerate(result_json.get('results', [])):
                print(f"{idx + 1}번째 추천 결과")
                print(f"상품명: {result['goodsnm']}\n 점수: {result['score']}, 이유: {result['reason']}")

        return {
            'input': row['input'],
            'result': result_json.get('results', []),
            'summary': result_summary_json.get('summary', "")
        }

    def run_evaluation(self, df, mode=None, max_workers=10):
        results = []

        # ThreadPoolExecutor에 max_workers 파라미터 추가
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 데이터프레임의 각 행을 병렬로 처리
            results = list(executor.map(lambda row: self.process_row(row, mode), [row for _, row in df.iterrows()]))

        # 결과를 DataFrame으로 변환하여 반환
        result_df = pd.DataFrame(results)
        return result_df
    
if __name__ == '__main__':
    evaluator = Evaluator()
    df = evaluator.get_test_data()
    evaluation_results = evaluator.run_evaluation(df, mode='test')