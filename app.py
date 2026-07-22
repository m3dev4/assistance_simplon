import streamlit as st

from ingestion import ask_question

st.set_page_config(
    page_title="Assistant Règlement Simplon",
    page_icon="🤖"
)

st.title("🤖 Assistant Règlement Simplon")

question = st.chat_input(
    "Pose ta question sur le règlement interieur de Simplon Sénégal..."
)

if question:
    with st.chat_message("user"):
        st.write(question)
    
    response = ask_question(question)

    with st.chat_message("assistant"):
        st.write(
            response["answer"]
        )
    
    st.divider()

    st.write("📚 Source utilisées")

    for doc in response["context"]:
        st.write(
            f"""
               - Article {doc.metadata.get('article')}
               - page {doc.metadata.get('page')}
            """
        )