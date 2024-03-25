import streamlit as st
from pptx import Presentation
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OllamaEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama

llm = Ollama(
    model="zephyr",  # Specify the language model to use
    verbose=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)


def extract_text_from_pptx(file):
    prs = Presentation(file)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return '\n'.join(text)


def main():
    st.title("PowerPoint Text Extractor")

    uploaded_file = st.file_uploader("Upload a PowerPoint file", type=["pptx"])

    if uploaded_file is not None:
        text = extract_text_from_pptx(uploaded_file)
        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="zephyr")
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # show user input
        user_question = st.text_input("Ask a question about your document:")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            chain = load_qa_chain(llm, chain_type="stuff")

            response = chain.run(input_documents=docs, question=user_question)

            st.write(response)


if __name__ == "__main__":
    main()
