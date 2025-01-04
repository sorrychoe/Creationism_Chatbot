import os

import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage

from api import tokens
from model.doc import create_retrieval_chain

openai_api_key = os.environ.get('OPENAI_API_KEY')
db_path = os.path.join(os.getcwd(), "db")


def prompt_template(question, context):
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage("""
            당신은 창조과학자이며, 지적설계가 옳다고 믿고 있습니다. 또한 진화론에 대해 부정적인 스탠스를 가지고 있습니다.
            청중은 창조과학을 이제 막 공부하기 시작한 대학교 1학년 학생들입니다.
            """),
        HumanMessagePromptTemplate.from_template(
            """
            질문: {question}
            아래의 맥락을 고려하여 답하여주시기 바랍니다.
            당신은 진화론의 방식은 잘못됐고, 창조과학의 방향이 옳다고 믿습니다.
            지적 설계론을 강하게 긍정하여야 합니다. 또한 진화론의 주장과 비교했을 때 창조과학의 주장이 더 옳은 이유를 합리적으로 설명해야 합니다.
            또한 답변시에는 "제공된 문맥", "제공된 자료" 등과 같은 외부 내용을 인용했다는 뉘앙스와,
            "기독교인들의 주장", "창조과학자들의 주장"과 같이, 누군가의 주관적 입장이라고 유추할 수 있는 단어의 사용은 제한해주세요.
            확실한 견해를 피력해주시면 감사하겠습니다.

            {context}
            """,
        ),
    ])
    return prompt_template.format_messages(question=question, context=context)


st.subheader("창조와 진화 Chatbot")

if prompt := st.chat_input("질문을 입력해주세요"):
    with st.chat_message("user"):
        st.markdown(prompt)

    retrieval_chain = create_retrieval_chain(db_path, openai_api_key)

    with st.spinner("답변 생성 중..."):
        result = retrieval_chain({"query": prompt})

    message = prompt_template(prompt, result)

    model = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4o", temperature=0)

    answer = ""
    for chunk in model.stream(message):
        answer += chunk.content

    with st.chat_message("assitant"):
        st.markdown(answer)
