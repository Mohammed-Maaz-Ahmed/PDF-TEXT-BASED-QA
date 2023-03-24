import streamlit as st
import re
import nltk
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import io
import pdfminer
import pdfminer.high_level
import pdfminer.layout
from pdfminer.high_level import extract_text_to_fp
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from PIL import Image


# Set the page config
st.set_page_config(
    page_title="PDF Question Answering System",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# read the file
def read_pdf(file):
    text = io.StringIO()
    extract_text_to_fp(file, text)
    return text.getvalue()

#preprocess the pdf text
def preprocess_text(text):
    # Remove non-alphanumeric characters and extra whitespaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    # Lowercase the text
    text = text.lower()
    return text

#preprocess the question 
def preprocess_question(question):
    # Remove special characters and punctuation
    question = re.sub(r"[^\w\s]", "", question)

    # Convert to lowercase
    question = question.lower()

    return question

def load_model():
    # Load the pre-trained model
    model_path = "saved_model"
    tokenizer_path = "saved_tokenizer"
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, use_fast=True)
    model = AutoModelForQuestionAnswering.from_pretrained(model_path)
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    return qa_pipeline


qa_pipeline = load_model()


# Set the logo and title
col1, col2 = st.columns([3, 29])

with col1:
    st.image("logo.jpg", width=200)

with col2:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>PDF BASED QA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: 10px;'>Welcome to our website! Please watch our video for more information about our PDF-based QA system.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Rest assured that any data or PDF files you upload will be kept confidential and not shared with any third parties.</p>", unsafe_allow_html=True)


# Display a video file named 'introvideo.mp4'
video_file = open('intovideo.mp4', 'rb')
video_bytes = video_file.read()

# Create a placeholder for the video
video_placeholder = st.empty()

# Option to skip the video
if st.button("Skip Video"):
    # Clear the video placeholder
    video_placeholder.empty()
    # Set the video file data to None
    video_bytes = None

if video_bytes is not None:
    # play the video
    video_placeholder.video(video_bytes)


st.sidebar.header("Settings")

# Upload a PDF file with a progress bar
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

# Ask a question
question = st.text_input("Ask a question")



# Display the answer to the question with a loading spinner
if file is not None and question != "":
    with st.spinner("Generating answer..."):
        text = read_pdf(io.BytesIO(bytes_data))
        text = preprocess_text(text)
        question = preprocess_question(question)
        result = qa_pipeline(question=question, context=text)
        answer = result["answer"]
    st.subheader("Answer")
    st.write(f"The answer is: {answer}")
