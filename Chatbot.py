import streamlit as st
from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI

api_key = os.getenv("OPENAI_API_KEY")
clr

st.title("Notebot Ai")

with st.sidebar:
    st.title("MyNoteBot")
    file=st.file_uploader("upload the notes! and strat asking the questions!",type=["pdf"])

    if file is not None:
        # Extraction text from pdf file
        my_pdf=PdfReader(file)
        text=""
        for page in my_pdf.pages:
            text+=page.extract_text()

            # break it into Chunks
            splitter=RecursiveCharacterTextSplitter(chunk_size=250,chunk_overlap=50)
            chunks=splitter.split_text(text)

            #creating Object of OpenAiEmbeddings class that let us connect with OpenAi's Embeddings Model
            embeddings=OpenAIEmbeddings(api_key=Open_API_KEY)

            #Crating VectorDB And Storing embeddings into it
            vector_store=FAISS.from_texts(chunks,embeddings)
            # the Above line will do these things take all the chunks and generate embeddings with the help of given
            # embedding models and then store
            # into the searchable index that is FAISS in that database

            #get user Query
            usr_query = st.text_input("Ask your Question...")

            #Semantic Search or similarity  From Vector Search
            #semilarity search we need two things
            #1.User Query
            #2.Vector Store
            #user will ask the question then it will be converted into embeddings
            #and  then acc to that question from that vector store from that vector data base
            # Semantic Search or that Similarity search will be done and it will
            #retrive the most similar chunks
            if usr_query:
                matching_chunks=vector_store.similarity_search(usr_query)
                #this similarity search this meathod internally convert this usr query
                # into embeddings on those from the vecor store
                # it will fetch the most similar chunks in the form of embeddings

                #define our LLm First

                llm=ChatOpenAI(
                    api_key=Open_API_KEY,
                    max_tokens=300,
                    temperature=0,
                    model="gpt-3.5-turbo"
                )

                #chaining or generate Response
                chain=load_qa_chain(llm,chain_type="stuff")
                output=chain.run(question=usr_query,documents=matching_chunks)
                st.write(output)



