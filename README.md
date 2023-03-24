# PDF-TEXT-BASED-QA(https://mohammed-maaz-ahmed-pdf-text-based-qa-app-je9uqj.streamlit.app/)
This is a PDF and text-based question-answering system implemented using the Streamlit framework. The code allows users to upload a PDF file or enter text, then ask a question related to the content in the uploaded PDF file or entered text. 

model is fine tuned on squad dataset considering only 5000 examples and dividing them as 80 percent and 20 percent and freezing the base layer and saving the files of model and tokenizer in the local system and using them in the stramlit to deploy 

i have share code file of model fine tuning and deployment and the because of a single reson that i cant upload model to github im directly calling the model from hugging face i have commented the original code for refrence

TO RUN THIS DEPLOYMENT FILE : save the file in .py fomat and run in cmd go to path where you have saved the file and type python app.py you will then have to type streamlit run app.py and it will direct your browswer to the webpage 


happy coding!!
