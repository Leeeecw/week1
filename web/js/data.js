// 이력서 데이터 (원본: resume_sample.docx)
// 내용을 수정할 때는 이 파일만 편집하면 됩니다.
// NOTE: contact의 email / phone / github 값은 샘플입니다. 실제 값으로 교체하세요.

const RESUME = {
  profile: {
    name: '이한양',
    title: 'AI ENGINEER',
    intro:
      '한양대학교 인공지능학과에서 머신러닝과 딥러닝을 공부하며, 이론을 실제 문제에 적용하는 프로젝트를 수행해왔습니다. ' +
      'PyTorch를 활용한 딥러닝 모델 구현부터 Transformer 기반 자연어처리, LLM과 RAG를 활용한 AI 서비스 개발까지 다양한 분야를 경험하고 있습니다. ' +
      '데이터 전처리, 모델 설계, 학습, 평가 및 서비스 구현까지 AI 시스템의 전체 과정을 이해하고 직접 구현할 수 있는 AI Engineer를 목표로 하고 있습니다.',
    resumeFile: 'resume_sample.docx',
  },

  contact: {
    github: 'https://github.com/example-hanyang-ai',
    email: 'lee.hanyang@example.com',
    phone: '010-0000-0000',
  },

  education: [
    {
      period: '2023. 03 - 현재',
      org: '한양대학교',
      title: '인공지능학과 학사과정',
      bullets: [
        '2026년 현재 4학년 재학 | 학점(전공): 3.0 / 4.5',
        '관련 과목: 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 자료구조, 알고리즘, 확률 및 통계',
      ],
    },
  ],

  activities: [
    {
      period: '2025. 03 - 2025. 12',
      org: '한양대학교',
      title: '인공지능학과 AI 학술동아리',
      bullets: [
        '머신러닝·딥러닝 논문 및 기술 스터디',
        'PyTorch를 활용한 CNN, RNN, Transformer 모델 구현',
        'Hugging Face 기반 사전학습 모델 Fine-tuning 실습',
      ],
    },
    {
      period: '2025. 07 - 2025. 08',
      org: '교내 AI Summer Study',
      title: '생성형 AI & LLM 스터디',
      bullets: [
        'Transformer 및 LLM 구조 학습',
        'Prompt Engineering 및 RAG 구조 실습',
        'LangChain을 활용한 간단한 LLM Application 개발',
      ],
    },
  ],

  skills: [
    { category: 'Programming Language', items: ['Python', 'C++'] },
    {
      category: 'AI / ML',
      items: ['PyTorch', 'Scikit-Learn', 'Hugging Face Transformers', 'NLP', 'Computer Vision', 'LLM', 'RAG'],
    },
    {
      category: 'Tools',
      items: ['Git', 'GitHub', 'Docker', 'FastAPI', 'Streamlit', 'Jupyter Notebook'],
    },
  ],

  projects: [
    {
      period: '2026. 03 - 2026. 05',
      org: '팀 프로젝트',
      title: '한양대 학사정보 RAG 챗봇',
      bullets: [
        '한양대학교 학사 안내 문서와 학과 정보를 검색하여 질문에 답변하는 RAG 기반 챗봇 개발',
        '학사 공지 및 PDF 문서를 Chunk 단위로 분할하고 Embedding하여 Vector DB에 저장',
        '사용자 질문과 관련된 문서를 검색한 뒤 LLM이 해당 문서를 기반으로 답변하도록 RAG Pipeline 구현',
        '검색 결과의 정확도를 개선하기 위해 Chunk Size 및 Top-K 값에 따른 성능 비교',
        'FastAPI와 Streamlit을 활용하여 간단한 웹 기반 데모 구현',
      ],
      techStack: ['Python', 'LangChain', 'Hugging Face', 'FAISS', 'FastAPI', 'Streamlit'],
      github: 'https://github.com/example-hanyang-ai/hyu-rag-chatbot',
    },
    {
      period: '2025. 09 - 2025. 12',
      org: '팀 프로젝트',
      title: '딥러닝 기반 음식 이미지 분류 및 영양정보 추천 시스템',
      bullets: [
        '음식 이미지를 입력받아 음식 종류를 분류하고 관련 영양정보를 제공하는 AI 서비스 개발',
        '공개 음식 이미지 데이터셋을 활용하여 데이터 전처리 및 Augmentation 수행',
        'ResNet 기반 Transfer Learning을 적용하여 이미지 분류 모델 구축',
        'Accuracy, Precision, Recall, F1-score를 활용하여 모델 성능 평가',
        '학습된 모델을 API 형태로 구성하고 웹 인터페이스에서 이미지 업로드 및 추론이 가능하도록 구현',
      ],
      techStack: ['Python', 'PyTorch', 'torchvision', 'ResNet', 'FastAPI', 'Streamlit'],
      github: 'https://github.com/example-hanyang-ai/food-vision-demo',
    },
  ],
};
