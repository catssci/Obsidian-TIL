import os
import pandas as pd
from dotenv import load_dotenv
import json

import vertexai
from vertexai.generative_models import GenerativeModel

class Evaluator:
    def __init__(self):
        # .env 파일 활성화
        load_dotenv()

        # 프로젝트 ID와 위치 정보 가져오기
        self.PROJECT_ID = os.getenv('project_id')
        self.LOCATION = os.getenv('location')

        # 환경 변수가 제대로 로드되었는지 확인
        if not all([self.PROJECT_ID, self.LOCATION]):
            raise ValueError("일부 필수 환경 변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")

        print("환경 변수가 성공적으로 로드되었습니다.")

        # Vertex AI multimodal model initialize
        vertexai.init(project=self.PROJECT_ID, location=self.LOCATION)
        self.model_gemini = GenerativeModel("gemini-1.5-flash-002")

    def get_test_data(self):
        df = pd.read_csv('test_data.csv')
        return df

    def get_prompt(self, action='recommend', recent_goods=None, query=None, recommend_results=None):
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
                1. 검색 쿼리와 검색 결과의 연관성 분류
                    - 연관성은 0과 10 사이의 값으로 구분한다.
                    - 높을수록 연관성이 높다.
                2. 연관성 분류 이유 설명

                형식은 json 포맷으로 해줘.
                json 포맷은 다음과 같다.
                {{
                    "query": "검색 쿼리",
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

                query: {query},

                result: {recommend_results}
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

    def run_evaluation(self, df):
        results = []
        for index, row in df.iterrows():
            if row['action'] == 'recommend':
                prompt = self.get_prompt(action='recommend', recent_goods=row['input'], recommend_results=row['recommend'])
            elif row['action'] == 'search':
                prompt = self.get_prompt(action='search', query=row['input'], recommend_results=row['recommend'])
            
            response = self.get_response(prompt)
            result = response.text.replace("```json", "").replace("```", "").strip()
            
            result_json = json.loads(result)
            print(result_json)
            print(pd.DataFrame(result_json["results"]))
            
            results.append(result_json)
        
        return results

if __name__ == '__main__':
    evaluator = Evaluator()
    df = evaluator.get_test_data()
    evaluation_results = evaluator.run_evaluation(df)