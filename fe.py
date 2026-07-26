# pip install streamlit 

# python -m pip install streamlit 
# pip install requests
# python -m pip install requests

import streamlit as st
import requests 

be_server_loc="http://127.0.0.1:8000"

# http://localhost:8501/
# http://localhost:8000 r http://127.0.0.1:8000 
# pip install uvicorn fastapi
# python -m pip install uvicorn fastapi

st.title("AI RESUME ANALYZER")
resume__=st.file_uploader("uploadPdfResume",type=["pdf"])

btn=st.button("analyzeResume")

if btn:
    r=requests.post(f"{be_server_loc}/resume_analyzing",files={"resume":resume__})
    # st.write(r)
    if r.status_code == 200:
        st.write(r.json()["msg"]["content"])
    #json :-- dict
    #files :-- file realted files
    #params :-- key:value
    #post() http req method who carries data from fe to be
# routes / end-point

# http://127.0.0.1:8000/resume_analyzing
# http://127.0.0.1:8000/register
# http://127.0.0.1:8000/profile_creation
# http://127.0.0.1:8000/profile_deletion
# http://127.0.0.1:8000/profile_updation

# python filename.py
# st.info()
# st.warning()
# st.success()
# st.danger()
# st.subheader()
# st.file_uploader()
