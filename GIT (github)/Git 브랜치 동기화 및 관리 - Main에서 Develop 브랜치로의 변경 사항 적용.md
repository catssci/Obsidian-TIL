
## 목적
- main과 develop 브랜치 간의 동기화 (develop 브랜치 작업을 재개하면서도 코드의 일관성을 유지 가능)
## 상황 설정
1. main 브랜치가 develop 브랜치 보더 더 앞서 있는 상황
2. develop 브랜치를 main 브랜치와 동일하게 맞추고 싶을 때
## 실습
### 1. 현재 상태를 커밋한 후 브랜치 전환하기
- main 브랜치에서 작업한 내용을 커밋
- 작업 중인 파일을 저장해두고, develop 브랜치로 전환할 때 데이터를 잃지 않도록
```bash
git add .
git commit -m "Commit current changes in main"
```
### 2. 브랜치 전환 중 에러 해결하기
- develop 브랜치로 전환할 때, 로컬 변경 사항이 존재하면 충돌이 발생 가능
- 변경 사항을 스태시하거나 커밋하여 충돌 방지
```bash
git stash # 또는 git commit -m "Save local changes"
git checkout develop
```
### 3. Main 브랜치의 변경 사항을 Develop 브랜치에 덮어쓰기
- develop 브랜치로 전환한 후, main 브랜치의 변경 사항을 강제로 덮어쓰는 방식으로 동기화
```bash
git reset --hard main
git push origin develop --force
```
