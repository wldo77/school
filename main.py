
import streamlit as st
import streamlit.components.v1 as components
import html
from datetime import datetime

st.set_page_config(
    page_title="과목 선택 나침반",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# 1. 디자인
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap');

:root {
    --cream:#fbf8ed;
    --green:#426b50;
    --dark:#294b36;
    --pale:#e7efdf;
}
html, body, [class*="css"] {
    font-family:'Gowun Dodum',sans-serif;
}
.stApp {
    background:linear-gradient(145deg,#fbf8ed,#f2f3e8 65%,#e7efdf);
}
.block-container {
    max-width:1400px;
    padding-top:1.5rem;
    padding-bottom:4rem;
}
h1,h2,h3 {
    font-family:'Jua',sans-serif!important;
    color:var(--dark)!important;
}
h1 {font-size:2.35rem!important;}
h2 {font-size:1.8rem!important;}
h3 {font-size:1.3rem!important;}
p,li,label {line-height:1.7;}
.hero {
    background:linear-gradient(120deg,#e6efdc,#fff3d4);
    border:1px solid #d6e2ce;
    padding:27px;
    border-radius:20px;
    margin-bottom:22px;
}
.hero-title {
    font-family:'Jua',sans-serif;
    color:var(--dark);
    font-size:2.15rem;
}
.hero-sub {color:#536650;font-size:1.05rem;margin-top:8px;}
.pill {
    display:inline-block;background:#e7efdf;color:#365c40;
    padding:4px 10px;border-radius:5px;margin:2px;font-size:.85rem;
}
.info-box {
    background:#fffdf6;border-left:4px solid #8ca87a;
    border-radius:5px;padding:13px 16px;margin:8px 0;
}
.review-card {
    background:#fffdf7;border:1px solid #dfe6d6;
    padding:14px;margin:8px 0;border-radius:8px;
}
div.stButton>button {
    border-radius:5px;
    border:1px solid #cbd9c5;
    background:#fffdf6;color:#294b36;
    min-height:43px;font-weight:700;
}
div.stButton>button:hover {
    background:#e7efdf;border-color:#426b50;
}
div.stButton>button[kind="primary"] {
    background:#426b50;color:white;border-color:#426b50;
}
div[data-testid="stSidebar"] {
    background:#edf1e4;
    border-right:1px solid #cbd8c2;
}
div[data-testid="stSidebar"] .nav-title {
    font-family:'Jua',sans-serif;font-size:1.6rem;color:#294b36;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap:0!important;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > div > label {
    border-radius:0!important;
    background:transparent!important;
    border:0!important;
    border-left:4px solid transparent!important;
    border-bottom:1px solid #d5dfce!important;
    padding:13px 10px!important;
    margin:0!important;
    color:#294b36!important;
    font-size:1.03rem!important;
    transition:background .15s;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > div > label:hover {
    background:#dfe9d7!important;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > div > label:has(input:checked) {
    background:#d8e6ce!important;
    border-left:4px solid #426b50!important;
    font-weight:bold!important;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > div > label p {
    font-weight:600;
}
div[data-testid="stMetric"] {
    background:#fffdf6;border:1px solid #dfe6d6;
    padding:12px;border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 2. 과목 자료
# 과목별 소개와 학습목표는 학생용 요약이며 공식 원문 아님
# =====================================================
RAW = {
"국어": [
("공통국어1","공통","읽기·쓰기·말하기의 기초와 다양한 자료의 이해","핵심 내용 파악, 목적에 맞게 표현하기","인문·언어, 교육·심리"),
("공통국어2","공통","다양한 언어 활동을 통한 의사소통","자료를 비판적으로 읽고 의견 표현하기","인문·언어, 미디어"),
("화법과 언어","일반 선택","말하기·듣기와 언어의 구조 및 사용","상황에 맞는 의사소통, 언어 현상 분석","인문·언어, 교육·심리"),
("독서와 작문","일반 선택","깊이 있는 읽기와 논리적인 글쓰기","관점과 근거 평가, 목적에 맞는 글 작성","인문·언어, 사회·법"),
("문학","일반 선택","문학 작품의 감상과 해석","작품의 내용·형식·맥락을 고려한 해석","인문·언어, 예술·디자인"),
("주제 탐구 독서","진로 선택","관심 주제를 중심으로 자료를 읽고 탐구","자료 비교·분석, 탐구 결과 정리","인문·언어, 사회·법"),
("독서 토론과 글쓰기","융합 선택","독서와 토론을 연결한 논리적 글쓰기","근거를 들어 토론하고 주장을 구성","인문·언어, 사회·법"),
],
"수학": [
("공통수학1","공통","식과 방정식 등 수학의 기본 개념","수학 개념 이해와 문제 해결","수학·데이터, 공학·컴퓨터"),
("공통수학2","공통","함수와 도형 등 수학 개념의 연결","수학적 관계를 표현하고 설명","수학·데이터, 공학·컴퓨터"),
("대수","일반 선택","지수·로그와 수열 등 대수적 관계","대수적 표현을 활용한 문제 해결","수학·데이터, 공학·컴퓨터"),
("미적분Ⅰ","일반 선택","함수의 극한과 미분·적분의 기초","변화율과 누적량을 수학적으로 해석","수학·데이터, 자연과학"),
("확률과 통계","일반 선택","확률과 자료 분석","확률 계산과 통계 자료 해석","수학·데이터, 경제·경영"),
("기하","진로 선택","도형과 공간 및 벡터","공간적 관계 표현과 기하 문제 해결","공학·컴퓨터, 자연과학"),
("경제 수학","진로 선택","경제 현상과 수학적 관계","경제 자료와 수학적 모델 연결","경제·경영, 수학·데이터"),
("실용 통계","융합 선택","실생활 자료의 수집과 통계적 해석","자료 정리, 분석, 결과 전달","수학·데이터, 사회·법"),
],
"영어": [
("공통영어1","공통","다양한 영어 자료의 이해와 표현","중심 내용 파악과 영어 의사소통","국제·외국어, 미디어"),
("공통영어2","공통","영어 의사소통과 문화 이해","핵심 정보 이해와 의견 표현","국제·외국어, 교육·심리"),
("영어Ⅰ","일반 선택","다양한 주제의 영어 자료 이해","세부 정보와 중심 생각 파악","국제·외국어, 경제·경영"),
("영어Ⅱ","일반 선택","복합적인 영어 자료와 의사소통","자료 분석과 영어로 의견 전달","국제·외국어, 자연과학"),
("영어 독해와 작문","일반 선택","영어 읽기와 목적에 맞는 작문","논리 구조 이해와 글쓰기","국제·외국어, 미디어"),
("영어 발표와 토론","진로 선택","영어 발표와 근거 중심 토론","발표 구성, 근거 제시, 상호작용","국제·외국어, 사회·법"),
("미디어 영어","융합 선택","미디어 속 영어 표현과 정보","미디어 자료 분석과 신뢰성 평가","국제·외국어, 미디어"),
],
"사회": [
("통합사회1","공통","인간·사회·공간·환경의 통합적 이해","사회 현상을 여러 관점으로 설명","사회·법, 경제·경영"),
("통합사회2","공통","사회 문제와 지속가능한 삶","사회 문제 분석과 해결 방안 탐색","사회·법, 환경·생태"),
("한국사1","공통","한국사의 흐름과 역사적 변화","사료를 통한 역사적 사실과 의미 파악","인문·언어, 사회·법"),
("세계시민과 지리","일반 선택","세계 지역과 세계화 현상","지도와 자료를 통한 지역 분석","국제·외국어, 환경·생태"),
("세계사","일반 선택","세계 여러 지역의 역사와 교류","역사 자료 비교와 변화 이해","인문·언어, 국제·외국어"),
("사회와 문화","일반 선택","사회 구조와 문화 현상","사회 자료 분석과 관점 비교","사회·법, 교육·심리"),
("정치","진로 선택","정치 과정과 시민 참여","정치 제도와 쟁점 분석","사회·법, 국제·외국어"),
("법과 사회","진로 선택","법의 원리와 생활 속 법적 쟁점","법적 쟁점 파악과 근거 중심 판단","사회·법"),
("경제","진로 선택","경제 주체의 선택과 시장","경제 자료 해석과 선택 결과 분석","경제·경영, 사회·법"),
("사회문제 탐구","융합 선택","현실 사회 문제의 조사와 대안 탐색","문제 설정, 자료 조사, 대안 제안","사회·법, 환경·생태"),
],
"과학": [
("통합과학1","공통","물질과 자연 현상의 통합적 이해","과학 개념 연결과 탐구 자료 해석","자연과학, 공학·컴퓨터"),
("통합과학2","공통","생명·환경 등 과학 현상의 연결","과학적 근거를 활용한 설명","자연과학, 환경·생태"),
("과학탐구실험1","공통","과학 탐구의 기초와 실험 방법","관찰·측정·기록과 안전한 실험","자연과학, 의료·보건"),
("물리학","일반 선택","운동과 에너지 등 물리 현상","물리 개념을 활용한 현상 설명","자연과학, 공학·컴퓨터"),
("화학","일반 선택","물질의 구조와 성질, 화학 반응","물질의 성질과 변화를 설명","자연과학, 의료·보건"),
("생명과학","일반 선택","생명체의 구조와 생명 현상","생명 현상에 관한 자료 분석","자연과학, 의료·보건"),
("지구과학","일반 선택","지구와 우주의 현상","관측 자료를 통한 지구 시스템 설명","자연과학, 환경·생태"),
("역학과 에너지","진로 선택","운동과 에너지의 관계","물리 법칙을 활용한 운동 분석","공학·컴퓨터, 자연과학"),
("생물의 유전","진로 선택","유전 현상과 유전 정보 전달","유전 자료 해석과 생명 현상 설명","자연과학, 의료·보건"),
("기후변화와 환경생태","융합 선택","기후 변화와 생태계의 변화","환경 자료 분석과 보전 방안 제안","환경·생태, 자연과학"),
("융합과학 탐구","융합 선택","과학 분야를 연결하는 탐구 활동","질문 설정, 증거 수집, 결과 발표","자연과학, 공학·컴퓨터"),
],
"정보·기술·가정": [
("정보","일반 선택","디지털 정보와 컴퓨팅 사고","문제 분해, 알고리즘, 데이터 활용","공학·컴퓨터, 수학·데이터"),
("인공지능 기초","진로 선택","인공지능의 기본 개념과 활용","AI 원리와 사회적 영향 탐색","공학·컴퓨터, 수학·데이터"),
("데이터 과학","진로 선택","데이터 수집과 분석","데이터 처리, 시각화, 결과 해석","수학·데이터, 공학·컴퓨터"),
("소프트웨어와 생활","융합 선택","소프트웨어를 활용한 생활 문제 해결","문제 정의, 프로그램 설계, 개선","공학·컴퓨터"),
("기술·가정","일반 선택","기술·생활·가족과 자립","생활 문제 해결과 지속가능한 실천","공학·컴퓨터, 교육·심리"),
("로봇과 공학세계","진로 선택","로봇과 공학 기술의 원리","공학 문제 분석과 설계 제안","공학·컴퓨터"),
("창의 공학 설계","진로 선택","설계 과정을 통한 실생활 문제 해결","아이디어 구상, 설계·제작·평가","공학·컴퓨터, 예술·디자인"),
],
"예술": [
("음악","일반 선택","음악 감상과 표현 및 음악 문화","음악 요소 탐색과 표현 활동","예술·디자인"),
("미술","일반 선택","시각적 표현과 작품 감상","시각 요소 활용과 작품 해석","예술·디자인"),
("연극","일반 선택","연극 표현과 협력적 창작","역할 표현, 장면 구성, 공연 제작","예술·디자인, 미디어"),
("음악 연주와 창작","진로 선택","음악 연주와 창의적 구성","음악적 아이디어 표현과 창작","예술·디자인"),
("미술 창작","진로 선택","재료와 방법을 활용한 시각 작품 제작","주제 구상과 작품 제작","예술·디자인"),
("음악과 미디어","융합 선택","음악과 디지털 미디어","매체에 맞는 음악 표현","예술·디자인, 미디어"),
("미술과 매체","융합 선택","다양한 매체를 활용한 시각 표현","시각 콘텐츠 기획과 제작","예술·디자인, 미디어"),
],
"제2외국어·한문": [
("중국어","일반 선택","중국어 기초 표현과 중국 문화","기초 의사소통과 문화 이해","국제·외국어"),
("일본어","일반 선택","일본어 기초 표현과 일본 문화","일상 표현과 문화 맥락 이해","국제·외국어, 미디어"),
("스페인어","일반 선택","스페인어 기초 의사소통","기초 표현과 스페인어권 문화 이해","국제·외국어"),
("프랑스어","일반 선택","프랑스어 기초 표현과 문화","기초 의사소통과 문화 이해","국제·외국어, 예술·디자인"),
("일본 문화","융합 선택","일본 사회와 문화의 탐구","문화 자료 해석과 비교","국제·외국어, 미디어"),
("중국 문화","융합 선택","중국의 역사와 생활 문화","문화 자료 비교와 맥락 이해","국제·외국어, 경제·경영"),
("한문","일반 선택","한자와 한문 문장의 이해","한자 어휘와 문장 의미 파악","인문·언어"),
],
"교양": [
("진로와 직업","일반 선택","흥미와 적성 탐색 및 진로 설계","진로 정보 탐색과 계획 수립","교육·심리"),
("생태와 환경","일반 선택","생태계와 환경 문제","환경 문제 분석과 실천 방안","환경·생태"),
("인간과 심리","진로 선택","인간의 심리와 행동 이해","심리 현상을 여러 관점에서 살피기","교육·심리"),
("교육의 이해","진로 선택","교육의 의미와 사회적 역할","교육 현상 분석과 성찰","교육·심리"),
("보건","진로 선택","건강한 생활과 건강 관리","건강 정보 판단과 생활 습관 계획","의료·보건"),
("논리와 사고","진로 선택","논리적 사고와 합리적 판단","주장과 근거 구분, 추론 평가","인문·언어, 사회·법"),
("금융과 경제생활","융합 선택","생활 속 금융과 경제 의사결정","소비·저축·금융 정보 이해","경제·경영"),
],
"체육": [
("체육1","일반 선택","신체활동과 건강 및 운동 기능","운동 기능과 건강 습관 기르기","체육·스포츠, 의료·보건"),
("체육2","일반 선택","신체활동과 협력","운동 전략과 협동의 가치 실천","체육·스포츠"),
("운동과 건강","진로 선택","운동과 건강의 관계","개인별 운동 계획 수립과 실천","체육·스포츠, 의료·보건"),
("스포츠 문화","진로 선택","스포츠의 사회적·문화적 의미","스포츠와 사회의 관계 분석","체육·스포츠, 사회·법"),
("스포츠 생활1","융합 선택","생활 속 스포츠와 건강한 여가","안전한 스포츠 활동 계획","체육·스포츠"),
],
}

CATEGORY_INFO = {
"국어":"읽기와 표현, 문학을 통해 생각을 나누는 분야예요.",
"수학":"논리적으로 분석하고 문제를 해결하는 힘을 기르는 분야예요.",
"영어":"외국어 의사소통과 다양한 문화 이해를 기르는 분야예요.",
"사회":"역사·지리·정치·경제 등 사회 현상을 탐구해요.",
"과학":"자연 현상을 관찰하고 증거를 바탕으로 설명해요.",
"정보·기술·가정":"디지털 기술과 공학, 생활 속 문제 해결을 다뤄요.",
"예술":"음악·미술·연극으로 생각과 감정을 표현해요.",
"제2외국어·한문":"새로운 언어와 문화를 탐구해요.",
"교양":"진로·환경·심리·보건 등 삶에 필요한 지식을 배워요.",
"체육":"신체활동과 스포츠를 통해 건강과 협력을 배워요.",
}

COURSES = []
for category, rows in RAW.items():
    for name, kind, intro, goals, career in rows:
        COURSES.append({
            "분야": category,
            "과목": name,
            "유형": kind,
            "소개": intro,
            "학습목표": goals,
            "진로": career,
        })

NAMES = [c["과목"] for c in COURSES]
KINDS = ["공통", "일반 선택", "진로 선택", "융합 선택"]
INTERESTS = [
    "인문·언어", "수학·데이터", "자연과학", "의료·보건",
    "공학·컴퓨터", "사회·법", "경제·경영", "교육·심리",
    "예술·디자인", "체육·스포츠", "환경·생태", "국제·외국어",
]

# =====================================================
# 3. 세션 상태와 탐색 함수
# =====================================================
defaults = {
    "page": "🏡 홈",
    "favorites": [],
    "reviews": [],
    "selected_course": None,
    "detail_open": False,
    "toast_message": "",
    "toast_id": 0,
    "guide_results": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

PAGES = [
    "🏡 홈", "📚 분야별 과목", "🔎 과목 검색",
    "⭐ 나의 관심 과목", "💬 수강 후기", "🧭 과목 선택 가이드",
]

def go_page(page):
    # 사이드바 radio 상태와 실제 페이지 상태를 함께 변경
    st.session_state.page = page
    st.session_state.main_navigation = page
    st.session_state.selected_course = None
    st.session_state.detail_open = False

def get_course(name):
    return next((c for c in COURSES if c["과목"] == name), None)

def get_reviews(name):
    return [r for r in st.session_state.reviews if r["course"] == name]

def toggle_favorite(name):
    if name in st.session_state.favorites:
        st.session_state.favorites.remove(name)
        msg = f"⭐ {name} 과목을 관심 목록에서 제외했어요."
    else:
        st.session_state.favorites.append(name)
        msg = f"⭐ {name} 과목을 관심 목록에 추가했어요."
    st.session_state.toast_message = msg
    st.session_state.toast_id += 1

def open_detail(name):
    st.session_state.selected_course = name
    st.session_state.detail_open = True

def close_detail():
    st.session_state.selected_course = None
    st.session_state.detail_open = False

def hero(title, subtitle, emoji="🌿"):
    st.markdown(f"""
    <div class="hero">
      <div style="font-size:2.2rem">{emoji}</div>
      <div class="hero-title">{html.escape(title)}</div>
      <div class="hero-sub">{html.escape(subtitle)}</div>
    </div>
    """, unsafe_allow_html=True)

# 하단 3초 알림
if st.session_state.toast_message:
    msg = html.escape(st.session_state.toast_message)
    tid = st.session_state.toast_id
    components.html(f"""
    <div id="toast{tid}" style="position:fixed;bottom:22px;left:50%;
    transform:translateX(-50%);z-index:999999;background:#294b36;color:white;
    padding:13px 22px;border-radius:6px;box-shadow:0 5px 18px #0003;
    font-size:16px;max-width:90vw;text-align:center">{msg}</div>
    <script>
    setTimeout(()=>{{
      let e=document.getElementById("toast{tid}");
      if(e){{e.style.transition="opacity .3s";e.style.opacity="0";
      setTimeout(()=>e.remove(),350);}}
    }},3000);
    </script>
    """, height=1)
    st.session_state.toast_message = ""

# =====================================================
# 4. 상세 패널과 후기
# =====================================================
def review_form(course):
    with st.expander("✍️ 이 과목 후기 남기기"):
        key = "review_" + course["과목"]
        with st.form(key, clear_on_submit=True):
            nickname = st.text_input("별명", max_chars=20)
            difficulty = st.select_slider(
                "체감 난이도",
                options=["쉬웠어요","조금 쉬웠어요","보통이에요",
                         "조금 어려웠어요","어려웠어요"],
                value="보통이에요",
            )
            content = st.text_area(
                "후기와 공부 조언",
                placeholder="수업 내용, 어려웠던 점, 도움이 된 공부 방법을 적어 주세요.",
                max_chars=1000,
            )
            submit = st.form_submit_button("후기 등록", type="primary")
            if submit:
                if not nickname.strip():
                    st.error("별명을 입력해 주세요.")
                elif len(content.strip()) < 10:
                    st.error("후기를 10자 이상 작성해 주세요.")
                else:
                    st.session_state.reviews.append({
                        "course": course["과목"],
                        "nickname": nickname.strip(),
                        "difficulty": difficulty,
                        "content": content.strip(),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                    })
                    st.session_state.toast_message = "💬 후기가 등록되었어요!"
                    st.session_state.toast_id += 1
                    st.rerun()

def detail_panel(course):
    if not course:
        st.info("과목 목록에서 상세 보기를 선택해 주세요.")
        return

    with st.container(border=True):
        st.markdown("## 📘 과목 상세 정보")
        if st.button("✕ 상세 패널 닫기", key="close_detail",
                     use_container_width=True):
            close_detail()
            st.rerun()

        st.markdown(f"# {course['과목']}")
        st.markdown(
            f"<span class='pill'>{html.escape(course['분야'])}</span>"
            f"<span class='pill'>{html.escape(course['유형'])}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("### 🌱 과목 소개")
        st.write(course["소개"])
        st.markdown("### 🎯 학습 목표")
        st.write(course["학습목표"])
        st.markdown("### 🧭 관련 진로")
        st.write(course["진로"])

        st.markdown("### 📌 선택 전 확인")
        st.write("""
- 선수 과목이나 필요한 기초 개념이 있나요?
- 학교에서 실제로 개설되는 과목인가요?
- 평가 방식과 탐구 활동이 나에게 맞나요?
- 관심 진로와 어떤 관계가 있나요?
        """)

        st.markdown("### 📖 성취기준 확인")
        st.info(
            "학습 목표는 이해를 돕기 위한 요약이며 공식 성취기준 원문이 아닙니다. "
            "정확한 과목별 성취기준은 공식 교육과정 자료에서 확인해 주세요."
        )
        st.markdown(
            "[국가교육과정정보센터(NCIC)](https://www.ncic.re.kr/)"
        )
        st.markdown(
            "[고교학점제 공식 과목 안내](https://www.hscredit.kr/curriculum/subjects)"
        )

        st.markdown("### 💬 수강 후기")
        reviews = get_reviews(course["과목"])
        if not reviews:
            st.caption("아직 후기가 없어요. 첫 후기를 남겨 보세요!")
        else:
            for r in reversed(reviews):
                st.markdown(f"""
                <div class="review-card">
                <b>{html.escape(r['nickname'])}</b>
                <span class="pill">{html.escape(r['difficulty'])}</span>
                <p>{html.escape(r['content'])}</p>
                <small>{html.escape(r['date'])}</small>
                </div>
                """, unsafe_allow_html=True)
        review_form(course)

def course_card(course, prefix):
    name = course["과목"]
    fav = name in st.session_state.favorites

    with st.container(border=True):
        title_col, star_col = st.columns([5, 1])
        with title_col:
            st.markdown(f"### {name}")
            st.caption(f"{course['분야']} · {course['유형']}")
        with star_col:
            if st.button(
                "⭐" if fav else "☆",
                key=f"{prefix}_star_{name}",
                help="관심 과목 추가 또는 해제",
                use_container_width=True,
            ):
                toggle_favorite(name)
                st.rerun()

        st.write(course["소개"])
        st.caption("학습 목표 · " + course["학습목표"])
        st.caption("관련 진로 · " + course["진로"])
        if st.button(
            "📖 상세 보기",
            key=f"{prefix}_detail_{name}",
            use_container_width=True,
            type="primary" if st.session_state.selected_course == name
            and st.session_state.detail_open else "secondary",
        ):
            open_detail(name)
            st.rerun()

def course_list_with_detail(courses, prefix):
    if st.session_state.detail_open:
        left, right = st.columns([1.05, 0.95], gap="large")
        with left:
            if not courses:
                st.info("조건에 맞는 과목이 없어요.")
            for c in courses:
                course_card(c, prefix)
        with right:
            detail_panel(get_course(st.session_state.selected_course))
    else:
        if not courses:
            st.info("조건에 맞는 과목이 없어요. 검색어나 선택 조건을 바꿔 보세요.")
        for c in courses:
            course_card(c, prefix)

# =====================================================
# 5. 사이드바 페이지 메뉴
# =====================================================
with st.sidebar:
    st.markdown('<div class="nav-title">🌿 과목 선택 나침반</div>',
                unsafe_allow_html=True)
    st.caption("나에게 맞는 배움의 방향 찾기")
    st.markdown("---")
    st.markdown("### 페이지 탐색")
    st.caption("이동할 페이지를 선택하세요.")

    # 홈의 이동 버튼과 사이드바 메뉴 상태가 같은 값을 사용
    if "main_navigation" not in st.session_state:
        st.session_state.main_navigation = st.session_state.page

    selected = st.radio(
        "페이지",
        PAGES,
        key="main_navigation",
        label_visibility="collapsed",
    )
    if selected != st.session_state.page:
        st.session_state.page = selected
        close_detail()
        st.rerun()

    st.markdown("---")
    st.markdown("### 🔗 공식 자료")
    st.markdown("[고교학점제](https://www.hscredit.kr/curriculum/subjects)")
    st.markdown("[국가교육과정정보센터](https://www.ncic.re.kr/)")
    st.caption("학교별 개설 과목과 이수 계획은 담당 선생님과 확인하세요.")

# =====================================================
# 6. 홈
# =====================================================
if st.session_state.page == "🏡 홈":
    hero(
        "내 과목 선택, 천천히 시작해요!",
        "2022 개정 교육과정과 고교학점제를 위한 과목 탐색 공간",
        "🍀",
    )
    st.write(
        "과목의 특징과 학습 목표를 알아보고, 관심 분야와 희망 진로를 연결해 보세요."
    )

    a, b, c = st.columns(3)
    a.metric("탐색 분야", f"{len(RAW)}개")
    b.metric("안내 과목", f"{len(COURSES)}개")
    c.metric("관심 과목", f"{len(st.session_state.favorites)}개")

    st.markdown("## 🌼 과목 탐색")
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("### 📚 분야별 과목 보기")
            st.write("국어, 수학, 과학, 예술 등 분야별로 과목을 비교해요.")
            if st.button("분야별 과목 보기 →", key="home_category",
                         type="primary", use_container_width=True):
                go_page("📚 분야별 과목")
                st.rerun()
    with right:
        with st.container(border=True):
            st.markdown("### 🔎 과목 검색하기")
            st.write("과목 이름, 학습 내용, 진로 키워드로 검색해요.")
            if st.button("과목 검색하기 →", key="home_search",
                         type="primary", use_container_width=True):
                go_page("🔎 과목 검색")
                st.rerun()

    st.markdown("## 🌿 과목 선택 전 확인할 것")
    for title, desc in [
        ("흥미와 적성", "배우고 싶은 내용인지 생각해요."),
        ("진로와의 연결", "희망 진로에 필요한 배움인지 살펴봐요."),
        ("선수 과목", "먼저 공부하면 좋은 기초 과목이 있는지 확인해요."),
        ("학교 개설 여부", "학교의 교육과정과 실제 개설 계획을 확인해요."),
    ]:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(desc)

    st.markdown("## 📌 고교학점제")
    st.write(
        "자신의 진로와 적성에 따라 과목을 선택하고 이수하는 교육과정이에요. "
        "과목 선택 시 학교의 개설 여부와 이수 계획도 함께 확인하는 것이 좋아요."
    )

# =====================================================
# 7. 분야별 과목
# =====================================================
elif st.session_state.page == "📚 분야별 과목":
    hero("분야별 과목 탐색", "분야와 과목 유형을 선택해 살펴보세요.", "📚")
    category = st.selectbox("과목 분야", list(RAW.keys()))
    st.info(CATEGORY_INFO[category])
    kind = st.selectbox(
        "과목 유형",
        ["전체", "공통", "일반 선택", "진로 선택", "융합 선택"],
    )
    courses = [c for c in COURSES if c["분야"] == category]
    if kind != "전체":
        courses = [c for c in courses if c["유형"] == kind]
    st.caption("⭐ 색칠된 별은 관심 과목입니다. 별을 다시 누르면 해제됩니다.")
    course_list_with_detail(courses, "category")

# =====================================================
# 8. 과목 검색
# =====================================================
elif st.session_state.page == "🔎 과목 검색":
    hero("궁금한 과목을 찾아봐요", "과목 이름·분야·학습 내용·진로를 검색해요.", "🔎")
    query = st.text_input(
        "검색어",
        placeholder="예: 인공지능, 미적분, 생명과학, 경제",
    )
    kind = st.selectbox(
        "과목 유형",
        ["전체", "공통", "일반 선택", "진로 선택", "융합 선택"],
        key="search_kind",
    )
    results = []
    for c in COURSES:
        searchable = " ".join([
            c["과목"], c["분야"], c["유형"], c["소개"],
            c["학습목표"], c["진로"],
        ])
        if query.strip().lower() not in searchable.lower():
            continue
        if kind != "전체" and c["유형"] != kind:
            continue
        results.append(c)
    st.write(f"검색 결과: **{len(results)}개**")
    course_list_with_detail(results, "search")

# =====================================================
# 9. 관심 과목
# =====================================================
elif st.session_state.page == "⭐ 나의 관심 과목":
    hero("나의 관심 과목", "관심 과목을 모아 비교하고 상세 내용을 확인해요.", "⭐")
    courses = [
        get_course(n) for n in st.session_state.favorites if get_course(n)
    ]
    if not courses:
        st.info("아직 관심 과목이 없어요. 분야별 과목에서 ☆를 눌러 추가해 보세요.")
    else:
        course_list_with_detail(courses, "favorite")

# =====================================================
# 10. 수강 후기
# =====================================================
elif st.session_state.page == "💬 수강 후기":
    hero("수강 후기 나눔터", "수강 경험과 공부 조언을 나누어요.", "💬")
    st.warning(
        "현재 후기는 세션에 임시 저장됩니다. 앱 재시작이나 세션 종료 후에도 "
        "영구 보존하고 여러 학생이 공유하려면 데이터베이스 연결이 필요합니다."
    )
    filter_course = st.selectbox("과목별 후기", ["전체 과목"] + NAMES)
    reviews = st.session_state.reviews
    if filter_course != "전체 과목":
        reviews = [r for r in reviews if r["course"] == filter_course]

    if reviews:
        for i, r in enumerate(reversed(reviews)):
            with st.container(border=True):
                st.markdown(f"### {r['course']}")
                st.caption(
                    f"{r['nickname']} · {r['difficulty']} · {r['date']}"
                )
                st.write(r["content"])
                if st.button("과목 상세 보기", key=f"review_detail_{i}"):
                    open_detail(r["course"])
                    st.rerun()
    else:
        st.info("아직 후기가 없어요.")

    st.markdown("---")
    st.markdown("## ✍️ 후기 작성")
    with st.form("general_review", clear_on_submit=True):
        course_name = st.selectbox("과목", NAMES)
        nickname = st.text_input("별명", max_chars=20)
        difficulty = st.select_slider(
            "체감 난이도",
            options=["쉬웠어요","조금 쉬웠어요","보통이에요",
                     "조금 어려웠어요","어려웠어요"],
            value="보통이에요",
        )
        content = st.text_area("후기와 공부 조언", max_chars=1000)
        submit = st.form_submit_button("후기 등록", type="primary")
        if submit:
            if not nickname.strip():
                st.error("별명을 입력해 주세요.")
            elif len(content.strip()) < 10:
                st.error("후기를 10자 이상 작성해 주세요.")
            else:
                st.session_state.reviews.append({
                    "course": course_name,
                    "nickname": nickname.strip(),
                    "difficulty": difficulty,
                    "content": content.strip(),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                })
                st.session_state.toast_message = "💬 후기가 등록되었어요!"
                st.session_state.toast_id += 1
                st.rerun()

    if st.session_state.detail_open:
        st.markdown("---")
        detail_panel(get_course(st.session_state.selected_course))

# =====================================================
# 11. 강화된 과목 선택 가이드
# =====================================================
elif st.session_state.page == "🧭 과목 선택 가이드":
    hero(
        "나에게 맞는 과목 선택 가이드",
        "여러 조건을 선택하면 조건에 맞는 과목을 찾아볼 수 있어요.",
        "🧭",
    )

    st.markdown("## 1. 어떤 유형의 과목을 찾고 있나요?")
    selected_kinds = st.multiselect(
        "탐색할 과목 유형 (여러 개 선택 가능)",
        ["일반 선택", "진로 선택", "융합 선택"],
        default=["일반 선택", "진로 선택", "융합 선택"],
        help="일반 선택은 폭넓은 학습, 진로 선택은 관심 진로 심화, "
             "융합 선택은 여러 분야를 연결하는 탐색의 관점에서 살펴볼 수 있어요.",
    )

    with st.expander("과목 유형의 차이 알아보기", expanded=False):
        st.markdown("""
**일반 선택**
- 교과의 주요 개념과 기본 소양을 폭넓게 학습하는 데 도움이 돼요.

**진로 선택**
- 관심 분야나 진로와 관련된 학습을 더 깊이 탐색하는 데 활용할 수 있어요.

**융합 선택**
- 여러 분야의 지식과 관점을 연결해 문제를 살펴보는 데 도움이 돼요.

실제 과목의 분류와 개설 여부는 적용 교육과정 및 학교 편성표에서 확인하세요.
        """)

    st.markdown("## 2. 현재 관심 있는 분야")
    interests = st.multiselect(
        "관심 분야를 선택해 주세요.",
        INTERESTS,
        help="관심 있는 분야를 여러 개 고를 수 있어요. 아직 진로를 정하지 않아도 괜찮아요.",
    )

    st.markdown("## 3. 현재 나의 학습 상황")
    c1, c2 = st.columns(2)
    with c1:
        grade_stage = st.radio(
            "현재 상황",
            ["아직 진로를 탐색 중", "관심 진로가 생기는 중",
             "희망 진로가 비교적 뚜렷함"],
        )
        study_style = st.selectbox(
            "선호하는 학습 방식",
            ["개념을 차근차근 이해하기", "문제 해결과 논리적 사고",
             "실험·실습·직접 만들어 보기", "토론·읽기·글쓰기",
             "프로젝트와 여러 과목 연결하기", "아직 잘 모르겠음"],
        )
    with c2:
        challenge = st.selectbox(
            "새로운 과목에 도전하는 정도",
            ["기초부터 안정적으로", "적당히 도전하기",
             "관심 분야는 깊이 도전하기", "다양한 분야를 경험하기"],
        )
        workload = st.selectbox(
            "과목 선택에서 중요하게 보는 점",
            ["흥미와 호기심", "희망 진로와의 연결", "기초 개념과 학습 준비",
             "탐구·실습 활동", "여러 분야의 융합", "균형 있는 학업 계획"],
        )

    st.markdown("## 4. 가장 중요하게 생각하는 기준")
    priorities = st.multiselect(
        "최대 3개까지 선택해 주세요.",
        ["흥미와 적성", "진로와의 연관성", "기초 실력 쌓기",
         "탐구 능력 기르기", "실생활 문제 해결",
         "창의적인 활동", "다양한 분야 경험"],
        default=["흥미와 적성"],
        max_selections=3,
    )

    st.markdown("## 5. 더 탐색하고 싶은 학습 주제")
    topics = st.multiselect(
        "관심 있는 주제 (선택 사항)",
        [
            "데이터 분석", "인공지능과 소프트웨어", "환경과 기후",
            "인간의 심리", "사회 문제", "경제와 금융",
            "언어와 문화", "역사와 철학", "건강과 생명",
            "예술과 디자인", "공학과 설계", "토론과 글쓰기",
        ],
    )

    st.markdown("## 6. 과목 선택 시 고려할 점")
    consider_foundation = st.checkbox("기초 개념을 충분히 배울 수 있는지 중요해요.")
    consider_career = st.checkbox("진로와 연결되는 과목을 우선 살펴보고 싶어요.")
    consider_project = st.checkbox("프로젝트나 탐구 활동이 있는 과목에 관심이 있어요.")

    if st.button("🌱 맞춤 과목 찾아보기", type="primary",
                 use_container_width=True):
        # 선택한 조건을 바탕으로 과목에 점수를 부여
        scored = []
        topic_map = {
            "데이터 분석": ["수학·데이터"],
            "인공지능과 소프트웨어": ["공학·컴퓨터", "수학·데이터"],
            "환경과 기후": ["환경·생태", "자연과학"],
            "인간의 심리": ["교육·심리"],
            "사회 문제": ["사회·법"],
            "경제와 금융": ["경제·경영", "수학·데이터"],
            "언어와 문화": ["인문·언어", "국제·외국어"],
            "역사와 철학": ["인문·언어", "사회·법"],
            "건강과 생명": ["의료·보건", "자연과학"],
            "예술과 디자인": ["예술·디자인"],
            "공학과 설계": ["공학·컴퓨터"],
            "토론과 글쓰기": ["인문·언어", "사회·법"],
        }

        for course in COURSES:
            score = 0
            if selected_kinds and course["유형"] not in selected_kinds:
                continue

            career_tags = [
                x.strip() for x in course["진로"].split(",")
            ]
            for interest in interests:
                if interest in career_tags:
                    score += 4

            for topic in topics:
                if any(tag in career_tags for tag in topic_map.get(topic, [])):
                    score += 3

            # 선호하는 학습 방식과 학습 목표를 간단히 연결
            goals = course["소개"] + " " + course["학습목표"]
            if study_style == "문제 해결과 논리적 사고" and (
                course["분야"] == "수학" or "분석" in goals or "문제 해결" in goals
            ):
                score += 2
            if study_style == "실험·실습·직접 만들어 보기" and (
                course["분야"] in ["과학", "정보·기술·가정", "체육", "예술"]
            ):
                score += 2
            if study_style == "토론·읽기·글쓰기" and (
                course["분야"] in ["국어", "사회", "제2외국어·한문"]
            ):
                score += 2
            if study_style == "프로젝트와 여러 과목 연결하기" and course["유형"] == "융합 선택":
                score += 3

            if "기초" in workload and course["유형"] == "공통":
                score += 2
            if consider_foundation and course["유형"] == "공통":
                score += 2
            if consider_career and interests and any(
                interest in career_tags for interest in interests
            ):
                score += 2
            if consider_project and course["유형"] == "융합 선택":
                score += 2

            if "실생활 문제 해결" in priorities and (
                "문제 해결" in goals or "생활" in goals
            ):
                score += 1
            if "탐구 능력 기르기" in priorities and (
                "탐구" in goals or "분석" in goals
            ):
                score += 1
            if "창의적인 활동" in priorities and (
                course["분야"] == "예술" or course["유형"] == "융합 선택"
            ):
                score += 1
            if "기초 실력 쌓기" in priorities and course["유형"] == "공통":
                score += 1
            if "다양한 분야 경험" in priorities and course["유형"] == "융합 선택":
                score += 1

            # 관심 분야가 없으면 모든 과목을 동등하게 탐색할 수 있도록 유지
            scored.append((score, course))

        scored.sort(key=lambda x: (-x[0], x[1]["과목"]))
        st.session_state.guide_results = [
            c["과목"] for score, c in scored if score > 0
        ][:20]
        if not st.session_state.guide_results:
            st.session_state.guide_results = [
                c["과목"] for score, c in scored[:12]
            ]
        st.session_state.guide_profile = {
            "유형": selected_kinds,
            "관심 분야": interests,
            "상황": grade_stage,
            "학습 방식": study_style,
            "도전 수준": challenge,
            "중요 기준": priorities,
            "주제": topics,
            "추가 고려": [
                label for label, checked in [
                    ("기초 개념", consider_foundation),
                    ("진로 연계", consider_career),
                    ("탐구·프로젝트", consider_project),
                ] if checked
            ],
        }
        st.session_state.guide_done = True

    if st.session_state.get("guide_done"):
        st.markdown("---")
        st.markdown("## 🌼 추천 과목")
        profile = st.session_state.guide_profile
        st.write(
            f"선택한 유형: {', '.join(profile['유형']) if profile['유형'] else '선택 없음'}"
        )
        st.write(
            f"관심 분야: {', '.join(profile['관심 분야']) if profile['관심 분야'] else '아직 탐색 중'}"
        )
        st.caption(
            "추천 결과는 선택한 조건과 과목의 분야·유형을 바탕으로 한 탐색용 제안이에요. "
            "적성이나 성적을 예측하는 결과가 아니며, 대학별 필수 과목을 의미하지 않습니다."
        )
        recommendations = [
            get_course(n) for n in st.session_state.guide_results
            if get_course(n)
        ]
        course_list_with_detail(recommendations, "guide")

    st.markdown("---")
    st.markdown("## 📌 마지막으로 확인해요")
    st.write("""
- 학교에서 실제로 개설하는지 확인하세요.
- 선수 과목과 이수 순서를 확인하세요.
- 대학의 권장 과목은 대학·학과·모집 연도별 공식 안내를 확인하세요.
- 담임 선생님이나 진로 담당 선생님과 상담해 본인의 학업 계획을 세우세요.
    """)
    st.markdown("[국가교육과정정보센터](https://www.ncic.re.kr/)")

# =====================================================
# 12. 하단 안내
# =====================================================
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#71806b'>"
    "🌿 과목 선택 나침반 · 나에게 맞는 배움을 찾아가는 여정"
    "</div>",
    unsafe_allow_html=True,
)
