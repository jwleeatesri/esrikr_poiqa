# POI 데이터 리뷰

# 저장소 활용법
> 위 `reports` 폴더로 들어가면 카테고리별로 문제 있는 POI, 문제의 심각도를 정리한 파이차트를 찾아 볼 수 있습니다.

## 과정
1. 제공받은 데이터셋을 `subcategory`별로 분류한다.
2. `subcategory` 별로 자주 등장하는 명사를 선정하고 `results`에 저장한다.
3. 저장된 `common_words`를 번역한다.
4. 선정된 `common_words`가 POI 명칭에 있다면 번역이 올바르게 되었는지 확인한다.
5. 번역이 틀리다면 `report`에 저장한다
6. `subcategory`의 총 POI 개수 중 몇 개가 틀리게 번역되었는지 확인하고 오류 백분율을 계산한다.

## TODO
- [x] 보고용 차트 만들기
- [] 나머지 번역하자...
- [] 어디가 어떻게 틀렸는지 보여주기
