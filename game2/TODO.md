# Slither.io 스타일 지렁이 게임 TODO

## 1. 뼈대

- [x] index.html (캔버스, HUD, 시작/게임오버 오버레이)
- [x] style.css (전체화면 캔버스, 오버레이)
- [x] js/config.js (상수)
- [x] js/main.js (초기화, 게임 루프, 상태 전환)

## 2. 플레이어 이동

- [x] js/snake.js (Snake 클래스, 경로 히스토리 기반 세그먼트)
- [x] js/input.js (마우스 → targetAngle, 부스트 입력)
- [x] js/camera.js (플레이어 추적, 길이 기반 줌)

## 3. 렌더링

- [x] js/renderer.js (배경 격자, 맵 경계, 먹이, 지렁이, 미니맵)

## 4. 먹이 및 성장

- [x] js/food.js (먹이 풀, spatial hash, 섭취 시 성장)

## 5. 충돌

- [x] js/world.js (머리 vs 세그먼트 충돌, 맵 경계 사망, 사망 시 먹이 드롭, 리스폰)

## 6. AI

- [x] js/ai.js (위험 회피 → 먹이 추적 → 배회, 랜덤 부스트)

## 7. 부가 기능

- [x] 부스트 (속도 증가, 길이 감소, 꼬리 먹이 드롭)
- [x] 줌아웃
- [x] 미니맵
- [x] HUD 순위

## 8. 최고 점수 및 오버레이

- [x] js/storage.js (localStorage 최고 점수)
- [x] 시작/게임오버 오버레이 연결

## 9. 검증

- [x] 로컬 서버 실행 후 브라우저 동작 확인
- [x] 문법 검사 (node --check) — 이 환경에 node 미설치
