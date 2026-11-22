import json
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AI 솔로몬 판사",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    html, body, .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: #10151f !important;
        color: #f2f4f8 !important;
    }
    .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 860px; }
    .hero {
        background: #161e2e !important; color: #f2f4f8 !important;
        border: 1px solid #2a354a; border-radius: 18px;
        padding: 28px 28px 22px 28px; margin-bottom: 18px;
    }
    .hero h1 { font-size: 2rem; margin: 0 0 8px 0; color: #f7f8fb !important; }
    .hero p { margin: 0; color: #d5dbe6 !important; }
    .badge-row { margin-top: 14px; display: flex; gap: 8px; flex-wrap: wrap; }
    .badge {
        background: rgba(212, 180, 131, 0.12); border: 1px solid rgba(212, 180, 131, 0.28);
        color: #e6d3b0 !important; border-radius: 999px; padding: 4px 10px; font-size: 0.82rem;
    }
    .card, .result-head {
        background: #171e2c !important; border: 1px solid #2a354a; border-radius: 16px;
        padding: 18px 18px 8px 18px; margin-bottom: 14px; color: #f2f4f8 !important;
    }
    .step { color: #d4b483 !important; font-size: 0.78rem; font-weight: 700; margin-bottom: 2px; }
    h1, h2, h3, p, span, label, li, .stMarkdown, [data-testid="stWidgetLabel"] {
        color: #f2f4f8 !important;
    }
    textarea, input, [data-baseweb="select"] > div {
        background: #121826 !important;
        color: #f2f4f8 !important;
        border-color: #3a465c !important;
        -webkit-text-fill-color: #f2f4f8 !important;
    }
    textarea::placeholder, input::placeholder { color: #9aa6ba !important; }
    [data-testid="stFileUploader"] section {
        background: #121826 !important;
        border-color: #3a465c !important;
        color: #f2f4f8 !important;
    }
    [data-testid="stFileUploader"] section * { color: #f2f4f8 !important; }
    button[kind="primary"] {
        background: #d4b483 !important;
        color: #10151f !important;
        border: none !important;
    }
    button[kind="primary"] * { color: #10151f !important; }
    .split { display: flex; height: 14px; border-radius: 999px; overflow: hidden; background: #2a3344; margin: 8px 0 6px 0; }
    .split-a { background: #8eb4e8; }
    .split-b { background: #d4b483; }
    .note { color: #c5cedd !important; font-size: 0.86rem; }
    div[data-testid="stMetric"] {
        background: #121826 !important; border: 1px solid #2a354a;
        border-radius: 14px; padding: 10px 12px;
    }
    pre, code, .stCode {
        background: #121826 !important;
        color: #f2f4f8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>⚖️ AI 솔로몬 판사</h1>
        <p>캡처와 설명을 보고, 책임 비중과 대응 문안을 참고용으로 정리합니다.</p>
        <div class="badge-row">
            <span class="badge">참고용 의견</span>
            <span class="badge">법률 자문 아님</span>
            <span class="badge">사진에 있는 내용만 판단</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return ""

def parse_json(raw):
    raw = (raw or "").strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start >= 0 and end > start:
        raw = raw[start:end + 1]
    return json.loads(raw)

def candidate_models(client):
    available = []
    for model in client.models.list():
        name = getattr(model, "name", "").replace("models/", "")
        if name:
            available.append(name)
    preferred = [
        "gemini-3.8-flash",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-flash-latest",
    ]
    ordered = [name for name in preferred if name in available]
    for name in available:
        if "flash" in name and "embed" not in name and name not in ordered:
            ordered.append(name)
    return ordered

def generate_result(client, contents):
    last_error = None
    models = candidate_models(client)
    if not models:
        raise RuntimeError("이 키로 쓸 수 있는 분석 모델을 찾지 못했습니다.")
    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                    system_instruction="너는 분쟁 참고 의견 보조다. 법원이나 변호사가 아니다. JSON만 출력한다.",
                ),
            )
            return model_name, parse_json(getattr(response, "text", ""))
        except Exception as e:
            last_error = e
            message = str(e)
            if any(word in message for word in ("503", "429", "UNAVAILABLE", "high demand")):
                continue
            raise
    raise RuntimeError(f"지금 모델이 모두 붐빕니다. 1~2분 뒤 다시 눌러 주세요.\n{last_error}")

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
st.caption("주민번호, 계좌번호가 보이면 가리고 올리세요. 사진은 분석 API로 전송됩니다.")
if uploaded_files:
    st.caption(f"첨부 {len(uploaded_files)}개")
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
        api_key = get_api_key()
        if not api_key:
            st.error("API 키가 없습니다. .streamlit/secrets.toml 에 GEMINI_API_KEY를 넣으세요.")
        else:
            prompt = f"""
분쟁 유형: {dispute_type}
사용자 설명:
{situation.strip()}

위 설명과 첨부 이미지만 보고 참고 의견을 JSON으로만 답하세요.
키는 반드시 이것만 쓰세요.
other_fault, summary, legal_basis, polite_message, firm_message, evidence_note

규칙:
- other_fault는 상대방 책임 비중이며 0에서 100 사이 정수다.
- 사진에 없는 금액, 날짜, 대화를 만들지 마라.
- 근거가 약하면 other_fault를 50 근처로 두고 evidence_note에 부족하다고 써라.
- 법률 자문처럼 단정하지 마라. 법조문 번호는 확신이 있을 때만 써라.
- polite_message는 정중한 요청, firm_message는 합의가 안 될 때의 단호한 요청이다.
- 협박, 허위 사실, 증거 조작은 넣지 마라.
"""
            contents = [prompt]
            for file in (uploaded_files or [])[:5]:
                mime = file.type if file.type in ("image/png", "image/jpeg") else "image/jpeg"
                contents.append(types.Part.from_bytes(data=file.getvalue(), mime_type=mime))

            try:
                with st.spinner("다른 모델을 찾아 분석하고 있습니다..."):
                    client = genai.Client(api_key=api_key)
                    model_name, data = generate_result(client, contents)
            except Exception as e:
                st.error("분석에 실패했습니다. 아래 글을 키 없이 복사해 주세요.")
                st.code(str(e))
                st.stop()

            digits = "".join(ch for ch in str(data.get("other_fault", "50")) if ch.isdigit())
            other = max(0, min(100, int(digits or "50")))
            own = 100 - other

            st.caption(f"사용 모델: {model_name}")
            st.markdown('<div class="result-head">', unsafe_allow_html=True)
            st.subheader("판독 결과")
            st.caption(f"{dispute_type} · 참고 의견")
            c1, c2 = st.columns(2)
            c1.metric("상대방 과실", f"{other}%")
            c2.metric("본인 과실", f"{own}%")
            st.markdown(
                f"""
                <div class="split">
                    <div class="split-a" style="width:{other}%"></div>
                    <div class="split-b" style="width:{own}%"></div>
                </div>
                <div class="note">남색이 상대방, 금색이 본인 비중입니다. 추정값이며 판결이 아닙니다.</div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.subheader("요약")
            st.write(data.get("summary", "요약을 만들지 못했습니다."))
            if data.get("evidence_note"):
                st.caption(data["evidence_note"])

            st.subheader("관련 근거")
            st.info(data.get("legal_basis", "확인된 근거가 없습니다."))

            st.subheader("추천 대응 메시지")
            tab1, tab2 = st.tabs(["정중한 협상형", "법적 조치 예고형"])
            with tab1:
                st.code(data.get("polite_message", ""), language=None)
            with tab2:
                st.code(data.get("firm_message", ""), language=None)

            st.warning("이 결과는 생성형 참고 의견입니다. 중요한 문제는 전문가와 상담하세요.")

st.caption("AI 솔로몬 판사 · 본 서비스는 법률 자문을 대체하지 않습니다.")
