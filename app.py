import streamlit as st
import google.generativeai as genai

# 1. Gemini API 설정 (보안을 위해 secrets 활용)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 페이지 설정 및 제목
st.set_page_config(page_title="킹왕짱 AI", page_icon="😎")
st.title("😎 킹왕짱 AI 챗봇")
st.info("반가워요! 저는 당신의 든든한 친구, 킹왕짱 AI예요. 무엇이든 물어보세요!")

# 3. 사이드바 - 대화 초기화 기능
with st.sidebar:
    st.header("설정")
    if st.button("대화 내용 지우기"):
        st.session_state.messages = []
        st.rerun()

# 4. 세션 상태 초기화 (대화 내역 저장)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 기존 대화 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 및 AI 답변 처리
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 표시 및 저장
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gemini 모델 설정 (gemini-1.5-flash)
    model = genai.GenerativeModel(model_name='models/gemini-2.5-flash')
    
    # 7. AI 답변 생성 루틴
    with st.chat_message("assistant", avatar="😎"):
        try:
            # 친근한 성격 부여를 위한 프롬프트 조합
            persona_prompt = f"너의 이름은 '킹왕짱 AI'야. 사용자에게 아주 친근하고 다정하게, 때로는 재치 있게 친구처럼 답변해줘. \n\n질문: {prompt}"
            
            response = model.generate_content(persona_prompt)
            full_response = response.text
            
            st.markdown(full_response)
            
            # AI 메시지 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"앗, 에러가 발생했어요! : {e}")