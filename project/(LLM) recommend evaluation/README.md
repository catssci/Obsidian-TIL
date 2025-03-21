## 목적
- LLM으로 추천결과를 평가
## 배경
- LLM을 이용한 추천 시스템 개발 중 평가 방법 필요성 발생
- 정답 데이터를 만들어 평가하는 방법이 가장 좋지만 현실적으로 불가능이라고 판단
	- 후보 리스트가 100만개 이상 존재 할 수 도 있음
	- 사람이 수동으로 한다고 해도 휴먼 에러 발생 가능성 존재
	- 비슷한 순위를 가지는 정답 데이터 존재 다수
	- 정답을 만드는 모델 만드는 것도 모순적
## Process
1. 쿼리 입력
2. 추천 결과 수집
	1. api요청으로 수집 (검색어, 최근 본 상품 기반)
	2. 프롬프트 입력에 맞게 데이터 전처리
4. 추천 결과 평가
	1. 특정 LLM 모델 선택 (using Gemini)
	2. 입력 쿼리와 추천 결과 평가하는 프롬프트 작성 (관련성 평가)
	3. 연관성 점수 평가
 	4. dataFrame 형태로 변환
5. 평가 결과 종합
	1. 점수 summary (총합, 분포)


## Data Structure
### input
| action | input | recommend |
| --- | --- | --- |
| recommend | 최근 본 상품 dictionary | 추천 결과 |
| search | 쿼리 | 추천 결과 |

### output
- 평가 결과 json 형태로 반환

## 후기
- 추천 시스템 평가를 LLM으로 수행
- 따로 학습 모델을 fine-tuning 하지 않아도 충분히 평가가 가능하다는 것을 확인함

## To-do List
- [ ] 평가 결과를 바탕으로 리랭킹 수행 (추후 다른 프로젝트로 진행)
