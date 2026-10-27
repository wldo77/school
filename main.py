
import streamlit as st
import pandas as pd
import html
import re

# =========================================================
# 1. 기본 설정
# =========================================================
st.set_page_config(
    page_title="나의 과목 선택 가이드",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = [
    "🏠 홈",
    "📚 분야별 과목",
    "🔎 과목 검색",
    "⭐ 관심 과목",
    "💬 수강후기",
    "🧭 선택 가이드",
]

# =========================================================
# 2. 과목 데이터
# ※ 학교별 개설 과목과 교육과정은 다를 수 있습니다.
# =========================================================
COURSES = [
    {
        "name": "공통국어",
        "field": "국어",
        "kind": "일반 선택",
        "intro": "다양한 글과 담화를 읽고 이해하며 자신의 생각을 표현하는 과목입니다.",
        "goals": "읽기, 쓰기, 말하기, 듣기 능력을 기르고 비판적으로 사고합니다.",
        "careers": ["인문", "교육", "언론", "문화"],
        "level": "기초",
        "topics": ["독서", "글쓰기", "토론", "의사소통"],
    },
    {
        "name": "화법과 언어",
        "field": "국어",
        "kind": "일반 선택",
        "intro": "언어의 특징을 이해하고 상황에 맞게 효과적으로 소통하는 과목입니다.",
        "goals": "언어생활을 탐구하고 목적과 상황에 적합한 의사소통 능력을 기릅니다.",
        "careers": ["인문", "교육", "언론"],
        "level": "보통",
        "topics": ["토론", "언어", "의사소통"],
    },
    {
        "name": "독서와 작문",
        "field": "국어",
        "kind": "일반 선택",
        "intro": "다양한 자료를 읽고 정보를 정리하여 자신의 글로 표현합니다.",
        "goals": "정보를 분석하고 논리적으로 글을 구성하는 능력을 기릅니다.",
        "careers": ["인문", "언론", "문화", "교육"],
        "level": "보통",
        "topics": ["독서", "글쓰기", "탐구"],
    },
    {
        "name": "문학",
        "field": "국어",
        "kind": "일반 선택",
        "intro": "시, 소설, 희곡 등 문학 작품을 감상하고 작품의 의미를 탐구합니다.",
        "goals": "문학적 감수성과 상상력을 기르고 다양한 삶의 모습을 이해합니다.",
        "careers": ["인문", "문화", "예술", "교육"],
        "level": "보통",
        "topics": ["독서", "문화", "예술"],
    },
    {
        "name": "수학",
        "field": "수학",
        "kind": "일반 선택",
        "intro": "수학의 기본 개념과 원리를 이해하고 문제 해결에 활용합니다.",
        "goals": "수학적 사고력, 추론 능력, 문제 해결 능력을 기릅니다.",
        "careers": ["공학", "자연과학", "정보", "경제"],
        "level": "기초",
        "topics": ["문제 해결", "데이터", "논리"],
    },
    {
        "name": "대수",
        "field": "수학",
        "kind": "일반 선택",
        "intro": "식과 방정식, 함수 등 대수의 주요 개념을 탐구합니다.",
        "goals": "대수적 표현과 계산을 이해하고 수학적 문제에 적용합니다.",
        "careers": ["공학", "자연과학", "정보"],
        "level": "보통",
        "topics": ["문제 해결", "논리"],
    },
    {
        "name": "미적분Ⅰ",
        "field": "수학",
        "kind": "일반 선택",
        "intro": "함수의 변화와 누적을 수학적으로 이해하는 과목입니다.",
        "goals": "극한, 미분, 적분과 관련된 개념을 이해하고 활용합니다.",
        "careers": ["공학", "자연과학", "정보"],
        "level": "도전",
        "topics": ["문제 해결", "논리"],
    },
    {
        "name": "확률과 통계",
        "field": "수학",
        "kind": "일반 선택",
        "intro": "불확실한 상황과 자료를 확률 및 통계로 분석합니다.",
        "goals": "자료를 해석하고 합리적인 판단을 내리는 능력을 기릅니다.",
        "careers": ["경제", "사회", "정보", "자연과학"],
        "level": "보통",
        "topics": ["데이터", "탐구", "문제 해결"],
    },
    {
        "name": "기하",
        "field": "수학",
        "kind": "진로 선택",
        "intro": "도형과 공간의 성질을 수학적으로 탐구합니다.",
        "goals": "공간 감각과 기하적 추론 능력을 기르고 관련 문제를 해결합니다.",
        "careers": ["공학", "자연과학", "건축"],
        "level": "도전",
        "topics": ["논리", "문제 해결"],
    },
    {
        "name": "영어",
        "field": "영어",
        "kind": "일반 선택",
        "intro": "영어로 된 자료를 이해하고 다양한 상황에서 의사소통합니다.",
        "goals": "영어 듣기, 말하기, 읽기, 쓰기 능력을 기릅니다.",
        "careers": ["언론", "교육", "국제", "관광"],
        "level": "기초",
        "topics": ["의사소통", "문화", "독서"],
    },
    {
        "name": "영어Ⅰ",
        "field": "영어",
        "kind": "일반 선택",
        "intro": "다양한 주제의 영어 자료를 이해하고 활용합니다.",
        "goals": "영어 의사소통 능력과 자기주도적 학습 능력을 기릅니다.",
        "careers": ["국제", "교육", "언론", "관광"],
        "level": "보통",
        "topics": ["의사소통", "문화", "독서"],
    },
    {
        "name": "세계사",
        "field": "사회",
        "kind": "일반 선택",
        "intro": "세계 여러 지역의 역사적 변화와 상호작용을 탐구합니다.",
        "goals": "역사적 사고력을 기르고 현재 사회를 다양한 관점에서 이해합니다.",
        "careers": ["역사", "교육", "국제", "문화"],
        "level": "보통",
        "topics": ["역사", "문화", "탐구"],
    },
    {
        "name": "사회와 문화",
        "field": "사회",
        "kind": "일반 선택",
        "intro": "사회 현상과 문화의 특징을 자료를 통해 분석합니다.",
        "goals": "사회 현상을 탐구하고 다양한 사회·문화적 관점을 이해합니다.",
        "careers": ["사회", "교육", "언론", "행정"],
        "level": "보통",
        "topics": ["사회", "탐구", "데이터"],
    },
    {
        "name": "경제",
        "field": "사회",
        "kind": "일반 선택",
        "intro": "시장과 경제생활에서 나타나는 현상을 탐구합니다.",
        "goals": "경제 원리를 이해하고 합리적인 경제적 의사결정 능력을 기릅니다.",
        "careers": ["경제", "경영", "금융", "행정"],
        "level": "보통",
        "topics": ["데이터", "사회", "문제 해결"],
    },
    {
        "name": "정치와 법",
        "field": "사회",
        "kind": "일반 선택",
        "intro": "정치 과정과 법의 원리를 이해하고 사회 문제를 살펴봅니다.",
        "goals": "민주시민으로서 필요한 판단력과 참여 역량을 기릅니다.",
        "careers": ["법", "행정", "정치", "사회"],
        "level": "보통",
        "topics": ["사회", "토론", "탐구"],
    },
    {
        "name": "통합과학",
        "field": "과학",
        "kind": "일반 선택",
        "intro": "물리, 화학, 생명과학, 지구과학의 기초 개념을 연결합니다.",
        "goals": "자연 현상을 과학적으로 탐구하고 여러 과학 분야를 통합적으로 이해합니다.",
        "careers": ["자연과학", "공학", "보건", "환경"],
        "level": "기초",
        "topics": ["탐구", "환경", "문제 해결"],
    },
    {
        "name": "물리학",
        "field": "과학",
        "kind": "진로 선택",
        "intro": "운동, 에너지, 전기 등 자연 현상의 원리를 탐구합니다.",
        "goals": "물리 개념과 법칙을 이해하고 이를 실제 현상에 적용합니다.",
        "careers": ["공학", "자연과학", "전자"],
        "level": "도전",
        "topics": ["탐구", "문제 해결", "논리"],
    },
    {
        "name": "화학",
        "field": "과학",
        "kind": "진로 선택",
        "intro": "물질의 구조와 성질, 화학 반응을 탐구합니다.",
        "goals": "물질과 반응에 관한 개념을 이해하고 과학적 탐구 능력을 기릅니다.",
        "careers": ["화학", "보건", "환경", "공학"],
        "level": "도전",
        "topics": ["탐구", "환경", "문제 해결"],
    },
    {
        "name": "생명과학",
        "field": "과학",
        "kind": "진로 선택",
        "intro": "생명체의 구조와 기능, 생명 현상의 원리를 탐구합니다.",
        "goals": "생명 현상을 이해하고 생명과학 관련 문제를 탐구합니다.",
        "careers": ["생명과학", "보건", "의료", "환경"],
        "level": "보통",
        "topics": ["탐구", "환경", "보건"],
    },
    {
        "name": "지구과학",
        "field": "과학",
        "kind": "진로 선택",
        "intro": "지구와 우주에서 나타나는 여러 현상을 탐구합니다.",
        "goals": "지구 시스템과 우주를 이해하고 자료를 분석하는 능력을 기릅니다.",
        "careers": ["환경", "자연과학", "기상", "우주"],
        "level": "보통",
        "topics": ["탐구", "환경", "데이터"],
    },
    {
        "name": "정보",
        "field": "정보·기술·가정",
        "kind": "일반 선택",
        "intro": "컴퓨팅 사고와 정보 기술을 활용하여 문제를 해결합니다.",
        "goals": "자료와 알고리즘을 이해하고 디지털 문제 해결 능력을 기릅니다.",
        "careers": ["정보", "공학", "데이터", "게임"],
        "level": "보통",
        "topics": ["데이터", "문제 해결", "프로젝트"],
    },
    {
        "name": "인공지능 기초",
        "field": "정보·기술·가정",
        "kind": "진로 선택",
        "intro": "인공지능의 기본 원리와 활용 사례를 이해합니다.",
        "goals": "인공지능 기술을 이해하고 사회적 영향과 활용 방안을 탐구합니다.",
        "careers": ["정보", "데이터", "공학", "게임"],
        "level": "도전",
        "topics": ["데이터", "프로젝트", "탐구"],
    },
    {
        "name": "기술·가정",
        "field": "정보·기술·가정",
        "kind": "일반 선택",
        "intro": "기술과 가정생활의 원리를 이해하고 생활 문제를 해결합니다.",
        "goals": "실생활 문제 해결 능력과 지속가능한 생활 역량을 기릅니다.",
        "careers": ["공학", "생활", "디자인", "환경"],
        "level": "기초",
        "topics": ["프로젝트", "환경", "문제 해결"],
    },
    {
        "name": "음악",
        "field": "예술",
        "kind": "일반 선택",
        "intro": "다양한 음악을 감상하고 표현하며 음악의 가치를 이해합니다.",
        "goals": "음악적 표현과 감상 능력을 기르고 문화적 소양을 넓힙니다.",
        "careers": ["예술", "문화", "교육", "공연"],
        "level": "기초",
        "topics": ["예술", "문화", "프로젝트"],
    },
    {
        "name": "미술",
        "field": "예술",
        "kind": "일반 선택",
        "intro": "시각적으로 표현하고 작품을 감상하며 미술 문화를 탐구합니다.",
        "goals": "창의적 표현 능력과 시각적 소통 능력을 기릅니다.",
        "careers": ["예술", "디자인", "문화", "콘텐츠"],
        "level": "기초",
        "topics": ["예술", "문화", "프로젝트"],
    },
    {
        "name": "일본어",
        "field": "제2외국어·한문",
        "kind": "일반 선택",
        "intro": "일본어의 기초 표현과 일본의 생활 문화를 이해합니다.",
        "goals": "기초적인 의사소통 능력과 문화 간 이해 능력을 기릅니다.",
        "careers": ["국제", "관광", "언어", "문화"],
        "level": "기초",
        "topics": ["의사소통", "문화"],
    },
    {
        "name": "중국어",
        "field": "제2외국어·한문",
        "kind": "일반 선택",
        "intro": "중국어의 기초 표현과 중국어권 문화를 이해합니다.",
        "goals": "기초적인 중국어 의사소통 능력과 문화 이해 능력을 기릅니다.",
        "careers": ["국제", "관광", "언어", "문화"],
        "level": "기초",
        "topics": ["의사소통", "문화"],
    },
    {
        "name": "철학",
        "field": "교양",
        "kind": "융합 선택",
        "intro": "인간과 세계, 지식과 가치에 관한 다양한 질문을 탐구합니다.",
        "goals": "논리적으로 질문하고 근거를 바탕으로 자신의 생각을 구성합니다.",
        "careers": ["인문", "교육", "사회", "문화"],
        "level": "보통",
        "topics": ["토론", "논리", "탐구"],
    },
    {
        "name": "환경",
        "field": "교양",
        "kind": "융합 선택",
        "intro": "환경 문제와 지속가능한 사회를 다양한 관점에서 살펴봅니다.",
        "goals": "환경 문제를 탐구하고 지속가능한 삶을 위한 실천 방안을 고민합니다.",
        "careers": ["환경", "과학", "사회", "공학"],
        "level": "보통",
        "topics": ["환경", "탐구", "프로젝트"],
    },
    {
        "name": "체육",
        "field": "체육",
        "kind": "일반 선택",
        "intro": "신체 활동에 참여하며 건강과 운동 능력을 기릅니다.",
        "goals": "건강한 생활 습관과 안전한 신체 활동 태도를 기릅니다.",
        "careers": ["체육", "보건", "교육", "스포츠"],
        "level": "기초",
        "topics": ["건강", "프로젝트"],
    },
]

FIELDS = list(dict.fromkeys(c["field"] for c in COURSES))
COURSE_NAMES = [c["name"] for c in COURSES]

# =========================================================
# 3. 세션 상태 초기화
# =========================================================
DEFAULTS = {
    "page": "🏠 홈",
    "favorites": [],
    "reviews": [],
    "selected_course": None,
    "detail_open": False,
    "toast_message": "",
    "guide_results": [],
    "guide_done": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_page(page):
    """페이지 상태만 변경합니다. 위젯 상태를 직접 수정하지 않습니다."""
    if page not in PAGES:
        page = "🏠 홈"
    st.session_state.page = page
    st.rerun()


def toggle_favorite(name):
    favorites = list(st.session_state.favorites)
    if name in favorites:
        favorites.remove(name)
        st.session_state.toast_message = f"⭐ {name} 과목을 관심 목록에서 뺐어요."
    else:
        favorites.append(name)
        st.session_state.toast_message = f"⭐ {name} 과목을 관심 목록에 담았어요."
    st.session_state.favorites = favorites


def open_detail(name):
    st.session_state.selected_course = name
    st.session_state.detail_open = True


def close_detail():
    st.session_state.detail_open = False
    st.session_state.selected_course = None


def get_course(name):
    return next((c for c in COURSES if c["name"] == name), None)


def key_safe(value):
    return re.sub(r"[^0-9a-zA-Z가-힣_-]", "_", str(value))


# =========================================================
# 4. 디자인
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap');

    :root {
        --cream: #fbf8ed;
        --green: #47785a;
        --green-dark: #2f5940;
        --green-light: #e8f1e5;
        --yellow: #f4d879;
        --ink: #28382c;
    }

    html, body, [class*="css"] {
        font-family: 'Gowun Dodum', sans-serif;
    }

    .stApp {
        background: var(--cream);
        color: var(--ink);
    }

    h1, h2, h3 {
        font-family: 'Jua', sans-serif !important;
        color: var(--green-dark);
    }

    h1 { font-size: 2.35rem !important; }
    h2 { font-size: 1.75rem !important; }
    h3 { font-size: 1.3rem !important; }

    p, label, li, .stMarkdown {
        font-size: 1.04rem;
        line-height: 1.65;
    }

    [data-testid="stSidebar"] {
        background: #eef3e6;
        border-right: 1px solid #d6e1d1;
    }

    [data-testid="stSidebar"] button {
        width: 100%;
        min-height: 46px;
        border-radius: 8px !important;
        border: 1px solid #cbd9c8 !important;
        background: #fffdf6 !important;
        color: #2f5940 !important;
        text-align: left !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 5px !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] button:hover {
        background: #dcebd8 !important;
        border-color: #47785a !important;
    }

    .hero {
        background: linear-gradient(125deg, #e5efdc, #fff4cb);
        padding: 28px;
        border-radius: 20px;
        border: 1px solid #dbe5d2;
        margin-bottom: 20px;
    }

    .hero h1 {
        margin-top: 0;
        margin-bottom: 8px;
    }

    .soft-card {
        background: #fffdf7;
        border: 1px solid #e0e5d7;
        border-radius: 15px;
        padding: 18px;
        margin: 8px 0;
    }

    .course-name {
        color: #2f5940;
        font-family: 'Jua', sans-serif;
        font-size: 1.28rem;
        margin-bottom: 4px;
    }

    .tag {
        display: inline-block;
        background: #e8f1e5;
        color: #2f5940;
        border-radius: 6px;
        padding: 3px 8px;
        margin: 3px 4px 3px 0;
        font-size: 0.88rem;
    }

    .notice {
        background: #fff5cf;
        border-left: 5px solid #e5c455;
        padding: 12px 15px;
        border-radius: 8px;
        margin: 12px 0;
    }

    .toast {
        position: fixed;
        bottom: 22px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 999999;
        background: #2f5940;
        color: white;
        padding: 12px 22px;
        border-radius: 12px;
        box-shadow: 0 5px 18px #0002;
        animation: toast-in 0.25s ease-out, toast-out 0.5s ease-in 2.5s forwards;
        font-size: 1rem;
    }

    @keyframes toast-in {
        from { opacity: 0; transform: translate(-50%, 12px); }
        to { opacity: 1; transform: translate(-50%, 0); }
    }

    @keyframes toast-out {
        to { opacity: 0; visibility: hidden; }
    }

    div.stButton > button {
        border-radius: 9px;
        font-size: 1rem;
        min-height: 42px;
    }

    div.stButton > button[kind="primary"] {
        background: #47785a;
        border-color: #47785a;
        color: white;
    }

    [data-testid="stMetric"] {
        background: #fffdf7;
        border: 1px solid #e0e5d7;
        padding: 14px;
        border-radius: 12px;
    }

    hr {
        border-color: #dce4d5;
    }

    a {
        color: #356747 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 5. 사이드바 메뉴
# 중요: st.radio와 main_navigation 상태를 사용하지 않습니다.
# =========================================================
with st.sidebar:
    st.markdown("# 🌱 과목 선택 가이드")
    st.caption("나에게 맞는 과목을 천천히 찾아봐요.")
    st.divider()

    for page_name in PAGES:
        is_current = st.session_state.page == page_name
        button_label = f"▶  {page_name}" if is_current else page_name

        if st.button(
            button_label,
            key=f"nav_{key_safe(page_name)}",
            use_container_width=True,
            type="primary" if is_current else "secondary",
        ):
            st.session_state.page = page_name
            st.session_state.detail_open = False
            st.session_state.selected_course = None
            st.rerun()

    st.divider()
    st.markdown("### ⭐ 관심 과목")
    st.write(f"현재 {len(st.session_state.favorites)}개 과목을 저장했어요.")

    st.caption("과목 정보는 이해를 돕기 위한 요약입니다.")

# =========================================================
# 6. 공통 과목 카드
# =========================================================
def render_course_card(course, prefix="course"):
    name = course["name"]
    is_favorite = name in st.session_state.favorites

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)

    left, star_col = st.columns([5, 1])

    with left:
        st.markdown(f'<div class="course-name">{html.escape(name)}</div>', unsafe_allow_html=True)
        st.caption(f'{course["field"]} · {course["kind"]}')
        st.write(course["intro"])

        tags_html = "".join(
            f'<span class="tag">{html.escape(tag)}</span>'
            for tag in course["careers"]
        )
        st.markdown(tags_html, unsafe_allow_html=True)

    with star_col:
        star = "⭐" if is_favorite else "☆"
        if st.button(
            star,
            key=f"{prefix}_star_{key_safe(name)}",
            help="관심 과목 추가 또는 해제",
            use_container_width=True,
        ):
            toggle_favorite(name)
            st.rerun()

    if st.button(
        "과목 상세 보기 →",
        key=f"{prefix}_detail_{key_safe(name)}",
        use_container_width=True,
    ):
        open_detail(name)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_review_list(course_name=None):
    reviews = st.session_state.reviews

    if course_name:
        reviews = [r for r in reviews if r["course"] == course_name]

    if not reviews:
        st.info("아직 등록된 수강후기가 없어요. 첫 후기를 남겨 보세요!")
        return

    for i, review in enumerate(reversed(reviews)):
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown(f"**📚 {html.escape(review['course'])}**")
        st.write(f"⭐ 추천도: {review['rating']} / 5")
        st.write(review["text"])
        if review.get("advice"):
            st.caption("💡 조언: " + review["advice"])
        st.caption("후기 작성자가 입력한 정보이며, 개인 경험에 따라 다를 수 있어요.")
        st.markdown("</div>", unsafe_allow_html=True)


def render_review_form(course_name, form_prefix="review"):
    with st.form(f"{form_prefix}_{key_safe(course_name)}"):
        st.markdown("#### ✏️ 수강후기 남기기")
        rating = st.slider("이 과목을 추천하는 정도", 1, 5, 4, key=f"{form_prefix}_rating_{key_safe(course_name)}")
        review_text = st.text_area(
            "과목을 들으며 느낀 점",
            placeholder="어떤 내용을 배웠는지, 어떤 학생에게 잘 맞을지 적어 주세요.",
            key=f"{form_prefix}_text_{key_safe(course_name)}",
        )
        advice = st.text_input(
            "후배에게 해 주고 싶은 조언 (선택)",
            key=f"{form_prefix}_advice_{key_safe(course_name)}",
        )
        submitted = st.form_submit_button("후기 등록하기", use_container_width=True)

    if submitted:
        if not review_text.strip():
            st.warning("후기 내용을 먼저 입력해 주세요.")
        else:
            st.session_state.reviews.append({
                "course": course_name,
                "rating": rating,
                "text": review_text.strip(),
                "advice": advice.strip(),
            })
            st.success("후기가 등록되었어요!")
            st.rerun()


def render_detail_panel():
    name = st.session_state.selected_course
    course = get_course(name) if name else None

    if not st.session_state.detail_open or not course:
        st.info("왼쪽에서 과목을 선택하면 상세 정보가 여기에 표시돼요.")
        return

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown(f"## 📖 {html.escape(course['name'])}")
    st.caption(f"{course['field']} · {course['kind']} · 학습 수준 참고: {course['level']}")
    st.write(course["intro"])

    st.markdown("### 🎯 무엇을 배우나요?")
    st.write(course["goals"])

    st.markdown("### 🧭 관련 관심 분야")
    st.write(" · ".join(course["careers"]))

    st.markdown("### 💡 이런 점을 생각해 보세요")
    st.write(
        "이 과목에서 다루는 주제에 흥미가 있는지, 현재 학습 준비도와 "
        "앞으로의 진로 탐색에 도움이 되는지를 함께 고려해 보세요."
    )

    if course["name"] in st.session_state.favorites:
        if st.button("⭐ 관심 과목에서 빼기", key=f"detail_remove_{key_safe(course['name'])}"):
            toggle_favorite(course["name"])
            st.rerun()
    else:
        if st.button("☆ 관심 과목에 담기", key=f"detail_add_{key_safe(course['name'])}"):
            toggle_favorite(course["name"])
            st.rerun()

    st.markdown("### 💬 이 과목의 수강후기")
    render_review_list(course["name"])
    render_review_form(course["name"], "detail_review")

    st.markdown("### 🔗 공식 교육과정 확인")
    st.write("과목의 정확한 성취기준과 편성 여부는 공식 자료 및 학교 교육과정에서 확인하세요.")
    st.markdown("- [국가교육과정정보센터(NCIC)](https://www.ncic.re.kr/)")
    st.markdown("- [고교학점제 안내](https://www.hscredit.kr/)")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✕ 상세 패널 닫기", key="close_detail_panel", use_container_width=True):
        close_detail()
        st.rerun()


def render_course_list_with_detail(courses, prefix="list"):
    if st.session_state.detail_open and st.session_state.selected_course:
        left, right = st.columns([1.05, 0.95], gap="large")
        with left:
            st.markdown("### 📚 과목 목록")
            if not courses:
                st.info("조건에 맞는 과목이 없어요.")
            for course in courses:
                render_course_card(course, prefix)
        with right:
            st.markdown("### 🔎 과목 상세")
            render_detail_panel()
    else:
        if not courses:
            st.info("조건에 맞는 과목이 없어요.")
        for course in courses:
            render_course_card(course, prefix)


# =========================================================
# 7. 홈
# =========================================================
page = st.session_state.page

if page == "🏠 홈":
    st.markdown(
        """
        <div class="hero">
            <h1>🌱 나에게 맞는 과목 찾기</h1>
            <p>관심 분야와 배우고 싶은 내용을 바탕으로 과목을 탐색해 보세요.</p>
            <p>정답을 찾기보다 나에게 맞는 선택의 이유를 알아가는 것이 중요해요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("과목 정보", f"{len(COURSES)}개")
    m2.metric("관심 과목", f"{len(st.session_state.favorites)}개")
    m3.metric("등록된 후기", f"{len(st.session_state.reviews)}개")

    st.markdown("## 어디서 시작할까요?")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("### 📚 분야별 과목 보기")
        st.write("국어, 수학, 사회, 과학 등 분야별로 과목을 살펴봐요.")
        if st.button("분야별 과목 보기 →", key="home_go_fields", use_container_width=True):
            go_page("📚 분야별 과목")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("### 🔎 과목 검색하기")
        st.write("과목명이나 관심 주제로 원하는 과목을 찾아봐요.")
        if st.button("과목 검색하기 →", key="home_go_search", use_container_width=True):
            go_page("🔎 과목 검색")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## ✨ 과목 선택 전에 생각해 보기")
    st.markdown(
        """
        - 어떤 주제를 배우면 시간이 빠르게 지나가나요?
        - 지금 배우는 내용 중 더 깊게 탐구하고 싶은 것은 무엇인가요?
        - 희망 진로와 연결되는 과목이 있나요?
        - 학교에서 실제로 개설하는 과목인지 확인했나요?
        """
    )

    st.markdown(
        '<div class="notice">과목 이름과 선택 유형은 학교와 교육과정 편성에 따라 다를 수 있어요. '
        '최종 선택 전에는 학교의 과목 안내 자료와 담당 선생님의 안내를 확인하세요.</div>',
        unsafe_allow_html=True,
    )

# =========================================================
# 8. 분야별 과목
# =========================================================
elif page == "📚 분야별 과목":
    st.title("📚 분야별 과목")
    st.write("관심 있는 분야와 과목 유형을 골라 살펴보세요.")

    c1, c2 = st.columns(2)
    with c1:
        selected_field = st.selectbox("과목 분야", ["전체"] + FIELDS, key="field_filter")
    with c2:
        selected_kind = st.selectbox(
            "과목 유형",
            ["전체", "일반 선택", "진로 선택", "융합 선택"],
            key="kind_filter",
        )

    filtered = COURSES[:]
    if selected_field != "전체":
        filtered = [c for c in filtered if c["field"] == selected_field]
    if selected_kind != "전체":
        filtered = [c for c in filtered if c["kind"] == selected_kind]

    st.caption(f"검색 결과: {len(filtered)}개 과목")
    render_course_list_with_detail(filtered, "field")

# =========================================================
# 9. 과목 검색
# =========================================================
elif page == "🔎 과목 검색":
    st.title("🔎 과목 검색")
    st.write("과목명, 배우는 내용, 진로 분야, 관심 주제로 검색할 수 있어요.")

    query = st.text_input(
        "검색어",
        placeholder="예: 데이터, 생명과학, 글쓰기, 환경",
        key="course_search_query",
    )
    field_filter = st.selectbox("분야 필터", ["전체"] + FIELDS, key="search_field_filter")
    kind_filter = st.selectbox(
        "유형 필터",
        ["전체", "일반 선택", "진로 선택", "융합 선택"],
        key="search_kind_filter",
    )

    results = []
    for course in COURSES:
        searchable = " ".join([
            course["name"],
            course["field"],
            course["kind"],
            course["intro"],
            course["goals"],
            " ".join(course["careers"]),
            " ".join(course["topics"]),
        ]).lower()

        if query.strip() and query.strip().lower() not in searchable:
            continue
        if field_filter != "전체" and course["field"] != field_filter:
            continue
        if kind_filter != "전체" and course["kind"] != kind_filter:
            continue
        results.append(course)

    st.caption(f"검색 결과: {len(results)}개 과목")
    render_course_list_with_detail(results, "search")

# =========================================================
# 10. 관심 과목
# =========================================================
elif page == "⭐ 관심 과목":
    st.title("⭐ 나의 관심 과목")
    st.write("별표를 눌러 저장한 과목을 모아 볼 수 있어요.")

    favorite_courses = [
        c for c in COURSES
        if c["name"] in st.session_state.favorites
    ]

    if not favorite_courses:
        st.info("아직 저장한 과목이 없어요. 분야별 과목이나 검색 페이지에서 ☆를 눌러 추가해 보세요.")
        if st.button("과목 찾아보기 →", key="favorites_go_fields"):
            go_page("📚 분야별 과목")
    else:
        render_course_list_with_detail(favorite_courses, "favorites")

# =========================================================
# 11. 수강후기
# =========================================================
elif page == "💬 수강후기":
    st.title("💬 수강후기와 조언")
    st.write("과목을 먼저 경험한 학생들의 의견을 공유하는 공간이에요.")

    review_course = st.selectbox(
        "후기를 남길 과목",
        COURSE_NAMES,
        key="general_review_course",
    )
    render_review_form(review_course, "general_review")

    st.divider()
    st.markdown("## 🗣️ 등록된 후기")
    review_filter = st.selectbox(
        "과목별로 보기",
        ["전체"] + COURSE_NAMES,
        key="review_filter",
    )

    if review_filter == "전체":
        render_review_list()
    else:
        render_review_list(review_filter)

    st.markdown(
        '<div class="notice">후기는 개인의 경험과 의견입니다. 수업 내용이나 난이도는 '
        '학교와 담당 교사, 학년도에 따라 달라질 수 있어요.</div>',
        unsafe_allow_html=True,
    )

# =========================================================
# 12. 선택 가이드
# =========================================================
elif page == "🧭 선택 가이드":
    st.title("🧭 나에게 맞는 과목 선택 가이드")
    st.write("몇 가지 질문에 답하면 응답에 맞는 과목을 추천해 드려요.")

    with st.form("course_guide_form"):
        st.markdown("### 1. 어떤 유형의 과목을 찾고 있나요?")
        kinds = st.multiselect(
            "복수 선택 가능",
            ["일반 선택", "진로 선택", "융합 선택"],
            default=["일반 선택", "진로 선택", "융합 선택"],
            help="아직 잘 모르겠다면 세 가지를 모두 선택해도 괜찮아요.",
        )

        st.markdown("### 2. 관심 있는 분야는 무엇인가요?")
        interests = st.multiselect(
            "관심 분야",
            [
                "인문", "교육", "언론", "문화", "공학", "자연과학",
                "정보", "데이터", "경제", "경영", "사회", "법",
                "국제", "환경", "보건", "의료", "예술", "디자인",
                "체육", "관광", "생명과학",
            ],
        )

        st.markdown("### 3. 어떤 주제를 배우고 싶나요?")
        topics = st.multiselect(
            "관심 주제",
            [
                "독서", "글쓰기", "토론", "의사소통", "문제 해결",
                "데이터", "논리", "탐구", "환경", "문화", "예술",
                "프로젝트", "건강", "보건", "역사", "사회",
            ],
        )

        st.markdown("### 4. 현재 나에게 중요한 기준은 무엇인가요?")
        priorities = st.multiselect(
            "중요한 기준 (최대 3개)",
            [
                "흥미와 호기심",
                "희망 진로와의 연결",
                "기초 개념과 학습 준비",
                "새로운 분야 경험",
                "탐구와 프로젝트",
                "다른 과목과의 연계",
            ],
            default=["흥미와 호기심"],
        )

        st.markdown("### 5. 어떤 학습 방식이 잘 맞나요?")
        learning_style = st.radio(
            "가장 선호하는 방식",
            [
                "개념을 차근차근 배우기",
                "자료를 읽고 분석하기",
                "문제를 해결하고 계산하기",
                "토론하고 의견 나누기",
                "직접 만들고 프로젝트 하기",
                "아직 잘 모르겠어요",
            ],
        )

        st.markdown("### 6. 어느 정도의 도전을 원하나요?")
        challenge = st.radio(
            "학습 도전 수준",
            [
                "기초를 탄탄히 다지고 싶어요",
                "익숙한 내용과 새로운 내용을 함께 배우고 싶어요",
                "관심 분야를 깊이 탐구하고 싶어요",
            ],
        )

        submitted_guide = st.form_submit_button(
            "나에게 맞는 과목 추천받기 🌱",
            use_container_width=True,
            type="primary",
        )

    if submitted_guide:
        scored = []

        for course in COURSES:
            if kinds and course["kind"] not in kinds:
                continue

            score = 0
            reasons = []

            interest_matches = set(interests) & set(course["careers"])
            topic_matches = set(topics) & set(course["topics"])

            if interest_matches:
                score += len(interest_matches) * 3
                reasons.append("관심 분야와 연결돼요")

            if topic_matches:
                score += len(topic_matches) * 2
                reasons.append("배우고 싶은 주제를 포함해요")

            if "흥미와 호기심" in priorities and (interest_matches or topic_matches):
                score += 1

            if "희망 진로와의 연결" in priorities and interest_matches:
                score += 2

            if "기초 개념과 학습 준비" in priorities and course["level"] == "기초":
                score += 3
                reasons.append("기초를 다지는 데 도움이 될 수 있어요")

            if "새로운 분야 경험" in priorities:
                score += 1

            if "탐구와 프로젝트" in priorities and (
                "탐구" in course["topics"] or "프로젝트" in course["topics"]
            ):
                score += 2
                reasons.append("탐구 활동과 연결돼요")

            if "다른 과목과의 연계" in priorities:
                score += 1

            if learning_style == "개념을 차근차근 배우기" and course["level"] == "기초":
                score += 2
            elif learning_style == "자료를 읽고 분석하기" and (
                "독서" in course["topics"] or "데이터" in course["topics"]
            ):
                score += 2
            elif learning_style == "문제를 해결하고 계산하기" and (
                "문제 해결" in course["topics"] or "논리" in course["topics"]
            ):
                score += 2
            elif learning_style == "토론하고 의견 나누기" and (
                "토론" in course["topics"] or "의사소통" in course["topics"]
            ):
                score += 2
            elif learning_style == "직접 만들고 프로젝트 하기" and "프로젝트" in course["topics"]:
                score += 2

            if challenge == "기초를 탄탄히 다지고 싶어요" and course["level"] == "기초":
                score += 3
            elif (
                challenge == "관심 분야를 깊이 탐구하고 싶어요"
                and course["kind"] in ["진로 선택", "융합 선택"]
            ):
                score += 2
            elif (
                challenge == "익숙한 내용과 새로운 내용을 함께 배우고 싶어요"
                and course["level"] == "보통"
            ):
                score += 2

            if not reasons:
                reasons.append("과목 소개를 읽고 관심이 가는지 확인해 보세요")

            scored.append((score, course, reasons))

        scored.sort(key=lambda item: (-item[0], item[1]["name"]))
        st.session_state.guide_results = scored[:8]
        st.session_state.guide_done = True
        st.session_state.detail_open = False
        st.session_state.selected_course = None

    if st.session_state.guide_done:
        st.divider()
        st.markdown("## 🌟 추천 과목")

        if not st.session_state.guide_results:
            st.info("선택한 조건에 맞는 과목이 없어요. 과목 유형을 더 선택해 보세요.")
        else:
            st.caption(
                "추천 순서는 입력한 관심사에 따른 참고 결과예요. "
                "성적, 난이도, 학교 개설 여부를 확정적으로 예측하지 않습니다."
            )

            recommended_courses = [
                item[1] for item in st.session_state.guide_results
            ]

            for score, course, reasons in st.session_state.guide_results:
                st.markdown('<div class="soft-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="course-name">🌱 {html.escape(course["name"])}</div>', unsafe_allow_html=True)
                st.caption(f'{course["field"]} · {course["kind"]}')
                st.write(course["intro"])
                st.write("추천 이유: " + " · ".join(reasons))

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(
                        "과목 상세 보기",
                        key=f"guide_detail_{key_safe(course['name'])}",
                        use_container_width=True,
                    ):
                        open_detail(course["name"])
                        st.rerun()
                with col_b:
                    star = "⭐ 관심 과목에 저장됨" if course["name"] in st.session_state.favorites else "☆ 관심 과목에 담기"
                    if st.button(
                        star,
                        key=f"guide_star_{key_safe(course['name'])}",
                        use_container_width=True,
                    ):
                        toggle_favorite(course["name"])
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

            if st.session_state.detail_open:
                st.divider()
                st.markdown("## 🔎 선택한 과목 상세")
                render_detail_panel()

        if st.button("선택 조건 다시 설정하기", key="guide_reset"):
            st.session_state.guide_done = False
            st.session_state.guide_results = []
            st.rerun()

# =========================================================
# 13. 공통 알림 및 안내
# =========================================================
if st.session_state.toast_message:
    message = html.escape(st.session_state.toast_message)
    st.markdown(
        f'<div class="toast">{message}</div>',
        unsafe_allow_html=True,
    )
    # 알림은 한 번 표시하고 다음 렌더링에서 반복되지 않도록 정리합니다.
    st.session_state.toast_message = ""

st.divider()
st.caption(
    "🌱 나의 과목 선택 가이드 | 과목 정보는 참고용이며, "
    "실제 개설 과목·교육과정·성취기준은 학교와 공식 자료를 통해 확인하세요."
)
