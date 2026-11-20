import streamlit as st
import random
import time

st.set_page_config(
    page_title="AI 솔로몬 판사",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #10151f;
        color: #f2f4f8;
    }
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 860px;
    }
    .hero {
        background: #161e2e;
        color: #f2f4f8;
        border: 1px solid #2a354a;
        border-radius: 18px;
        padding: 28px 28px 22px 28px;
        margin-bottom: 18px;
    }
    .hero h1 {
        font-size: 2rem;
        margin: 0 0 8px 0;
        letter-spacing: -0.03em;
        color: #f7f8fb;
    }
    .hero p {
        margin: 0;
        color: #d5dbe6;
        font-size: 1.02rem;
    }
    .badge-row {
        margin-top: 14px;
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .badge {
        background: rgba(212, 180, 131, 0.12);
        border: 1px solid rgba(212, 180, 131, 0.28);
        color: #e6d3b0;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.82rem;
    }
    .card, .result-head {
        background: #171e2c;
        border: 1px solid #2a354a;
        border-radius: 16px;
        padding: 18px 18px 8px 18px;
        margin-bottom: 14px;
        color: #f2f4f8;
    }
    .step {
        color: #d4b483;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 2px;
    }
    .split {
        display: flex;
        height: 14px;
        border-radius: 999px;
        overflow: hidden;
        background: #2a3344;
        margin: 8px 0 6px 0;
    }
    .split-a { background: #8eb4e8; }
    .split-b { background: #d4b483; }
    .note {
        color: #c5cedd;
        font-size: 0.86rem;
    }
    div[data-testid="stMetric"] {
        background: #121826;
        border: 1px solid #2a354a;
        border-radius: 14px;
        padding: 10px 12px;
    }
    h1, h2, h3, p, label, .stMarkdown {
        color: #f2f4f8;
    }
    </style>
    """,
    unsafe_allow_html=True,)

st.markdown(
    """
    <div class="hero">
        <h1>⚖️ AI 솔로몬 판사</h1>
        <p>억울한 상황을 정리하고, 책임 비중과 대응 문안을 한 화면에서 확인합니다.</p>
        <div class="badge-row">
            <span class="badge">참고용 의견</span>
            <span class="badge">법률 자문 아님</span>
            <span class="badge">중고 · 알바 · 보증금</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="step">STEP 1</div>', unsafe_allow_html=True)
st.subheader("분쟁 유형")
dispute_type = st.selectbox(
    "어떤 종류의 분쟁인가요?",
    ["중고거래", "알바 임금", "보증금/전세", "기타"],
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="step">STEP 2</div>', unsafe_allow_html=True)
st.subheader("증거 자료")
uploaded_files = st.file_uploader(
    "대화 캡처나 증거 사진을 올려주세요",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
)
if uploaded_files:
    st.caption(f"첨부 {len(uploaded_files)}개 접수됨")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="step">STEP 3</div>', unsafe_allow_html=True)
st.subheader("상황 설명")
situation = st.text_area(
    "상황을 간단히 적어주세요",
    height=140,
    placeholder="언제, 누구와, 무슨 약속이 있었고, 지금 무엇이 문제인지 적어주세요.",
)
st.markdown("</div>", unsafe_allow_html=True)

clicked = st.button("판독 요청하기", type="primary", use_container_width=True)

if clicked:
    if not situation.strip():
        st.warning("상황 설명을 입력해주세요.")
    else:
        with st.spinner("자료를 정리하고 문안을 구성하고 있습니다..."):
            time.sleep(1.8)

        if dispute_type == "중고거래":
            seller_fault = random.randint(68, 88)
        elif dispute_type == "알바 임금":
            seller_fault = random.randint(75, 92)
        elif dispute_type == "보증금/전세":
            seller_fault = random.randint(60, 82)
        else:
            seller_fault = random.randint(55, 80)

        buyer_fault = 100 - seller_fault

        if dispute_type == "중고거래":
            summary = """
            입력하신 **중고거래** 분쟁을 정리한 결과입니다.
            상품 상태나 거래 조건에 대한 사전 고지가 부족했거나,
            약속된 상태와 다른 점이 있는 것으로 보입니다.
            매도인의 담보책임이 인정될 가능성이 있습니다.
            """
            legal = """
            - 민법 제580조 (매도인의 담보책임)
            - 전자상거래 등에서의 소비자보호에 관한 법률
            - 소비자분쟁해결기준 (공정거래위원회)
            """
            polite = f"""안녕하세요.
중고거래 건으로 연락드립니다.

{situation.strip()}

상품 상태에 대한 사전 설명이 부족했던 점 등을 고려할 때, 관련 법령상 판매자의 책임이 있을 수 있어 보입니다.
원만한 환불 또는 합의를 부탁드립니다."""
            firm = f"""안녕하세요.
본 중고거래 건에 대해 공식적으로 요청드립니다.

{situation.strip()}

민법상 매도인의 담보책임 및 전자상거래법 관련 조항에 근거하여 책임을 요구합니다.
기한 내 성실한 회신이 없을 경우 소액심판 또는 관련 기관 신고를 진행할 예정입니다."""

        elif dispute_type == "알바 임금":
            summary = """
            입력하신 **알바 임금** 관련 분쟁을 정리한 결과입니다.
            근로 제공에 대한 정당한 대가 지급이 이루어지지 않은 정황이 보입니다.
            근로기준법상 임금 체불에 해당할 여지가 있습니다.
            """
            legal = """
            - 근로기준법 제43조 (임금 지급)
            - 근로기준법 제36조 (금품 청산)
            - 고용노동부 임금체불 진정 제도
            """
            polite = f"""안녕하세요.
알바 급여 관련하여 말씀드립니다.

{situation.strip()}

제공한 근로에 대한 정당한 임금 지급이 이루어지지 않은 것으로 보여, 관련 법령에 따라 지급을 요청드립니다.
빠른 확인과 처리 부탁드립니다."""
            firm = f"""안녕하세요.
임금 체불 건으로 공식적으로 요청드립니다.

{situation.strip()}

근로기준법에 따라 체불 임금의 지급을 요구합니다.
기한 내 지급이 이루어지지 않을 경우 고용노동부 진정 및 법적 조치를 진행할 예정입니다."""

        elif dispute_type == "보증금/전세":
            summary = """
            입력하신 **보증금/전세** 관련 분쟁을 정리한 결과입니다.
            계약 종료 후 보증금 반환이 지연되거나 정당한 사유 없이 공제하려는 정황이 보입니다.
            주택임대차보호법상 보증금 반환 의무가 있습니다.
            """
            legal = """
            - 주택임대차보호법
            - 민법 제654조 (임차인의 보증금 반환 청구)
            - 주택임대차분쟁조정위원회
            """
            polite = f"""안녕하세요.
보증금 반환 건으로 연락드립니다.

{situation.strip()}

계약 종료에 따른 보증금 반환이 정상적으로 이루어지지 않은 것으로 보여, 관련 법령에 따라 반환을 요청드립니다.
원만한 해결을 위해 협의 부탁드립니다."""
            firm = f"""안녕하세요.
보증금 반환 요청 건입니다.

{situation.strip()}

주택임대차보호법 등에 근거하여 보증금 반환을 정식으로 요구합니다.
기한 내 반환이 이루어지지 않을 경우 내용증명 발송 및 분쟁조정 신청을 진행할 예정입니다."""

        else:
            summary = """
            입력하신 **기타** 분쟁을 종합적으로 정리한 결과입니다.
            제시된 상황과 자료를 바탕으로 볼 때, 상대방의 책임 비중이 더 높은 것으로 판단됩니다.
            구체적인 법적 근거는 사안에 따라 달라질 수 있습니다.
            """
            legal = """
            - 민법 일반 원칙 (불법행위, 채무불이행)
            - 관련 특별법 (사안에 따라 적용)
            - 소비자분쟁해결기준 또는 관련 조정 제도
            """
            polite = f"""안녕하세요.
해당 건으로 연락드립니다.

{situation.strip()}

관련 법령과 일반 원칙에 비추어 볼 때 상대방의 책임이 인정될 여지가 있어 보입니다.
원만한 해결을 위해 협의를 부탁드립니다."""
            firm = f"""안녕하세요.
본 건에 대해 공식적으로 요청드립니다.

{situation.strip()}

관련 법리에 근거하여 책임을 요구하며, 합의가 이루어지지 않을 경우 내용증명 발송 및 법적 조치를 검토할 예정입니다.
기한 내 회신 부탁드립니다."""

        st.markdown('<div class="result-head">', unsafe_allow_html=True)
        st.subheader("판독 결과")
        st.caption(f"{dispute_type} · 참고 의견")

        c1, c2 = st.columns(2)
        c1.metric("상대방 과실", f"{seller_fault}%")
        c2.metric("본인 과실", f"{buyer_fault}%")
        st.markdown(
            f"""
            <div class="split">
                <div class="split-a" style="width:{seller_fault}%"></div>
                <div class="split-b" style="width:{buyer_fault}%"></div>
            </div>
            <div class="note">남색이 상대방, 금색이 본인 비중입니다.</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("요약")
        st.write(summary)

        st.subheader("관련 근거")
        st.info(legal)

        st.subheader("추천 대응 메시지")
        tab1, tab2 = st.tabs(["정중한 협상형", "법적 조치 예고형"])
        with tab1:
            st.caption("먼저 보내 보기 좋은 톤입니다. 오른쪽 위 복사 버튼을 쓰세요.")
            st.code(polite, language=None)
        with tab2:
            st.caption("합의가 안 될 때 쓰는 더 단호한 톤입니다.")
            st.code(firm, language=None)

        st.warning("이 결과는 생성형 참고 의견입니다. 중요한 문제는 전문가와 상담하세요.")

st.caption("AI 솔로몬 판사 · 본 서비스는 법률 자문을 대체하지 않습니다.")