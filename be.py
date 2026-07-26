from fastapi import FastAPI,File,UploadFile # importing FastAPI from fastapi
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq  import ChatGroq

fast_api_obj=FastAPI()


llm = ChatGroq(
    api_key="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",
    model="llama-3.3-70b-versatile"
)



@fast_api_obj.post("/resume_analyzing") #listens to fe request
async def resume_taker(resume :UploadFile= File(...) ): # params
    # need to create file and store all the data in the created file in be
    f_name=resume.filename
    with open(f_name,"wb") as f : # creating file with name -- f_name with mode of op w i.e creating file
        f.write(await resume.read() ) # add all data to file


    loader=PyPDFLoader(f_name) # loading yr file with loader    
    # print(resume.filename)

    docs=loader.load() # one pdf to multiple small pdfs /docs

    splitter=RecursiveCharacterTextSplitter( #splitter param obj
        chunk_size=500,
        chunk_overlap=100
    )

    chunks=splitter.split_documents(docs) ## one small doc into multiple chunks

    e_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_db=Chroma.from_documents(
        documents=chunks,
        embedding=e_model ,
        persist_directory="./chroma_db_folder"
    )
    r_docs=vector_db.similarity_search(
        query="analyze skills, strength, weaknesses, experience etc..",
        k=5
    )

    r_chunks="\n\n".join([i.page_content for i in r_docs])


    prompt=f"""
      You are an expert HR recruiter.

    Analyze the following resume and provide:

    1. Candidate Summary
    2. Technical Skills
    3. Projects
    4. Strengths
    5. Weaknesses
    6. Suggested Job Roles
    7. Resume Score out of 10

    resume :-- 

    {r_chunks}
    """

    response=llm.invoke(prompt)

    return {
        "msg":response
    }

# uvicorn
# streamlit
# fastapi 
# requests

# fe server start command :-- streamlit run fe.py
# be server start command :-- uvicorn be:fast_api_obj --reload
# install below libs 

# pip install langchain
# pip install langchain-core
# pip install langchain-community
# pip install langchain-text-splitters
# pip install sentence-transformers
# pip install pypdf
# pip install langchain-chroma
# pip install langchain-huggingface 
# pip install langchain-groq 

# HuggingFaceEmbeddings is a class ehich creates embedding_model and the embedding_model is used to convert chunks to vectors

# pip install python-multiplart
# resume_taker(1) #arg    

# uvicorn be:fast_api_obj --realod command to start the server

# python -m uvicorn be:fast_api_obj
