import anthropic
import streamlit as st
from pyresparser import ResumeParser
from docx import Document
import pandas as pd
import PyPDF2

st.title('Generate an email!')

api_key = st.sidebar.text_input('Anthropic API key', type='password')

def bio_submitted(bio, calendar):
    st.session_state.bio_submitted = True
    st.session_state.bio = bio
    st.session_state.calendar_link = calendar
def generate_response(input_text):
    client = anthropic.Anthropic(api_key= api_key) 
    message = client.messages.create(model="claude-3-opus-20240229", max_tokens=750, temperature=0.0, system = "Have a professional tone (for a business fraternity).", messages=[{"role":"user", "content": input_text}])
    st.info(message.content[0].text)

default_values = {'bio': '', 'calendar_link': '', 'bio_submitted': False,}

for key, value in default_values.items():
    st.session_state.setdefault(key, value)

if not st.session_state.bio_submitted:
    with st.form('first_page'): #binds multiple elements together, vals are sent in a batch
        bio = st.text_area('Enter a bio of yourself that will be added to the beginning of the email.')
        calendar = st.text_area('Enter your Calendly link')
        st.form_submit_button('Submit', on_click = bio_submitted, args = (bio, calendar))      
           
else:           
#with st.form('my_form', border = True): #binds multiple elements together, vals are sent in a batch
    interests = st.text_area('What are you interested in learning more about?')
    uploaded_file = st.file_uploader("Upload resume") 
    #submitted = st.form_submit_button('Submit') #required with st.form()
    
    submitted = st.button('Submit')

    if 'sk' not in api_key:
        st.warning('Key is not correct!')
    if submitted and 'sk' in api_key:
        if not uploaded_file:
            st.warning('You have not uploaded a resume!')
        else:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            content = ''
            for page in range(len(pdf_reader.pages)):
                content+=pdf_reader.pages[page].extract_text()
            #st.write(content)
        
            text = "Here is a bio of myself that is to be included in the beginning of the email you generate: " + st.session_state.bio + "] \n These are things I found interesting in the provided resume: [" + interests + "] \n Here is the resume: [" + content + "] \n. Now, generate a short email that details three things I would like to learn about from this resume (do not make it a bulleted list) in a coffee chat I would like to schedule this week or next using this provided link: " + st.session_state.calendar_link
            generate_response(text)

            again = st.button('Generate another email')

