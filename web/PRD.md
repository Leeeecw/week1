# 이력서 기반 포트폴리오 웹사이트 제작 계획

## Context

`web/resume_sample.docx`(이한양 · AI Engineer 이력서)를 원본으로 삼아, 같은 내용을 웹에서 보기 좋게 보여주는 단일 페이지 포트폴리오 사이트를 만든다.
사용자 결정 사항:

- **기술 스택**: 순수 HTML/CSS/JS, 빌드 도구 없음 (기존 `game2/`와 동일한 방식)
- **언어**: 한국어 단일
- **디자인**: 미니멀 다크 테크 (어두운 배경, 단색 강조색, 코드/터미널 느낌 포인트)

이력서에서 추출한 데이터(총 6개 섹션):

| 섹션 | 내용 |
|---|---|
| Hero | 이름 "이한양", 직함 "AI ENGINEER", 자기소개 문단 1개 |
| Contact | GitHub, E-mail, Phone |
| Education | 한양대 인공지능학과 학사 (2023.03~), 4학년, 전공학점 3.0/4.5, 관련 과목 8개 |
| Activities | AI 학술동아리 (2025.03~12), AI Summer Study LLM 스터디 (2025.07~08), 각 3개 bullet |
| Skills | Programming Language / AI·ML / Tools 3개 카테고리 |
| Projects | 학사정보 RAG 챗봇 (2026.03~05), 음식 이미지 분류 시스템 (2025.09~12), 각 5개 bullet + Tech Stack + GitHub 링크 |

## 파일 구조

```
web/
├── resume_sample.docx      # 원본 (건드리지 않음)
├── index.html              # 단일 페이지, 시맨틱 섹션 6개
├── css/
│   └── style.css           # CSS 변수 기반 다크 테마, 반응형
├── js/
│   ├── data.js             # 이력서 내용을 JS 객체로 분리 (내용 수정 시 이 파일만 편집)
│   ├── render.js           # data.js → DOM 렌더링 (섹션별 템플릿 함수)
│   └── main.js             # 네비게이션 활성화, 스크롤 reveal, 초기화
└── assets/
    └── favicon.svg         # 간단한 모노그램 파비콘
```

`game2/js/`처럼 모듈을 역할별로 나누되, 페이지 규모가 작으므로 3개 파일로 제한한다.

## 구현 단계

### 1. `js/data.js` — 이력서 데이터 객체화
- docx에서 추출한 텍스트를 `const RESUME = { profile, contact, education, activities, skills, projects }` 형태로 옮긴다.
- 각 항목은 `{ period, org, title, bullets[], techStack?, github? }` 구조로 통일해 Activities와 Projects가 같은 렌더러를 공유하게 한다.
- 전화번호·이메일은 원문 그대로 두되, 이후 사용자가 실제 값으로 교체하기 쉽도록 파일 상단에 주석으로 표시한다.

### 2. `index.html` — 뼈대
- `<header>` 고정 상단 네비(이름 로고 + 섹션 앵커 5개: 소개/학력/활동/기술/프로젝트).
- `<main>` 안에 `<section id="...">` 6개. 내용은 대부분 `render.js`가 채우고, HTML은 컨테이너와 제목만 둔다.
- `<footer>`에 연락처 반복 + "© 2026 이한양".
- 메타: `lang="ko"`, viewport, `<title>이한양 | AI Engineer</title>`, description 메타, Pretendard 웹폰트(CDN) + 시스템 폰트 fallback, 코드 포인트용 monospace 스택.

### 3. `css/style.css` — 다크 테크 테마
- `:root` 변수: `--bg`(#0b0f14 계열), `--surface`, `--border`, `--text`, `--muted`, `--accent`(단일 강조색, 예: 청록 #3ddc97 또는 파랑 #5b9cff 중 하나), `--mono`.
- 레이아웃: `max-width: 960px` 중앙 컬럼, 섹션 간 넉넉한 세로 여백, 모바일(≤640px)에서 단일 컬럼.
- 컴포넌트:
  - Hero: 큰 이름 + 직함을 monospace 느낌의 태그 형태(`// AI ENGINEER`)로, 소개 문단, 연락처 버튼 3개.
  - 타임라인 카드(Education/Activities/Projects 공용): 왼쪽 기간, 오른쪽 기관·제목·bullet 목록. 좌측 세로선 + 점으로 타임라인 표현.
  - Skills: 카테고리별 pill 태그 그룹.
  - Projects: 카드 하단에 Tech Stack pill + GitHub 링크 버튼.
- 상호작용: 링크/카드 hover 시 border 색상만 `--accent`로 전환. 과한 애니메이션은 두지 않는다.
- `prefers-reduced-motion` 대응, 포커스 링 유지.

### 4. `js/render.js` — 렌더링
- `renderHero`, `renderEducation`, `renderTimeline(items)`, `renderSkills`, `renderProjects` 함수. 문자열 템플릿 대신 `document.createElement` 또는 안전한 템플릿으로 생성(데이터가 신뢰 가능하므로 innerHTML 사용 허용하되 외부 입력 없음).
- Activities/Projects는 `renderTimeline`을 공유하고, Projects만 techStack/github 블록을 추가.

### 5. `js/main.js` — 동작
- `DOMContentLoaded` 시 렌더링 실행.
- `IntersectionObserver`로 현재 섹션에 맞춰 네비 링크 활성 표시, 섹션 진입 시 fade-in 클래스 부여.
- 앵커 클릭 시 `scroll-behavior: smooth`(CSS)로 처리, JS는 최소화.

### 6. 마무리
- `assets/favicon.svg` 생성(모노그램 "LH" 또는 "이").
- Hero의 "이력서 다운로드" 버튼은 `resume_sample.docx`로 링크.

## 재사용/참고
- 파일 분할 방식과 no-build 구조는 [game2/index.html](game2/index.html), [game2/js/main.js](game2/js/main.js) 패턴을 따른다.

## 검증
1. `open web/index.html` 또는 `python3 -m http.server -d web 8080` 후 브라우저에서 확인.
2. 체크리스트:
   - 6개 섹션 모두 렌더링되고 docx 내용과 텍스트가 1:1로 일치하는지 대조.
   - GitHub 링크 3개, 메일/전화 링크(`mailto:`, `tel:`)가 동작하는지.
   - 네비 앵커 이동 및 활성 표시.
   - 창 너비 375px / 768px / 1280px에서 레이아웃 깨짐 없음.
   - 콘솔 에러 없음.
3. 배포는 범위 밖이나, GitHub Pages에 `web/` 폴더 그대로 올리면 동작하도록 상대 경로만 사용한다.
