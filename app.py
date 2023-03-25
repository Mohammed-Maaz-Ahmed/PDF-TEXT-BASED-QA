#necessary liblaries
import streamlit as st
import re
import pikepdf
import nltk
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import io
import pdfminer
import pdfminer.high_level
import pdfminer.layout
from pdfminer.high_level import extract_text_to_fp
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

# Set page config
st.set_page_config(
    page_title="PDF AND TEXT BASED Question Answering System",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# read file
def read_pdf(file):
    text = io.StringIO()
    extract_text_to_fp(file, text)
    return text.getvalue()

#preprocess pdf text
def preprocess_text(text):
    # Remove non-alphanumeric characters and extra whitespaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    # Lowercase the text
    text = text.lower()
    return text

#preprocess question 
def preprocess_question(question):
    # Remove special characters and punctuation
    question = re.sub(r"[^\w\s]", "", question)

    # Convert to lowercase
    question = question.lower()

    return question

def load_model():
    # Load my model
    model_path = "saved_model"
    tokenizer_path = "saved_tokenizer"
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, use_fast=True)
    model = AutoModelForQuestionAnswering.from_pretrained(model_path)
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    return qa_pipeline


qa_pipeline = load_model()


# Set logo and title
col1, col2 = st.columns([3, 29])

with col1:
    st.image("logo.jpg", width=200)

with col2:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>PDF AND TEXT BASED QA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: 10px;'>Welcome to our website! Please watch our video for more information about our PDF-based QA system.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Rest assured that any data or PDF files you upload will be kept confidential and not shared with any third parties.</p>", unsafe_allow_html=True)

# Display a video  introvideo.mp4
video_file = open('intovideo.mp4', 'rb')
video_bytes = video_file.read()

# Create  placeholder  video
video_placeholder = st.empty()

#  skip  video
if st.button("Skip Video"):
    # Clear the video placeholder
    video_placeholder.empty()
    # Set video file data to None
    video_bytes = None

if video_bytes is not None:
    # play video
    video_placeholder.video(video_bytes)

# choose between uploading a PDF file or enter text
if "option" not in st.session_state:
    st.session_state.option = "Upload a PDF file"
option = st.radio("Select an option:", ("Upload a PDF file", "Enter text"))

# Upload PDF 
if option == "Upload a PDF file":
    text = None
    with st.expander("Upload a PDF file", expanded=True):
        file = st.file_uploader("Choose a file", type="pdf")
        if file is not None:
            bytes_data = file.read()
            st.write("File upload complete.")

    # Display the PDF file
    if file is not None:
        st.sidebar.subheader("PDF File")
        st.sidebar.write(file.name)
        st.sidebar.write(file.size)
        st.sidebar.write(file.type)

        text = read_pdf(file)

        st.subheader("PDF Text")
        st.write(text)

# ask text
if option == "Enter text":
    file = None
    with st.expander("Input Text", expanded=True):
        text = st.text_area("Enter text here", height=300)
        if st.button("Submit"):
            if len(text) > 0:
                st.write(text)
            st.write("Text input complete.")  


# Ask question
question = st.text_input("Ask a question")
question_button = st.button("Generate Answer")

# Check if  user  provided input and clicked generate button
if question_button:
    # Display answer to the question with loading spinner
    if (option == "Upload a PDF file" and file is not None) or (option == "Enter text" and len(text) > 0) and len(question) > 0:
        with st.spinner("Generating answer..."):
            if option == "Upload a PDF file":
                text = read_pdf(file)
                text = preprocess_text(text)
            else:
                text = preprocess_text(text)
            question = preprocess_question(question)
            if len(question) > 0:
                result = qa_pipeline(question=question, context=text)
                answer = result["answer"]
                confidence = result["score"]
                if confidence < 0.01:
                    answer = "Sorry, the question is out of context."
                    confidence = 0
            else:
                answer = ""
                confidence = 0
        st.subheader("Answer")
        if len(answer) > 0:
            st.write(f"The answer is: {answer}")
    
    # Reset confidence score if option changed
    if st.session_state.option != option:
        st.session_state.option = option
        confidence = 0

st.write("*******Developed by Mohammed Maaz Ahmed, Data Scientist at SoothSayer Analytics*******")

