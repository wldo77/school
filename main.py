
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

# =========================================================
# 1. 디자인
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap');

:root {
    --cream: #fbf8ed;
    --green: #426b50;
    --light-green: #e7efdf;
    --dark-green: #294b36;
    --yellow: #f4d77b;
}
html, body, [class*="css"] {
    font-family: 'Gowun Dodum', sans-serif;
}
.stApp {
    background: linear-gradient(150deg, #fbf8ed, #f1f3e7 60%, #e7efdf);
}
.block-container {
    max-width: 1350px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}
h1, h2, h3 {
    font-family: 'Jua', sans-serif !important;
    color: #294b36 !important;
}
h1 { font-size: 2.4rem !important; }
h2 { font-size: 1.8rem !important; }
h3 { font-size: 1.3rem !important; }
p, label, li, .stMarkdown {
    font-size: 1.02rem;
    line-height: 1.7;
}
div.stButton > button {
    border-radius: 13px;
    border: 1px solid #cbd9c5;
    background: #fffdf6;
    color: #294b36;
    min-height: 43px;
    font-weight: 700;
    transition: all .18s ease;
}
div.stButton > button:hover {
    background: #e7efdf;
    border-color: #426b50;
    transform: translateY(-1px);
}
div.stButton > button[kind="primary"] {
    background: #426b50;
    color: white;
    border-color: #426b50;
}
div[data-testid="stSidebar"] {
    background: #edf1e4;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    font-family: 'Jua', sans-serif;
    font-size: 1.05rem;
    color: #294b36;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 7px;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > div > label {
    background: #fffdf6;
    border: 1px solid #d2dfcb;
    border-radius: 12px;
    padding: 10px 12px;
    margin: 0;
    transition: all .15s ease;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > div > label:hover {
    background: #e1ecd9;
    border-color: #789875;
}
div[data-testid="stSidebar"] [data-testid="stRadio"] > div > label:has(input:checked) {
    background: #426b50;
    border-color: #426b50;
    color: white;
}
.hero {
    background: linear-gradient(120deg, #e6efdc, #fff4d5);
    border: 1px solid #d6e2ce;
    border-radius: 24px;
    padding: 26px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Jua', sans-serif;
    font-size: 2.25rem;
    line-height: 1.4;
    color: #294b36;
}
.hero-sub {
    color: #536650;
    font-size: 1.08rem;
    margin-top: 8px;
}
.pill {
    display: inline-block;
    background: #e7efdf;
    color: #365c40;
    border-radius: 999px;
    padding: 4px 11px;
    margin: 2px 4px 2px 0;
    font-size: .86rem;
}
.info-box {
    background: #fffdf6;
    border-left: 4px solid #8ca87a;
    border-radius: 10px;
    padding: 13px 16px;
    margin: 8px 0;
}
.course-card {
    background: rgba(255,253,246,.95);
    border: 1px solid #dfe6d6;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 10px;
}
.detail-panel {
    background: rgba(255,253,246,.96);
    border: 2px solid #cdddc4;
    border-radius: 20px;
    padding: 18px;
}
.detail-heading {
    font-family: 'Jua', sans-serif;
    color: #294b36;
    font-size: 1.7rem;
}
.review-card {
    background: #fffdf7;
    border: 1px solid #dfe6d6;
    border-radius: 13px;
    padding: 14px;
    margin: 9px 0;
}
.star-help {
    font-size: .9rem;
    color: #687662;
}
div[data-testid="stMetric"] {
    background: #fffdf6;
    border: 1px solid #dfe6d6;
    padding: 12px;
    border-radius: 15px;
}
hr { border-color: #dce4d4; }
@media (max-width: 700px) {
    .hero-title { font-size: 1.8rem; }
    h1 { font-size: 2rem !important; }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 2. 과목 데이터
# 형식: 과목명 | 과목 유형 | 소개 | 학습 목표 요약 | 관련 진로
# =========================================================
RAW = {
"국어": [
("공통국어1","공통","읽기·쓰기·말하기의 기초를 다지고 다양한 자료를 이해한다.","글의 핵심 내용과 구조 파악, 생각을 말과 글로 표현하기","독서, 언론, 교육, 콘텐츠"),
("공통국어2","공통","다양한 언어 활동을 통해 의사소통 역량을 기른다.","자료를 비판적으로 읽고 목적과 맥락에 맞게 표현하기","교육, 출판, 미디어"),
("화법과 언어","일반 선택","말하기와 듣기, 언어의 구조와 사용을 탐구한다.","상황에 적절한 의사소통 전략 활용, 언어 현상 분석하기","언론, 교육, 광고"),
("독서와 작문","일반 선택","글을 깊이 읽고 논리적으로 글을 작성한다.","글의 관점과 근거 평가, 목적에 맞는 글쓰기","인문, 법, 연구"),
("문학","일반 선택","문학 작품의 의미와 가치를 감상하고 해석한다.","작품의 내용·형식·맥락을 고려하여 해석하기","문예창작, 문화, 교육"),
("주제 탐구 독서","진로 선택","관심 주제를 중심으로 여러 자료를 읽고 탐구한다.","자료 비교·분석, 탐구 결과 정리하기","연구, 인문사회"),
("독서 토론과 글쓰기","융합 선택","독서와 토론을 연결하여 논리적인 글을 쓴다.","근거를 들어 토론하고 주장을 글로 구성하기","언론, 법, 교육"),
],
"수학": [
("공통수학1","공통","식과 방정식 등 수학의 기본 개념을 학습한다.","수학적 개념 이해, 식과 방정식의 문제 해결","공학, 자연과학, 경제"),
("공통수학2","공통","함수와 도형 등 여러 수학 개념을 연결한다.","수학적 관계 표현, 문제 해결 과정 설명하기","공학, 컴퓨터, 경제"),
("대수","일반 선택","지수·로그 및 수열 등 대수적 관계를 다룬다.","대수적 표현을 활용하여 수학적 문제 해결하기","공학, 데이터, 금융"),
("미적분Ⅰ","일반 선택","함수의 극한과 미분·적분의 기초를 학습한다.","변화율과 누적량을 수학적으로 해석하기","공학, 물리, 경제"),
("확률과 통계","일반 선택","불확실한 상황과 자료를 수학적으로 분석한다.","확률 계산, 통계 자료 해석하기","통계, 경영, 사회과학"),
("기하","진로 선택","도형과 공간을 벡터 등으로 탐구한다.","공간적 관계를 표현하고 기하 문제 해결하기","건축, 디자인, 공학"),
("경제 수학","진로 선택","경제 현상을 수학적 관계로 분석한다.","경제 자료와 수학적 모델 연결하기","경제, 금융, 경영"),
("실용 통계","융합 선택","실생활 자료를 수집하고 통계적으로 해석한다.","자료 정리, 통계적 해석, 결과 전달하기","사회과학, 마케팅, 데이터"),
],
"영어": [
("공통영어1","공통","영어로 된 다양한 자료를 이해하고 표현한다.","중심 내용 파악, 상황에 맞는 영어 의사소통","국제, 관광, 교육"),
("공통영어2","공통","영어 의사소통 능력과 문화 이해를 넓힌다.","자료의 핵심 정보 이해, 자신의 의견 표현하기","무역, 국제, 미디어"),
("영어Ⅰ","일반 선택","다양한 주제의 영어 자료를 이해한다.","글의 세부 정보와 중심 생각 파악하기","인문, 국제, 경영"),
("영어Ⅱ","일반 선택","복합적인 영어 자료를 읽고 의사소통한다.","자료를 분석하고 영어로 의견을 전달하기","국제, 연구, 교육"),
("영어 독해와 작문","일반 선택","영어 글을 읽고 목적에 맞게 글을 쓴다.","글의 논리 구조 이해, 목적에 맞는 작문","출판, 국제, 미디어"),
("영어 발표와 토론","진로 선택","영어로 발표하고 근거를 들어 토론한다.","발표 구성, 근거 제시, 상호작용하기","국제, 외교, 관광"),
("미디어 영어","융합 선택","미디어 속 영어 표현과 정보를 탐구한다.","미디어 자료 분석, 정보의 신뢰성 살피기","미디어, 광고, 콘텐츠"),
],
"사회": [
("통합사회1","공통","인간과 사회, 공간, 환경의 관계를 통합적으로 살핀다.","사회 현상을 여러 관점에서 이해하고 설명하기","사회복지, 행정, 경제"),
("통합사회2","공통","사회 문제와 지속가능한 삶을 탐구한다.","사회 문제 분석, 합리적인 해결 방안 탐색하기","정책, 환경, 국제"),
("한국사1","공통","한국사의 흐름과 역사적 변화를 이해한다.","사료를 활용해 역사적 사실과 의미 파악하기","역사, 교육, 문화"),
("세계시민과 지리","일반 선택","세계의 지역과 세계화 현상을 지리적으로 이해한다.","지도·자료를 활용해 지역의 특성 분석하기","지리, 국제, 도시"),
("세계사","일반 선택","세계 여러 지역의 역사적 변화와 교류를 탐구한다.","역사 자료 비교, 변화와 연속성 이해하기","역사, 국제, 문화"),
("사회와 문화","일반 선택","사회 구조와 문화 현상을 탐구한다.","사회 자료 분석, 사회 현상에 대한 관점 비교하기","사회학, 복지, 조사"),
("정치","진로 선택","정치 과정과 시민의 참여를 이해한다.","정치 제도와 쟁점 분석, 참여 방법 탐색하기","정치외교, 행정, 법"),
("법과 사회","진로 선택","법의 원리와 사회생활 속 법적 쟁점을 탐구한다.","법적 쟁점 파악, 근거를 활용한 판단하기","법, 경찰행정, 행정"),
("경제","진로 선택","경제 주체의 선택과 시장의 작동 원리를 학습한다.","경제 자료 해석, 선택의 결과 분석하기","경제, 경영, 금융"),
("사회문제 탐구","융합 선택","현실의 사회 문제를 조사하고 해결 방안을 모색한다.","문제 설정, 자료 조사, 대안 제안하기","사회복지, 정책, 연구"),
("기후변화와 지속가능한 세계","융합 선택","기후 변화와 지속가능성을 다양한 관점에서 살핀다.","환경 자료 분석, 지속가능한 실천 방안 제안하기","환경, 지리, 정책"),
],
"과학": [
("통합과학1","공통","물질과 자연 현상을 통합적인 관점에서 이해한다.","과학 개념을 연결하고 탐구 자료를 해석하기","자연과학, 공학, 보건"),
("통합과학2","공통","생명과 환경 등 과학적 현상을 연결해 탐구한다.","과학적 근거를 활용해 현상을 설명하기","생명과학, 환경, 공학"),
("과학탐구실험1","공통","과학 탐구의 기초와 실험 방법을 익힌다.","관찰·측정·기록, 안전한 실험 수행하기","연구, 보건, 공학"),
("물리학","일반 선택","운동과 에너지 등 물리 현상을 이해한다.","물리 개념과 수학적 표현을 이용해 현상 설명하기","물리, 기계, 전기전자"),
("화학","일반 선택","물질의 구조와 성질, 화학 반응을 학습한다.","물질의 성질과 변화를 입자 관점에서 설명하기","화학, 약학, 재료"),
("생명과학","일반 선택","생명체의 구조와 생명 현상을 탐구한다.","생명 현상에 관한 자료 분석과 설명하기","생명, 보건, 생태"),
("지구과학","일반 선택","지구와 우주에서 일어나는 현상을 학습한다.","관측 자료를 해석해 지구 시스템 설명하기","지질, 기상, 천문"),
("역학과 에너지","진로 선택","운동과 에너지의 관계를 깊이 탐구한다.","물리 법칙을 활용하여 운동 현상 분석하기","기계, 항공, 물리"),
("생물의 유전","진로 선택","유전 현상과 유전 정보의 전달을 탐구한다.","유전 자료 해석, 생명 현상 설명하기","생명공학, 의생명"),
("기후변화와 환경생태","융합 선택","기후와 생태계의 변화를 과학적으로 탐구한다.","환경 자료 해석, 생태계 보전 방안 제안하기","환경, 생태, 기후"),
("융합과학 탐구","융합 선택","여러 과학 분야를 연결하여 탐구 활동을 수행한다.","탐구 질문 설정, 증거 수집, 결과 발표하기","융합연구, 공학"),
],
"체육": [
("체육1","일반 선택","신체활동을 통해 건강과 운동 기능을 기른다.","운동 기능 향상, 건강한 생활 습관 실천하기","체육, 스포츠, 보건"),
("체육2","일반 선택","다양한 신체활동에 참여하고 협력한다.","운동 전략 활용, 규칙과 협동의 가치 실천하기","스포츠, 교육, 건강"),
("운동과 건강","진로 선택","운동과 건강의 관계를 이해하고 실천한다.","개인에게 맞는 운동 계획 수립과 실천하기","스포츠과학, 보건"),
("스포츠 문화","진로 선택","스포츠의 사회적·문화적 의미를 탐구한다.","스포츠와 사회의 관계를 분석하기","스포츠산업, 체육교육"),
("스포츠 생활1","융합 선택","생활 속 스포츠 참여와 건강한 여가를 탐색한다.","안전하고 지속적인 스포츠 활동 계획하기","스포츠, 여가, 건강"),
],
"예술": [
("음악","일반 선택","음악을 듣고 표현하며 음악 문화를 이해한다.","음악 요소 탐색, 감상과 표현 활동하기","음악, 공연, 교육"),
("미술","일반 선택","시각적 표현과 감상을 통해 생각을 나타낸다.","시각 요소 활용, 작품 감상과 해석하기","디자인, 미술, 콘텐츠"),
("연극","일반 선택","연극의 표현 방식과 협력적 창작을 경험한다.","역할 표현, 장면 구성, 협력적 공연 만들기","연극, 영상, 공연"),
("음악 연주와 창작","진로 선택","음악을 연주하고 창의적으로 구성한다.","음악적 아이디어 표현과 창작하기","음악, 작곡, 공연"),
("미술 창작","진로 선택","다양한 재료와 방법으로 시각 작품을 만든다.","주제 구상, 표현 방법 선택, 작품 제작하기","미술, 디자인, 공예"),
("음악과 미디어","융합 선택","음악과 디지털 미디어의 관계를 탐구한다.","음악을 매체에 맞게 표현하고 감상하기","음향, 미디어, 콘텐츠"),
("미술과 매체","융합 선택","다양한 매체를 활용한 시각 표현을 탐구한다.","매체 특성 이해, 시각 콘텐츠 제작하기","디자인, 영상, 광고"),
],
"정보·기술·가정": [
("정보","일반 선택","디지털 정보와 컴퓨팅 사고를 학습한다.","문제 분해, 알고리즘 설계, 데이터 활용하기","소프트웨어, AI, 데이터"),
("인공지능 기초","진로 선택","인공지능의 기본 개념과 활용 사례를 이해한다.","인공지능 원리와 사회적 영향 탐색하기","AI, 로봇, 데이터"),
("데이터 과학","진로 선택","데이터를 수집·분석하여 의미를 찾는다.","데이터 처리, 시각화, 결과 해석하기","데이터 분석, 연구"),
("소프트웨어와 생활","융합 선택","생활 속 문제를 소프트웨어로 해결한다.","문제 정의, 프로그램 설계, 결과 개선하기","개발, 창업, 자동화"),
("기술·가정","일반 선택","기술과 생활, 가족과 자립에 관한 내용을 탐구한다.","생활 문제 해결, 지속가능한 생활 실천하기","공학, 생활과학, 교육"),
("로봇과 공학세계","진로 선택","로봇과 공학 기술의 원리를 탐색한다.","공학 문제 분석, 설계 아이디어 제안하기","로봇, 기계, 전자"),
("창의 공학 설계","진로 선택","설계 과정을 통해 실생활 문제를 해결한다.","아이디어 구상, 설계·제작·평가하기","공학, 제품디자인"),
],
"제2외국어·한문": [
("중국어","일반 선택","중국어의 기초 표현과 중국 문화를 학습한다.","기초 의사소통, 문화 자료 이해하기","중국, 무역, 관광"),
("일본어","일반 선택","일본어의 기초 표현과 일본 문화를 학습한다.","일상 표현 활용, 문화적 맥락 이해하기","일본, 관광, 콘텐츠"),
("스페인어","일반 선택","스페인어의 기초 의사소통을 익힌다.","기초 표현 활용, 스페인어권 문화 이해하기","국제, 관광, 외교"),
("프랑스어","일반 선택","프랑스어의 기초 표현과 문화를 탐구한다.","기초 의사소통, 문화적 차이 이해하기","국제, 문화, 예술"),
("일본 문화","융합 선택","일본의 사회와 문화를 다양한 자료로 탐구한다.","문화 자료 해석, 한국과의 공통점·차이점 살피기","국제, 문화, 콘텐츠"),
("중국 문화","융합 선택","중국의 역사와 생활 문화를 이해한다.","문화 자료 비교와 문화적 맥락 이해하기","국제, 무역, 문화"),
("한문","일반 선택","한자와 한문 문장을 이해하고 활용한다.","한자 어휘 이해, 한문 문장의 의미 파악하기","인문, 역사, 언어"),
],
"교양": [
("진로와 직업","일반 선택","자신의 흥미와 적성을 탐색하고 진로를 설계한다.","진로 정보 탐색, 진로 목표와 계획 세우기","모든 진로 분야"),
("생태와 환경","일반 선택","생태계와 환경 문제, 지속가능한 삶을 탐구한다.","환경 문제 분석, 생활 속 실천 방안 제안하기","환경, 생태, 정책"),
("인간과 심리","진로 선택","인간의 심리와 행동을 이해한다.","심리 현상을 여러 관점에서 살펴보기","심리, 상담, 교육"),
("교육의 이해","진로 선택","교육의 의미와 사회적 역할을 탐구한다.","교육 현상 분석, 교육의 가치와 역할 성찰하기","교육, 상담, 정책"),
("보건","진로 선택","건강한 생활과 건강 관리 방법을 이해한다.","건강 정보 판단, 건강한 생활 습관 계획하기","보건, 간호, 복지"),
("논리와 사고","진로 선택","논리적 사고와 합리적 판단 방법을 학습한다.","주장과 근거 구별, 추론의 타당성 살피기","철학, 법, 연구"),
("금융과 경제생활","융합 선택","생활 속 금융과 합리적인 경제 의사결정을 탐구한다.","소비·저축·금융 정보 이해와 계획 세우기","금융, 경제, 경영"),
],
}

CATEGORY_INFO = {
"국어":"읽기, 쓰기, 말하기, 문학을 통해 생각을 표현하고 다른 사람의 관점을 이해하는 분야예요.",
"수학":"수량과 관계를 논리적으로 분석하고 문제를 해결하는 힘을 기르는 분야예요.",
"영어":"영어 자료를 이해하고 자신의 생각을 전달하며 다양한 문화를 이해하는 분야예요.",
"사회":"사회 현상, 역사, 지리, 정치, 경제를 탐구하며 세상을 이해하는 분야예요.",
"과학":"자연 현상을 관찰하고 실험과 증거를 바탕으로 설명하는 분야예요.",
"체육":"신체활동과 스포츠를 통해 건강, 협력, 운동 능력을 기르는 분야예요.",
"예술":"음악, 미술, 연극을 통해 생각과 감정을 창의적으로 표현하는 분야예요.",
"정보·기술·가정":"디지털 기술과 공학, 생활 속 문제 해결을 다루는 분야예요.",
"제2외국어·한문":"새로운 언어와 문화를 이해하고 의사소통의 폭을 넓히는 분야예요.",
"교양":"진로, 환경, 심리, 보건 등 삶에 필요한 지식과 태도를 탐구하는 분야예요.",
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

COURSE_NAMES = [c["과목"] for c in COURSES]

# =========================================================
# 3. 세션 상태
# =========================================================
defaults = {
    "page": "🏡 홈",
    "favorites": [],
    "reviews": [],
    "selected_course": None,
    "detail_open": False,
    "toast_message": "",
    "toast_id": 0,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def get_course(name):
    return next((c for c in COURSES if c["과목"] == name), None)

def get_reviews(name):
    return [r for r in st.session_state.reviews if r["course"] == name]

def toggle_favorite(name):
    if name in st.session_state.favorites:
        st.session_state.favorites.remove(name)
        message = f"⭐ {name} 과목을 관심 목록에서 제외했어요."
    else:
        st.session_state.favorites.append(name)
        message = f"⭐ {name} 과목을 관심 목록에 추가했어요."

    st.session_state.toast_message = message
    st.session_state.toast_id += 1

def set_detail(name):
    st.session_state.selected_course = name
    st.session_state.detail_open = True

def close_detail():
    st.session_state.detail_open = False
    st.session_state.selected_course = None

# =========================================================
# 4. 공통 헤더와 하단 알림
# =========================================================
def hero(title, subtitle, emoji="🌿"):
    st.markdown(f"""
    <div class="hero">
      <div style="font-size:2.3rem">{emoji}</div>
      <div class="hero-title">{html.escape(title)}</div>
      <div class="hero-sub">{html.escape(subtitle)}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.toast_message:
    safe_message = html.escape(st.session_state.toast_message)
    toast_id = st.session_state.toast_id
    components.html(f"""
    <div id="toast-{toast_id}" style="
      position:fixed; bottom:25px; left:50%; transform:translateX(-50%);
      z-index:999999; background:#294b36; color:white;
      padding:14px 24px; border-radius:14px;
      box-shadow:0 5px 20px #0003; font-size:16px;
      font-family:sans-serif; text-align:center; width:max-content;
      max-width:90vw;">
      {safe_message}
    </div>
    <script>
    setTimeout(() => {{
      const el = document.getElementById("toast-{toast_id}");
      if (el) {{
        el.style.transition = "opacity .25s";
        el.style.opacity = "0";
        setTimeout(() => el.remove(), 300);
      }}
    }}, 3000);
    </script>
    """, height=1)

    # 다음 rerun에서는 같은 알림이 다시 나타나지 않도록 처리
    st.session_state.toast_message = ""

# =========================================================
# 5. 상세 패널
# =========================================================
def show_review_form(course):
    with st.expander("✍️ 이 과목 후기 남기기", expanded=False):
        st.caption("실제로 수강한 경험을 공유해 주세요. 실명·연락처 등 개인정보는 적지 마세요.")
        form_key = "review_form_" + course["과목"]

        with st.form(form_key, clear_on_submit=True):
            nickname = st.text_input("별명", max_chars=20, key=form_key+"_nick")
            difficulty = st.select_slider(
                "체감 난이도",
                options=["쉬웠어요", "조금 쉬웠어요", "보통이에요",
                         "조금 어려웠어요", "어려웠어요"],
                value="보통이에요",
                key=form_key+"_diff",
            )
            content = st.text_area(
                "후기와 공부 조언",
                placeholder="배운 내용, 어려웠던 점, 도움이 된 공부 방법을 적어 주세요.",
                max_chars=1000,
                height=120,
                key=form_key+"_content",
            )
            submitted = st.form_submit_button("후기 등록하기", type="primary")

            if submitted:
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

def show_detail_panel(course):
    if not course:
        st.info("왼쪽에서 과목의 상세 보기를 눌러 주세요.")
        return

    st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
    st.markdown('<div class="detail-heading">📘 과목 상세 정보</div>', unsafe_allow_html=True)
    st.caption("선택한 과목의 학습 정보와 후기를 확인할 수 있어요.")

    if st.button("✕ 상세 패널 닫기", key="close_detail", use_container_width=True):
        close_detail()
        st.rerun()

    st.markdown(f"## {course['과목']}")
    st.markdown(
        f"<span class='pill'>{html.escape(course['분야'])}</span>"
        f"<span class='pill'>{html.escape(course['유형'])}</span>",
        unsafe_allow_html=True,
    )

    st.markdown("### 🌱 어떤 과목인가요?")
    st.write(course["소개"])

    st.markdown("### 🎯 주요 학습 목표")
    st.write(course["학습목표"])

    st.markdown("### 🧭 연결되는 진로")
    st.write(course["진로"])

    st.markdown("### 📝 선택 전 확인 사항")
    st.markdown("""
    - 이 과목에서 배우는 내용에 관심이 있나요?
    - 희망 진로 또는 앞으로 탐색할 분야와 연결되나요?
    - 선수 과목이나 기초 개념을 먼저 배워야 하나요?
    - 우리 학교에서 실제로 개설되나요?
    - 평가 방법과 과제·탐구 활동이 나에게 맞을까요?
    """)

    st.markdown("### 📖 성취기준 안내")
    st.info(
        "아래 학습 목표는 학생의 이해를 돕기 위해 요약한 내용이며, "
        "공식 성취기준 원문을 그대로 옮긴 것은 아니에요."
    )
    st.markdown(
        "[국가교육과정정보센터(NCIC)에서 교육과정 확인하기](https://www.ncic.re.kr/)"
    )
    st.markdown(
        "[고교학점제 공식 과목 안내](https://www.hscredit.kr/curriculum/subjects)"
    )

    st.markdown("---")
    st.markdown("### 💬 이 과목의 수강 후기")

    reviews = get_reviews(course["과목"])
    if not reviews:
        st.caption("아직 등록된 후기가 없어요. 첫 후기를 남겨 보세요!")
    else:
        st.caption(f"등록된 후기 {len(reviews)}개")
        for r in reversed(reviews):
            st.markdown(f"""
            <div class="review-card">
              <span class="pill">{html.escape(r['difficulty'])}</span>
              <b>{html.escape(r['nickname'])}</b>
              <p>{html.escape(r['content'])}</p>
              <div style="color:#77836f;font-size:.85rem">{html.escape(r['date'])}</div>
            </div>
            """, unsafe_allow_html=True)

    show_review_form(course)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 6. 과목 카드
# 관심 별과 상세 보기 버튼을 모든 목록에서 공통 사용
# =========================================================
def render_course_card(course, prefix):
    name = course["과목"]
    is_fav = name in st.session_state.favorites

    with st.container(border=True):
        title_col, star_col = st.columns([5, 1])

        with title_col:
            st.markdown(f"### {name}")
            st.caption(f"{course['분야']} · {course['유형']}")

        with star_col:
            star_label = "⭐" if is_fav else "☆"
            if st.button(
                star_label,
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
            set_detail(name)
            st.rerun()

# =========================================================
# 7. 사이드바: 기존 위치 유지, 직사각형 메뉴
# =========================================================
with st.sidebar:
    st.markdown("# 🌿 과목 선택 나침반")
    st.caption("나에게 맞는 배움의 방향을 찾아봐요.")
    st.markdown("---")

    pages = [
        "🏡 홈",
        "📚 분야별 과목",
        "🔎 과목 검색",
        "⭐ 나의 관심 과목",
        "💬 수강 후기",
        "🧭 과목 선택 가이드",
    ]

    current_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0
    selected_page = st.radio(
        "페이지 이동",
        pages,
        index=current_index,
        key="main_navigation",
        label_visibility="collapsed",
    )

    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        close_detail()
        st.rerun()

    st.markdown("---")
    st.markdown("### 🔗 공식 자료")
    st.markdown("[고교학점제 과목 안내](https://www.hscredit.kr/curriculum/subjects)")
    st.markdown("[국가교육과정정보센터](https://www.ncic.re.kr/)")
    st.caption("실제 개설 과목은 학교별로 다를 수 있어요.")

# =========================================================
# 8. 홈
# =========================================================
if st.session_state.page == "🏡 홈":
    hero(
        "내 과목 선택, 천천히 시작해요!",
        "2022 개정 교육과정과 고교학점제를 위한 나만의 과목 탐색 공간",
        "🍀",
    )

    st.write("""
    과목 선택이 어렵게 느껴진다면 여기서 하나씩 살펴봐요.
    과목의 특징과 학습 목표를 알아보고, 나의 관심 분야와 연결해 보세요.
    """)

    a, b, c = st.columns(3)
    a.metric("탐색 분야", f"{len(RAW)}개")
    b.metric("안내 과목", f"{len(COURSES)}개")
    c.metric("내 관심 과목", f"{len(st.session_state.favorites)}개")

    st.markdown("## 🌼 과목 탐색 시작하기")
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 📚 분야별 과목")
            st.write("국어부터 과학, 정보, 예술까지 분야별로 탐색해요.")
            if st.button("분야별 과목 보기", use_container_width=True):
                st.session_state.page = "📚 분야별 과목"
                close_detail()
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 🔎 과목 검색")
            st.write("과목 이름이나 진로 키워드로 정보를 찾아봐요.")
            if st.button("과목 검색하기", use_container_width=True):
                st.session_state.page = "🔎 과목 검색"
                close_detail()
                st.rerun()

    st.markdown("## 🌿 과목을 선택할 때 생각해 볼 네 가지")
    for title, desc in [
        ("흥미와 적성", "내가 궁금하고 배우고 싶은 내용인지 생각해요."),
        ("진로와의 연결", "희망 진로나 관심 분야에 필요한 배움인지 살펴봐요."),
        ("과목의 순서", "선수 과목이 있는지, 기초부터 배워야 하는지 확인해요."),
        ("학교의 개설 여부", "학교 교육과정, 시간표, 평가 방법을 확인해요."),
    ]:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(desc)

    st.markdown("## 📌 고교학점제 알아보기")
    st.write("""
    고등학교에서 자신의 진로와 적성에 따라 과목을 선택하고 이수하는 교육과정이에요.
    과목을 선택할 때는 흥미뿐 아니라 선수 과목, 학교의 개설 여부와 학업 계획도
    함께 확인하는 것이 좋아요.
    """)
    st.markdown("[고교학점제 공식 안내](https://www.hscredit.kr/curriculum/intro)")

# =========================================================
# 9. 분야별 과목: 목록 왼쪽 / 상세 정보 오른쪽
# =========================================================
elif st.session_state.page == "📚 분야별 과목":
    hero("분야별 과목 탐색", "관심 분야를 선택하고 과목의 별과 상세 정보를 확인해요.", "📚")

    category = st.selectbox("과목 분야", list(RAW.keys()), key="category_select")
    st.info(CATEGORY_INFO[category])

    kind_filter = st.selectbox(
        "과목 유형",
        ["전체", "공통", "일반 선택", "진로 선택", "융합 선택"],
        key="category_kind",
    )

    filtered = [c for c in COURSES if c["분야"] == category]
    if kind_filter != "전체":
        filtered = [c for c in filtered if c["유형"] == kind_filter]

    st.caption("⭐ 색칠된 별은 관심 과목이에요. 별을 다시 누르면 관심 목록에서 제외돼요.")
    st.markdown(f"### {category} 과목 {len(filtered)}개")

    if st.session_state.detail_open:
        left, right = st.columns([1.05, 0.95], gap="large")
        with left:
            for course in filtered:
                render_course_card(course, "cat")
        with right:
            show_detail_panel(get_course(st.session_state.selected_course))
    else:
        for course in filtered:
            render_course_card(course, "cat")

# =========================================================
# 10. 과목 검색: 검색 결과 왼쪽 / 상세 정보 오른쪽
# =========================================================
elif st.session_state.page == "🔎 과목 검색":
    hero("궁금한 과목을 찾아봐요", "과목 이름, 분야, 학습 목표, 진로 키워드로 검색해요.", "🔎")

    query = st.text_input(
        "검색어",
        placeholder="예: 미적분, 인공지능, 생명과학, 심리",
        key="course_query",
    )
    kind_filter = st.selectbox(
        "과목 유형",
        ["전체", "공통", "일반 선택", "진로 선택", "융합 선택"],
        key="search_kind",
    )

    results = []
    for course in COURSES:
        text = " ".join([
            course["과목"], course["분야"], course["유형"],
            course["소개"], course["학습목표"], course["진로"],
        ])
        if query.strip().lower() not in text.lower():
            continue
        if kind_filter != "전체" and course["유형"] != kind_filter:
            continue
        results.append(course)

    st.write(f"검색 결과: **{len(results)}개**")

    if st.session_state.detail_open:
        left, right = st.columns([1.05, 0.95], gap="large")
        with left:
            for course in results:
                render_course_card(course, "search")
        with right:
            show_detail_panel(get_course(st.session_state.selected_course))
    else:
        for course in results:
            render_course_card(course, "search")

# =========================================================
# 11. 관심 과목
# =========================================================
elif st.session_state.page == "⭐ 나의 관심 과목":
    hero("나의 관심 과목", "관심 과목을 모아 살펴보고 별을 눌러 관리해요.", "⭐")

    favorites = [
        get_course(name) for name in st.session_state.favorites
        if get_course(name)
    ]

    if not favorites:
        st.info("아직 관심 과목이 없어요. 분야별 과목에서 ☆를 눌러 추가해 보세요.")
    else:
        st.caption(f"저장한 과목 {len(favorites)}개")
        if st.session_state.detail_open:
            left, right = st.columns([1.05, 0.95], gap="large")
            with left:
                for course in favorites:
                    render_course_card(course, "fav")
            with right:
                show_detail_panel(get_course(st.session_state.selected_course))
        else:
            for course in favorites:
                render_course_card(course, "fav")

# =========================================================
# 12. 수강 후기: 과목별 조회 및 등록
# =========================================================
elif st.session_state.page == "💬 수강 후기":
    hero("선배들의 수강 후기", "수업 경험과 공부 방법을 나누어요.", "💬")

    st.warning(
        "현재 버전의 후기는 서버 데이터베이스에 저장되지 않아요. "
        "세션이 끝나면 사라질 수 있어요. 모든 사용자에게 영구 공유하려면 "
        "Supabase 등의 데이터베이스 연결이 필요해요."
    )

    review_course = st.selectbox(
        "어떤 과목의 후기를 볼까요?",
        ["전체 과목"] + COURSE_NAMES,
        key="review_filter",
    )

    if review_course == "전체 과목":
        reviews = list(st.session_state.reviews)
    else:
        reviews = get_reviews(review_course)

    if reviews:
        st.caption(f"후기 {len(reviews)}개")
        for review in reversed(reviews):
            with st.container(border=True):
                st.markdown(f"### {review['course']}")
                st.markdown(
                    f"<span class='pill'>{html.escape(review['difficulty'])}</span>",
                    unsafe_allow_html=True,
                )
                st.write(f"**{review['nickname']}**")
                st.write(review["content"])
                st.caption(review["date"])
                if st.button(
                    "이 과목 상세 보기",
                    key="review_detail_" + str(st.session_state.reviews.index(review)),
                ):
                    set_detail(review["course"])
                    st.session_state.page = "💬 수강 후기"
                    st.rerun()
    else:
        st.info("아직 등록된 후기가 없어요.")

    st.markdown("---")
    st.markdown("## ✍️ 후기 작성하기")
    st.write("실제 수강 경험을 바탕으로 후배에게 도움이 되는 조언을 남겨 주세요.")

    with st.form("general_review_form", clear_on_submit=True):
        course_name = st.selectbox("과목 선택", COURSE_NAMES, key="general_review_course")
        nickname = st.text_input("별명 (실명 사용 금지)", max_chars=20)
        difficulty = st.select_slider(
            "체감 난이도",
            options=["쉬웠어요", "조금 쉬웠어요", "보통이에요",
                     "조금 어려웠어요", "어려웠어요"],
            value="보통이에요",
        )
        content = st.text_area(
            "후기와 조언",
            placeholder="배운 내용, 어려웠던 점, 공부 방법 등을 적어 주세요.",
            max_chars=1000,
            height=140,
        )
        submitted = st.form_submit_button("후기 등록하기", type="primary")

        if submitted:
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
        show_detail_panel(get_course(st.session_state.selected_course))

# =========================================================
# 13. 과목 선택 가이드
# =========================================================
elif st.session_state.page == "🧭 과목 선택 가이드":
    hero("나에게 맞는 과목 선택 가이드", "관심 분야에서 과목 탐색을 시작해 보세요.", "🧭")

    interests = st.multiselect(
        "관심 분야를 선택하세요.",
        [
            "인문·언어", "수학·데이터", "자연과학", "의료·보건",
            "공학·컴퓨터", "사회·정치", "경제·경영", "교육·심리",
            "예술·디자인", "체육·스포츠", "환경·생태", "국제·외국어",
        ],
    )

    priority = st.radio(
        "과목을 선택할 때 가장 중요하게 생각하는 기준은 무엇인가요?",
        ["흥미와 적성", "희망 진로와의 연결", "기초부터 차근차근 배우기", "새로운 분야 탐색"],
    )

    mapping = {
        "인문·언어": ["문학", "독서와 작문", "세계사", "한문"],
        "수학·데이터": ["대수", "미적분Ⅰ", "확률과 통계", "실용 통계", "데이터 과학"],
        "자연과학": ["물리학", "화학", "생명과학", "지구과학", "융합과학 탐구"],
        "의료·보건": ["생명과학", "화학", "보건", "운동과 건강"],
        "공학·컴퓨터": ["물리학", "대수", "정보", "인공지능 기초", "로봇과 공학세계"],
        "사회·정치": ["정치", "법과 사회", "사회와 문화", "사회문제 탐구"],
        "경제·경영": ["경제", "경제 수학", "확률과 통계", "금융과 경제생활"],
        "교육·심리": ["교육의 이해", "인간과 심리", "문학", "진로와 직업"],
        "예술·디자인": ["미술", "미술 창작", "미술과 매체", "음악과 미디어"],
        "체육·스포츠": ["체육1", "운동과 건강", "스포츠 문화", "스포츠 생활1"],
        "환경·생태": ["생태와 환경", "기후변화와 환경생태", "지구과학"],
        "국제·외국어": ["영어 발표와 토론", "세계시민과 지리", "일본어", "중국어"],
    }

    if st.button("관심 분야 과목 찾아보기", type="primary"):
        recommended = list(dict.fromkeys(
            name for interest in interests for name in mapping.get(interest, [])
        ))
        st.session_state.guide_results = recommended
        st.session_state.guide_priority = priority

    if "guide_results" in st.session_state:
        recommended = st.session_state.guide_results
        st.markdown(f"## 🌱 탐색해 볼 과목 {len(recommended)}개")
        st.caption("선택 기준: " + st.session_state.get("guide_priority", "흥미와 적성"))

        if not recommended:
            st.info("관심 분야를 선택한 뒤 버튼을 눌러 주세요.")
        else:
            if st.session_state.detail_open:
                left, right = st.columns([1.05, 0.95], gap="large")
                with left:
                    for name in recommended:
                        course = get_course(name)
                        if course:
                            render_course_card(course, "guide")
                with right:
                    show_detail_panel(get_course(st.session_state.selected_course))
            else:
                for name in recommended:
                    course = get_course(name)
                    if course:
                        render_course_card(course, "guide")

    st.markdown("---")
    st.markdown("## 📌 꼭 확인해요")
    st.write("""
    - 추천 과목은 탐색을 위한 참고 자료이며 진로를 확정하는 결과가 아니에요.
    - 대학의 권장 과목과 전형 안내는 대학 및 모집 연도에 따라 달라질 수 있어요.
    - 공식 성취기준 원문은 국가교육과정정보센터에서 확인해 주세요.
    - 실제 학교 개설 여부와 이수 순서는 학교 선생님과 상담해 주세요.
    """)
    st.markdown("[고교학점제 공식 과목 안내](https://www.hscredit.kr/curriculum/subjects)")

# =========================================================
# 14. 하단
# =========================================================
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#71806b;font-size:.9rem'>"
    "🌿 과목 선택 나침반 · 나에게 맞는 배움을 찾아가는 여정"
    "</div>",
    unsafe_allow_html=True,
)
