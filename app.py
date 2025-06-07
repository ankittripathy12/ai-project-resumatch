import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv



load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

## streamlit app
st.title("ResuFit")
st.text("Improve Your Resume ATS")
jd=st.text_area("Give the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

import json

if submit:
    if uploaded_file is not None and jd.strip() != "":
        text = input_pdf_text(uploaded_file)
        final_prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_repsonse(final_prompt)
        
        try:
            result = json.loads(response.replace("```json", "").replace("```", ""))
            st.subheader("📊 JD Match")
            st.markdown(f"**{result['JD Match']}**")

            st.subheader("❌ Missing Keywords")
            st.markdown(", ".join(result["MissingKeywords"]))

            st.subheader("📝 Profile Summary")
            st.markdown(result["Profile Summary"])
        except Exception as e:
            st.error("Failed to parse response. Please check the format.")
            st.text(response)
    else:
        st.warning("Please upload a resume and paste the job description.")

