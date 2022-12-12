# POI 데이터 리뷰

## 방법론
1. 제공받은 데이터셋을 `subcategory`별로 분류한다.
2. `subcategory` 별로 자주 등장하는 명사를 선정하고 `results`에 저장한다.
3. 저장된 `common_words`를 번역한다.
4. 선정된 `common_words`가 POI 명칭에 있다면 번역이 올바르게 되었는지 확인한다.
5. 번역이 틀리다면 `report`에 저장한다
6. `subcategory`의 총 POI 개수 중 몇 개가 틀리게 번역되었는지 확인하고 오류 백분율을 계산한다.

## TODO
- 보고용 차트 만들기