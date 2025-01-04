import os

from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


def ingest_txt_documents(text_path: str, db_path: str, openai_api_key: str):

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")

    txt_list = []
    doc_list = []

    for file_name in os.listdir(text_path):
        f = open(text_path + file_name, "r")
        answer = f.read()

        txt_list.append(Document(page_content=answer))

        text_splitter = CharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=50,
        )
        docs = text_splitter.split_documents(txt_list)

    for doc in docs:
        doc.metadata = {"source": file_name}
        doc_list.append(doc)

    vectorstore = Chroma.from_documents(
        documents=doc_list,
        embedding=embeddings,
        persist_directory=db_path,
    )

    vectorstore.persist()


def create_retrieval_chain(db_path: str, openai_api_key: str):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")

    vectorstore = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings,
    )

    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name="gpt-4o",
        temperature=0.0,
    )

    retrieval_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
    )

    return retrieval_chain
