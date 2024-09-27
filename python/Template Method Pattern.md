#design-patterns
## Template Method Pattern 이란?
- base class에서 정의한 구조를 지정
- sub class에서 구조를 재정의하지 않고 특정 부분만 정의하여 사용하는 방법을 말한다.
## 사용하면 좋은 점
1. 중복 코드 구현을 줄일 수 있다.
2. sub class 구현 단계에서 특정 단계만 쉽게 재정의 가능하다.
3. 역할 구분이 가능하다. base class는 알고리즘의 구조를 처리하고, sub class 는 각 단계의 세부 사항에 집중한다.
## Example
- 목적
	- 음료의 기본 구조를 정의하는 base class 생성
	- base class를 재사용하여 특정 함수만 정의하는 coffee, tea sub class 생성
- code
```python
from abc import ABC
from abc import abstractmethod

class Beverage(ABC):
    def prepare(self):
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        self.add_condiments()

    def boil_water(self):
        print("Boiling water")

    def pour_in_cup(self):
        print("Pouring into cup")

    @abstractmethod
    def brew(self):
        pass

    @abstractmethod
    def add_condiments(self):
        pass

class Coffee(Beverage):
    def brew(self):
        print("Dripping coffee through filter")

    def add_condiments(self):
        print("Adding sugar and milk")

class Tea(Beverage):
    def brew(self):
        print("Steeping the tea")

    def add_condiments(self):
        print("Adding lemon")

# Usage
coffee = Coffee()
tea = Tea()

print("Making coffee:")
coffee.prepare()

print("\nMaking tea:")
tea.prepare()
```
#### code에서 주목해야 할 부분
1. code 정리
	- beverage class는 base class로 공통적으로 사용하는 구조를 정의
	- sub class 에서 brew, add_condiments 메서드를 정의하도록 설정
2. abc library
	- 
3. abstractmethod 기능
	- sub class에서 기능을 정의하도록 지정하는 decorator
## reference
- https://startcodingnow.com/template-method-design-pattern
- https://bluese05.tistory.com/61
- https://docs.python.org/3/library/abc.html