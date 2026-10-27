
import streamlit as st
import html

st.set_page_config(
    page_title="나의 과목 선택 가이드",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# 1. 과목 데이터
# =====================================================
COURSES = [
    {"name": "공통국어", "field": "국어", "kind": "일반 선택",
     "intro": "다양한 글을 읽고 자신의 생각을 표현합니다.",
     "goals": "읽기, 쓰기, 말하기, 듣기 능력과 비판적 사고력을 기릅니다.",
     "careers": ["인문", "교육", "언론"], "topics": ["독서", "글쓰기", "토론"]},
    {"name": "화법과 언어", "field": "국어", "kind": "일반 선택",
     "intro": "언어의 특징과 효과적인 의사소통 방법을 배웁니다.",
     "goals": "상황에 맞게 소통하고 언어생활을 탐구합니다.",
     "careers": ["인문", "교육", "언론"], "topics": ["토론", "의사소통"]},
    {"name": "독서와 작문", "field": "국어", "kind": "일반 선택",
     "intro": "다양한 자료를 읽고 자신의 글로 표현합니다.",
     "goals": "정보를 분석하고 논리적으로 글을 구성합니다.",
     "careers": ["인문", "언론", "교육"], "topics": ["독서", "글쓰기", "탐구"]},
    {"name": "문학", "field": "국어", "kind": "일반 선택",
     "intro": "시와 소설 등 문학 작품을 감상하고 해석합니다.",
     "goals": "문학적 감수성과 상상력, 다양한 삶에 대한 이해를 기릅니다.",
     "careers": ["인문", "문화", "예술"], "topics": ["독서", "문화", "예술"]},

    {"name": "수학", "field": "수학", "kind": "일반 선택",
     "intro": "수학의 기본 개념과 원리를 이해하고 문제를 해결합니다.",
     "goals": "수학적 사고력과 추론 능력을 기릅니다.",
     "careers": ["공학", "자연과학", "정보"], "topics": ["문제 해결", "논리"]},
    {"name": "대수", "field": "수학", "kind": "일반 선택",
     "intro": "식과 방정식, 함수 등 대수의 주요 개념을 탐구합니다.",
     "goals": "대수적 표현과 계산을 이해하고 문제에 적용합니다.",
     "careers": ["공학", "자연과학", "정보"], "topics": ["문제 해결", "논리"]},
    {"name": "미적분Ⅰ", "field": "수학", "kind": "일반 선택",
     "intro": "함수의 변화와 누적을 수학적으로 이해합니다.",
     "goals": "극한, 미분, 적분의 기초 개념을 이해하고 활용합니다.",
     "careers": ["공학", "자연과학", "정보"], "topics": ["문제 해결", "논리"]},
    {"name": "확률과 통계", "field": "수학", "kind": "일반 선택",
     "intro": "자료와 불확실한 상황을 확률과 통계로 분석합니다.",
     "goals": "자료를 해석하고 합리적으로 판단하는 능력을 기릅니다.",
     "careers": ["경제", "사회", "정보"], "topics": ["데이터", "탐구"]},
    {"name": "기하", "field": "수학", "kind": "진로 선택",
     "intro": "도형과 공간의 성질을 수학적으로 탐구합니다.",
     "goals": "공간 감각과 기하적 추론 능력을 기릅니다.",
     "careers": ["공학", "자연과학", "건축"], "topics": ["논리", "문제 해결"]},

    {"name": "영어", "field": "영어", "kind": "일반 선택",
     "intro": "영어 자료를 이해하고 다양한 상황에서 의사소통합니다.",
     "goals": "영어 듣기, 말하기, 읽기, 쓰기 능력을 기릅니다.",
     "careers": ["언론", "교육", "국제"], "topics": ["의사소통", "문화"]},
    {"name": "영어Ⅰ", "field": "영어", "kind": "일반 선택",
     "intro": "다양한 주제의 영어 자료를 읽고 활용합니다.",
     "goals": "영어 의사소통 능력과 자기주도적 학습 능력을 기릅니다.",
     "careers": ["국제", "교육", "관광"], "topics": ["의사소통", "독서"]},

    {"name": "세계사", "field": "사회", "kind": "일반 선택",
     "intro": "세계 여러 지역의 역사적 변화와 교류를 탐구합니다.",
     "goals": "역사적 사고력을 기르고 현재 사회를 이해합니다.",
     "careers": ["역사", "교육", "국제"], "topics": ["역사", "문화", "탐구"]},
    {"name": "사회와 문화", "field": "사회", "kind": "일반 선택",
     "intro": "사회 현상과 문화의 특징을 자료로 분석합니다.",
     "goals": "사회 현상을 탐구하고 다양한 관점을 이해합니다.",
     "careers": ["사회", "교육", "행정"], "topics": ["사회", "탐구", "데이터"]},
    {"name": "경제", "field": "사회", "kind": "일반 선택",
     "intro": "시장과 경제생활에서 나타나는 현상을 탐구합니다.",
     "goals": "경제 원리를 이해하고 합리적인 의사결정을 연습합니다.",
     "careers": ["경제", "경영", "금융"], "topics": ["데이터", "사회"]},
    {"name": "정치와 법", "field": "사회", "kind": "일반 선택",
     "intro": "정치 과정과 법의 원리를 이해합니다.",
     "goals": "민주시민에게 필요한 판단력과 참여 역량을 기릅니다.",
     "careers": ["법", "행정", "정치"], "topics": ["사회", "토론"]},

    {"name": "통합과학", "field": "과학", "kind": "일반 선택",
     "intro": "여러 과학 분야의 기초 개념을 연결해 배웁니다.",
     "goals": "자연 현상을 과학적으로 탐구하고 통합적으로 이해합니다.",
     "careers": ["자연과학", "공학", "환경"], "topics": ["탐구", "환경"]},
    {"name": "물리학", "field": "과학", "kind": "진로 선택",
     "intro": "운동, 에너지, 전기 등 자연 현상의 원리를 탐구합니다.",
     "goals": "물리 개념과 법칙을 이해하고 실제 현상에 적용합니다.",
     "careers": ["공학", "자연과학", "전자"], "topics": ["탐구", "문제 해결"]},
    {"name": "화학", "field": "과학", "kind": "진로 선택",
     "intro": "물질의 구조와 성질, 화학 반응을 탐구합니다.",
     "goals": "물질과 반응에 관한 개념과 탐구 능력을 기릅니다.",
     "careers": ["화학", "보건", "환경"], "topics": ["탐구", "환경"]},
    {"name": "생명과학", "field": "과학", "kind": "진로 선택",
     "intro": "생명체의 구조와 기능, 생명 현상의 원리를 탐구합니다.",
     "goals": "생명 현상을 이해하고 관련 문제를 탐구합니다.",
     "careers": ["생명과학", "보건", "의료"], "topics": ["탐구", "보건"]},
    {"name": "지구과학", "field": "과학", "kind": "진로 선택",
     "intro": "지구와 우주에서 나타나는 현상을 탐구합니다.",
     "goals": "지구 시스템과 우주를 이해하고 자료 분석 능력을 기릅니다.",
     "careers": ["환경", "자연과학", "우주"], "topics": ["탐구", "환경", "데이터"]},

    {"name": "정보", "field": "정보·기술·가정", "kind": "일반 선택",
     "intro": "컴퓨팅 사고와 정보 기술을 활용해 문제를 해결합니다.",
     "goals": "자료와 알고리즘을 이해하고 디지털 문제 해결 능력을 기릅니다.",
     "careers": ["정보", "공학", "데이터"], "topics": ["데이터", "문제 해결", "프로젝트"]},
    {"name": "인공지능 기초", "field": "정보·기술·가정", "kind": "진로 선택",
     "intro": "인공지능의 기본 원리와 활용 사례를 이해합니다.",
     "goals": "인공지능 기술과 사회적 영향을 탐구합니다.",
     "careers": ["정보", "데이터", "공학"], "topics": ["데이터", "프로젝트"]},
    {"name": "기술·가정", "field": "정보·기술·가정", "kind": "일반 선택",
     "intro": "기술과 가정생활의 원리를 배우고 생활 문제를 해결합니다.",
     "goals": "실생활 문제 해결과 지속가능한 생활 역량을 기릅니다.",
     "careers": ["공학", "디자인", "환경"], "topics": ["프로젝트", "환경"]},

    {"name": "음악", "field": "예술", "kind": "일반 선택",
     "intro": "음악을 감상하고 표현하며 음악의 가치를 이해합니다.",
     "goals": "음악적 표현과 감상 능력을 기릅니다.",
     "careers": ["예술", "문화", "공연"], "topics": ["예술", "문화", "프로젝트"]},
    {"name": "미술", "field": "예술", "kind": "일반 선택",
     "intro": "시각적으로 표현하고 작품을 감상하며 미술 문화를 탐구합니다.",
     "goals": "창의적 표현 능력과 시각적 소통 능력을 기릅니다.",
     "careers": ["예술", "디자인", "콘텐츠"], "topics": ["예술", "문화", "프로젝트"]},

    {"name": "일본어", "field": "제2외국어·한문", "kind": "일반 선택",
     "intro": "일본어의 기초 표현과 일본의 생활 문화를 배웁니다.",
     "goals": "기초 의사소통 능력과 문화 이해 능력을 기릅니다.",
     "careers": ["국제", "관광", "언어"], "topics": ["의사소통", "문화"]},
    {"name": "중국어", "field": "제2외국어·한문", "kind": "일반 선택",
     "intro": "중국어의 기초 표현과 중국어권 문화를 배웁니다.",
     "goals": "기초 중국어 의사소통 능력과 문화 이해 능력을 기릅니다.",
     "careers": ["국제", "관광", "언어"], "topics": ["의사소통", "문화"]},

    {"name": "철학", "field": "교양", "kind": "융합 선택",
     "intro": "인간과 세계, 지식과 가치에 관한 질문을 탐구합니다.",
     "goals": "논리적으로 질문하고 근거를 바탕으로 생각을 구성합니다.",
     "careers": ["인문", "교육", "사회"], "topics": ["토론", "논리", "탐구"]},
    {"name": "환경", "field": "교양", "kind": "융합 선택",
     "intro": "환경 문제와 지속가능한 사회를 다양한 관점에서 살펴봅니다.",
     "goals": "환경 문제를 탐구하고 지속가능한 실천 방안을 고민합니다.",
     "careers": ["환경", "과학", "사회"], "topics": ["환경", "탐구", "프로젝트"]},

    {"name": "체육", "field": "체육", "kind": "일반 선택",
     "intro": "신체 활동에 참여하며 건강과 운동 능력을 기릅니다.",
     "goals": "건강한 생활 습관과 안전한 신체 활동 태도를 기릅니다.",
     "careers": ["체육", "보건", "교육"], "topics": ["건강", "프로젝트"]},
]

FIELDS = list(dict.fromkeys(c["field"] for c in COURSES))
COURSE_NAMES = [c["name"] for c in COURSES]

FIELD_DESCRIPTIONS = {
    "국어": "읽기, 쓰기, 말하기와 문학을 탐구하는 분야",
    "수학": "논리적 사고와 수학적 문제 해결을 배우는 분야",
    "영어": "영어 의사소통과 다양한 문화를 배우는 분야",
    "사회": "사회 현상, 역사, 경제, 정치 등을 탐구하는 분야",
    "과학": "자연 현상과 과학적 원리를 탐구하는 분야",
    "정보·기술·가정": "디지털 기술과 생활 속 문제 해결을 배우는 분야",
    "예술": "창의적인 표현과 예술 감상을 경험하는 분야",
    "제2외국어·한문": "다른 언어와 문화에 대해 배우는 분야",
    "교양": "다양한 관점으로 삶과 사회를 탐구하는 분야",
    "체육": "신체 활동과 건강한 생활을 배우는 분야",
}

# =====================================================
# 2. 세션 상태
# =====================================================
defaults = {
    "page": "🏠 홈",
    "favorites": [],
    "reviews": [],
    "selected_course": None,
    "detail_open": False,
    "guide_results": [],
    "guide_done": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_page(page):
    st.session_state.page = page
    st.session_state.detail_open = False
    st.session_state.selected_course = None
    st.rerun()


def find_course(name):
    return next((c for c in COURSES if c["name"] == name), None)


def safe_key(text):
    return "".join(ch if ch.isalnum() else "_" for ch in text)


def toggle_favorite(name):
    favorites = list(st.session_state.favorites)
    if name in favorites:
        favorites.remove(name)
        st.toast(f"⭐ {name} 과목을 관심 목록에서 뺐어요.")
    else:
        favorites.append(name)
        st.toast(f"⭐ {name} 과목을 관심 목록에 담았어요.")
    st.session_state.favorites = favorites


def open_detail(name):
    st.session_state.selected_course = name
    st.session_state.detail_open = True


# =====================================================
# 3. 스타일
# =====================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap');

    .stApp {
        background: #fbf8ed;
        color: #28382c;
    }

    html, body, [class*="css"] {
        font-family: 'Gowun Dodum', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Jua', sans-serif !important;
        color: #2f5940;
    }

    h1 { font-size: 2.25rem !important; }

    [data-testid="stSidebar"] {
        background: #eef3e6;
        border-right: 1px solid #d5e3cc;
    }

    [data-testid="stSidebar"] button {
        border-radius: 7px !important;
        min-height: 44px;
        font-weight: bold;
        text-align: left;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 40px;
    }

    .hero {
        background: linear-gradient(120deg, #e3efdc, #fff1c6);
        border: 1px solid #d8e4d0;
        border-radius: 18px;
        padding: 25px;
        margin-bottom: 18px;
    }

    .field-section {
        border-radius: 16px;
        padding: 15px;
        margin: 18px 0 10px 0;
        border: 2px solid #d8e3d0;
        background: #f0f5e9;
    }

    .field-header {
        border-radius: 10px;
        padding: 12px 16px;
        color: white;
        font-family: 'Jua', sans-serif;
        font-size: 1.4rem;
        margin-bottom: 8px;
    }

    .field-description {
        color: #526653;
        font-size: 0.95rem;
        padding: 2px 3px 5px 3px;
    }

    .subject-card {
        background: #fffdf7;
        border: 1px solid #d8e1d2;
        border-left: 6px solid #83a878;
        border-radius: 12px;
        padding: 14px;
        min-height: 195px;
        margin: 6px 0 8px 0;
    }

    .subject-title {
        color: #2f5940;
        font-family: 'Jua', sans-serif;
        font-size: 1.22rem;
        margin-bottom: 6px;
    }

    .subject-description {
        font-size: 0.95rem;
        line-height: 1.55;
        color: #38483b;
        min-height: 52px;
    }

    .badge {
        display: inline-block;
        border-radius: 6px;
        padding: 4px 9px;
        font-size: 0.84rem;
        font-weight: bold;
        margin: 2px 3px 6px 0;
    }

    .badge-general {
        background: #dcebd8;
        color: #285739;
    }

    .badge-career {
        background: #ffedbd;
        color: #795510;
    }

    .badge-convergence {
        background: #e9def8;
        color: #61418a;
    }

    .detail-panel {
        background: #f0f5e9;
        border: 2px solid #d5e3cc;
        border-radius: 15px;
        padding: 20px;
    }

    .review-card {
        background: #fffdf7;
        border: 1px solid #e0e5d7;
        border-radius: 12px;
        padding: 14px;
        margin: 10px 0;
    }

    .notice {
        background: #fff5cf;
        border-left: 5px solid #e5c455;
        padding: 12px 15px;
        border-radius: 8px;
        margin: 12px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# 4. 사이드바
# =====================================================
PAGES = [
    "🏠 홈",
    "📚 분야별 과목",
    "🔎 과목 검색",
    "⭐ 관심 과목",
    "💬 수강후기",
    "🧭 선택 가이드",
]

with st.sidebar:
    st.markdown("# 🌱 과목 선택 가이드")
    st.caption("나에게 맞는 과목을 찾아봐요.")
    st.divider()

    for page_name in PAGES:
        current = st.session_state.page == page_name
        label = f"▶  {page_name}" if current else page_name
        if st.button(
            label,
            key=f"nav_{safe_key(page_name)}",
            use_container_width=True,
            type="primary" if current else "secondary",
        ):
            go_page(page_name)

    st.divider()
    st.markdown("### ⭐ 관심 과목")
    st.write(f"{len(st.session_state.favorites)}개 저장됨")

# =====================================================
# 5. 공통 과목 카드
# =====================================================
BADGE_CLASSES = {
    "일반 선택": "badge-general",
    "진로 선택": "badge-career",
    "융합 선택": "badge-convergence",
}

def render_course_card(course, prefix):
    name = course["name"]
    favorite = name in st.session_state.favorites
    badge = BADGE_CLASSES.get(course["kind"], "badge-general")

    st.markdown(
        f"""
        <div class="subject-card">
            <div class="subject-title">{html.escape(name)}</div>
            <span class="badge {badge}">{html.escape(course["kind"])}</span>
            <div class="subject-description">{html.escape(course["intro"])}</div>
            <div><b>관련 분야:</b> {html.escape(" · ".join(course["careers"]))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "⭐ 관심 해제" if favorite else "☆ 관심 담기",
            key=f"{prefix}_star_{safe_key(name)}",
            use_container_width=True,
        ):
            toggle_favorite(name)
            st.rerun()
    with c2:
        if st.button(
            "상세 보기 →",
            key=f"{prefix}_detail_{safe_key(name)}",
            use_container_width=True,
        ):
            open_detail(name)
            st.rerun()


def render_review_list(course_name=None):
    reviews = st.session_state.reviews
    if course_name:
        reviews = [r for r in reviews if r["course"] == course_name]

    if not reviews:
        st.info("아직 등록된 후기가 없어요.")
        return

    for review in reversed(reviews):
        st.markdown('<div class="review-card">', unsafe_allow_html=True)
        st.markdown(f"**📚 {html.escape(review['course'])} · ⭐ {review['rating']}/5**")
        st.write(review["text"])
        if review.get("advice"):
            st.caption("💡 조언: " + review["advice"])
        st.markdown("</div>", unsafe_allow_html=True)


def render_review_form(course_name, prefix):
    with st.form(f"{prefix}_{safe_key(course_name)}"):
        rating = st.slider("추천 정도", 1, 5, 4, key=f"{prefix}_rating_{safe_key(course_name)}")
        review_text = st.text_area(
            "수강후기",
            placeholder="배운 내용, 느낀 점, 과목이 잘 맞을 학생 등을 적어 주세요.",
            key=f"{prefix}_text_{safe_key(course_name)}",
        )
        advice = st.text_input(
            "후배에게 주는 조언 (선택)",
            key=f"{prefix}_advice_{safe_key(course_name)}",
        )
        submitted = st.form_submit_button("후기 등록하기", use_container_width=True)

    if submitted:
        if not review_text.strip():
            st.warning("후기 내용을 입력해 주세요.")
        else:
            st.session_state.reviews.append({
                "course": course_name,
                "rating": rating,
                "text": review_text.strip(),
                "advice": advice.strip(),
            })
            st.success("후기가 등록되었어요.")
            st.rerun()


def render_detail_panel():
    course = find_course(st.session_state.selected_course)
    if not st.session_state.detail_open or not course:
        return

    st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
    st.markdown(f"## 📖 {html.escape(course['name'])}")
    st.caption(f"{course['field']} · {course['kind']}")
    st.write(course["intro"])

    st.markdown("### 🎯 무엇을 배우나요?")
    st.write(course["goals"])

    st.markdown("### 🧭 관련 관심 분야")
    st.write(" · ".join(course["careers"]))

    st.markdown("### 💬 이 과목의 수강후기")
    render_review_list(course["name"])
    render_review_form(course["name"], "detail_review")

    st.markdown("### 🔗 공식 자료 확인")
    st.markdown("- [국가교육과정정보센터(NCIC)](https://www.ncic.re.kr/)")
    st.markdown("- [고교학점제 안내](https://www.hscredit.kr/)")
    st.caption("과목 설명은 이해를 돕기 위한 요약입니다. 공식 성취기준과 학교 개설 여부를 확인하세요.")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✕ 상세 패널 닫기", key="close_detail", use_container_width=True):
        st.session_state.detail_open = False
        st.session_state.selected_course = None
        st.rerun()


def render_list_with_detail(courses, prefix):
    if st.session_state.detail_open and st.session_state.selected_course:
        left, right = st.columns([1.05, 0.95], gap="large")
        with left:
            st.markdown("### 📚 과목 목록")
            for course in courses:
                render_course_card(course, prefix)
        with right:
            st.markdown("### 🔎 과목 상세")
            render_detail_panel()
    else:
        for course in courses:
            render_course_card(course, prefix)


# =====================================================
# 6. 페이지
# =====================================================
page = st.session_state.page

if page == "🏠 홈":
    st.markdown(
        """
        <div class="hero">
            <h1>🌱 나에게 맞는 과목 찾기</h1>
            <p>관심 분야와 배우고 싶은 내용을 바탕으로 과목을 탐색해 보세요.</p>
            <p>정답을 고르는 것보다 나에게 맞는 선택의 이유를 알아가는 것이 중요해요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)
    a.metric("등록 과목", f"{len(COURSES)}개")
    b.metric("관심 과목", f"{len(st.session_state.favorites)}개")
    c.metric("수강후기", f"{len(st.session_state.reviews)}개")

    st.markdown("## 어디서 시작할까요?")
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="field-section">', unsafe_allow_html=True)
        st.markdown("### 📚 분야별 과목")
        st.write("색으로 구분된 분야별 섹션에서 과목을 찾아보세요.")
        if st.button("분야별 과목 보기 →", key="home_fields", use_container_width=True):
            go_page("📚 분야별 과목")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="field-section">', unsafe_allow_html=True)
        st.markdown("### 🔎 과목 검색")
        st.write("과목명이나 관심 주제로 과목을 찾아보세요.")
        if st.button("과목 검색하기 →", key="home_search", use_container_width=True):
            go_page("🔎 과목 검색")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## ✨ 과목 선택 전 생각해 보기")
    st.markdown("""
    - 어떤 주제를 배울 때 가장 흥미롭나요?
    - 더 깊게 탐구하고 싶은 교과 내용은 무엇인가요?
    - 관심 진로와 연결되는 과목이 있나요?
    - 학교에서 실제로 개설하는 과목인가요?
    """)
    st.markdown(
        '<div class="notice">과목 유형과 개설 여부는 학교 교육과정에 따라 다를 수 있습니다. '
        '최종 선택 전에 학교 안내 자료와 담당 선생님의 설명을 확인하세요.</div>',
        unsafe_allow_html=True,
    )

elif page == "📚 분야별 과목":
    st.title("📚 분야별 과목")
    st.write("분야별 직사각형 영역에서 과목을 비교해 보세요.")

    f1, f2 = st.columns(2)
    with f1:
        selected_field = st.selectbox("① 관심 분야", ["전체"] + FIELDS, key="field_filter")
    with f2:
        selected_kind = st.selectbox(
            "② 과목 유형",
            ["전체", "일반 선택", "진로 선택", "융합 선택"],
            key="kind_filter",
        )

    filtered = [
        c for c in COURSES
        if (selected_field == "전체" or c["field"] == selected_field)
        and (selected_kind == "전체" or c["kind"] == selected_kind)
    ]

    st.caption(f"검색 결과: {len(filtered)}개 과목")

    # 분야별 색상 테마
    FIELD_COLORS = {
        "국어": ("#47785a", "#edf5e9", "#d5e3cc"),
        "수학": ("#3e718e", "#eaf3f8", "#c8dfe9"),
        "영어": ("#8a659e", "#f3edf7", "#dfd0e9"),
        "사회": ("#a36b36", "#fbf0e3", "#ead4bc"),
        "과학": ("#397f79", "#e7f4f1", "#c5e2dc"),
        "정보·기술·가정": ("#5268a0", "#edf0fa", "#d2d9f0"),
        "예술": ("#a65d76", "#f9edf1", "#edcfda"),
        "제2외국어·한문": ("#8b7a35", "#f8f4df", "#e8dfb5"),
        "교양": ("#75654d", "#f3eee5", "#e1d5c2"),
        "체육": ("#4c8250", "#edf5e8", "#d2e5cb"),
    }

    for field_name in FIELDS:
        group = [c for c in filtered if c["field"] == field_name]
        if not group:
            continue

        main_color, bg_color, border_color = FIELD_COLORS.get(
            field_name, ("#47785a", "#f0f5e9", "#d5e3cc")
        )

        st.markdown(
            f"""
            <div style="
                background:{bg_color};
                border:2px solid {border_color};
                border-radius:16px;
                padding:15px;
                margin:22px 0 10px 0;
            ">
                <div style="
                    background:{main_color};
                    color:white;
                    border-radius:10px;
                    padding:12px 16px;
                    font-family:'Jua',sans-serif;
                    font-size:1.4rem;
                ">📂 {html.escape(field_name)}</div>
                <div style="color:#526653;padding:12px 3px 3px 3px;">
                    {html.escape(FIELD_DESCRIPTIONS.get(field_name, "관심 과목을 찾아보세요."))}
                    · 과목 {len(group)}개
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for i in range(0, len(group), 2):
            row = st.columns(2, gap="medium")
            for j, course in enumerate(group[i:i + 2]):
                with row[j]:
                    render_course_card(course, "field")

    if st.session_state.detail_open:
        st.divider()
        st.markdown("## 🔎 선택한 과목 상세")
        render_detail_panel()

elif page == "🔎 과목 검색":
    st.title("🔎 과목 검색")
    st.write("과목명, 설명, 관련 분야와 관심 주제로 검색하세요.")

    query = st.text_input("검색어", placeholder="예: 데이터, 환경, 글쓰기")
    f1, f2 = st.columns(2)
    with f1:
        field_filter = st.selectbox("분야", ["전체"] + FIELDS, key="search_field")
    with f2:
        kind_filter = st.selectbox(
            "과목 유형",
            ["전체", "일반 선택", "진로 선택", "융합 선택"],
            key="search_kind",
        )

    results = []
    for course in COURSES:
        searchable = " ".join([
            course["name"], course["field"], course["kind"],
            course["intro"], course["goals"],
            " ".join(course["careers"]), " ".join(course["topics"]),
        ]).lower()

        if query.strip() and query.strip().lower() not in searchable:
            continue
        if field_filter != "전체" and course["field"] != field_filter:
            continue
        if kind_filter != "전체" and course["kind"] != kind_filter:
            continue
        results.append(course)

    st.caption(f"검색 결과: {len(results)}개")
    render_list_with_detail(results, "search")

elif page == "⭐ 관심 과목":
    st.title("⭐ 나의 관심 과목")
    favorites = [c for c in COURSES if c["name"] in st.session_state.favorites]

    if not favorites:
        st.info("아직 관심 과목이 없어요. 분야별 과목에서 ☆를 눌러 저장해 보세요.")
        if st.button("과목 찾아보기 →", key="favorites_browse"):
            go_page("📚 분야별 과목")
    else:
        render_list_with_detail(favorites, "favorites")

elif page == "💬 수강후기":
    st.title("💬 수강후기와 조언")
    st.write("과목을 먼저 경험한 학생들의 의견을 공유해 보세요.")

    course_name = st.selectbox("후기를 남길 과목", COURSE_NAMES, key="review_course")
    render_review_form(course_name, "review_form")

    st.divider()
    st.markdown("## 🗣️ 등록된 후기")
    review_filter = st.selectbox("후기 필터", ["전체"] + COURSE_NAMES, key="review_filter")
    render_review_list(None if review_filter == "전체" else review_filter)

    st.markdown(
        '<div class="notice">후기는 개인 경험에 따른 의견입니다. 수업 내용과 난이도는 학교마다 다를 수 있어요.</div>',
        unsafe_allow_html=True,
    )

elif page == "🧭 선택 가이드":
    st.title("🧭 나에게 맞는 과목 선택 가이드")
    st.write("관심 분야와 학습 방식에 답하면 관련 과목을 추천해 드려요.")

    with st.form("guide_form"):
        kinds = st.multiselect(
            "① 찾고 있는 과목 유형",
            ["일반 선택", "진로 선택", "융합 선택"],
            default=["일반 선택", "진로 선택", "융합 선택"],
        )
        interests = st.multiselect(
            "② 관심 분야",
            sorted(set(tag for c in COURSES for tag in c["careers"])),
        )
        topics = st.multiselect(
            "③ 배우고 싶은 주제",
            sorted(set(topic for c in COURSES for topic in c["topics"])),
        )
        priorities = st.multiselect(
            "④ 중요한 선택 기준",
            [
                "흥미와 호기심", "희망 진로와의 연결",
                "기초 개념과 학습 준비", "새로운 분야 경험",
                "탐구와 프로젝트", "다른 과목과의 연계",
            ],
            default=["흥미와 호기심"],
        )
        style = st.radio(
            "⑤ 선호하는 학습 방식",
            [
                "개념을 차근차근 배우기",
                "자료를 읽고 분석하기",
                "문제를 해결하고 계산하기",
                "토론하고 의견 나누기",
                "직접 만들고 프로젝트 하기",
                "아직 잘 모르겠어요",
            ],
        )
        challenge = st.radio(
            "⑥ 원하는 학습 수준",
            [
                "기초를 탄탄히 다지고 싶어요",
                "익숙한 내용과 새로운 내용을 함께 배우고 싶어요",
                "관심 분야를 깊이 탐구하고 싶어요",
            ],
        )
        submitted = st.form_submit_button(
            "나에게 맞는 과목 추천받기 🌱",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        scored = []
        for course in COURSES:
            if kinds and course["kind"] not in kinds:
                continue

            score = 0
            reasons = []
            career_matches = set(interests) & set(course["careers"])
            topic_matches = set(topics) & set(course["topics"])

            if career_matches:
                score += 3 * len(career_matches)
                reasons.append("관심 분야와 연결돼요")
            if topic_matches:
                score += 2 * len(topic_matches)
                reasons.append("배우고 싶은 주제를 포함해요")
            if "흥미와 호기심" in priorities and (career_matches or topic_matches):
                score += 1
            if "희망 진로와의 연결" in priorities and career_matches:
                score += 2
            if "새로운 분야 경험" in priorities:
                score += 1
            if "탐구와 프로젝트" in priorities and (
                "탐구" in course["topics"] or "프로젝트" in course["topics"]
            ):
                score += 2
                reasons.append("탐구 활동과 연결돼요")
            if "다른 과목과의 연계" in priorities and topic_matches:
                score += 1

            if style == "자료를 읽고 분석하기" and (
                "독서" in course["topics"] or "데이터" in course["topics"]
            ):
                score += 2
            elif style == "문제를 해결하고 계산하기" and (
                "문제 해결" in course["topics"] or "논리" in course["topics"]
            ):
                score += 2
            elif style == "토론하고 의견 나누기" and (
                "토론" in course["topics"] or "의사소통" in course["topics"]
            ):
                score += 2
            elif style == "직접 만들고 프로젝트 하기" and "프로젝트" in course["topics"]:
                score += 2

            if challenge == "관심 분야를 깊이 탐구하고 싶어요" and course["kind"] in ["진로 선택", "융합 선택"]:
                score += 2
            elif challenge == "익숙한 내용과 새로운 내용을 함께 배우고 싶어요" and course["kind"] == "일반 선택":
                score += 1

            if not reasons:
                reasons.append("과목 소개를 읽고 흥미가 있는지 확인해 보세요")

            scored.append((score, course, reasons))

        scored.sort(key=lambda item: (-item[0], item[1]["name"]))
        st.session_state.guide_results = scored[:8]
        st.session_state.guide_done = True
        st.session_state.detail_open = False
        st.session_state.selected_course = None

    if st.session_state.guide_done:
        st.divider()
        st.markdown("## 🌟 추천 과목")
        st.caption("추천은 입력한 관심사에 따른 참고 결과이며, 성적이나 적합성을 확정하는 평가가 아닙니다.")

        for score, course, reasons in st.session_state.guide_results:
            st.markdown('<div class="review-card">', unsafe_allow_html=True)
            st.markdown(f"### 🌱 {html.escape(course['name'])}")
            st.caption(f"{course['field']} · {course['kind']}")
            st.write(course["intro"])
            st.write("추천 이유: " + " · ".join(reasons))

            a, b = st.columns(2)
            with a:
                if st.button("상세 보기", key=f"guide_detail_{safe_key(course['name'])}", use_container_width=True):
                    open_detail(course["name"])
                    st.rerun()
            with b:
                fav = course["name"] in st.session_state.favorites
                if st.button(
                    "⭐ 관심 저장됨" if fav else "☆ 관심 과목에 담기",
                    key=f"guide_fav_{safe_key(course['name'])}",
                    use_container_width=True,
                ):
                    toggle_favorite(course["name"])
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.detail_open:
            st.markdown("## 🔎 선택한 과목 상세")
            render_detail_panel()

        if st.button("선택 조건 다시 설정하기", key="guide_reset"):
            st.session_state.guide_done = False
            st.session_state.guide_results = []
            st.rerun()

# =====================================================
# 7. 하단 안내
# =====================================================
st.divider()
st.caption(
    "🌱 나의 과목 선택 가이드 | 과목 설명은 참고용입니다. "
    "실제 개설 과목과 공식 성취기준은 학교 안내 및 국가교육과정정보센터에서 확인하세요."
)
