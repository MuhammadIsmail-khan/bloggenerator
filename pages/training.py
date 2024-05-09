import streamlit as st
from io import BytesIO
from PyPDF2 import PdfReader
from database import store_training_data,get_traning_data_from_database
import docx

def get_pdf_text(pdf):
    text=""
    # for pdf in pdf_docs:
    # print("File type ------------------------------- >>>>>>>>>>> : ",type(pdf))
    
    pdf_stream=BytesIO(pdf.read())
    # print("File type after byteio ------------------------  :",type(pdf_stream))
    pdf_reader=PdfReader(pdf_stream)
    for page in pdf_reader.pages:
        text+=page.extract_text()
        
    # print("Text from pdf ",text)
    return text

def get_docx_text(docx_file):
    text = ""
    docx_stream = BytesIO(docx_file.read())
    doc = docx.Document(docx_stream)
    for para in doc.paragraphs:
        text += para.text
    return text

def main():
    textToShow=""
    st.title("Blog Generator")

    # Create six select menus
    with st.form("select_form"):
        col1, col2=st.columns(2)
        
        with col1:
            option1 = st.selectbox("Option", ["AI", "I", "WE","You"])
        with col2:
            option2=st.file_uploader("upload here")
            if option2:
                if option2.type == "application/pdf":
                    text = get_pdf_text(option2)
                elif option2.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = get_docx_text(option2)
                
                selected_data = text
                
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            # print(f"Option : {option1} , selected data : ",selected_data)
            store_training_data(option1,selected_data)

    
    if submit_button:
        pass

    col3,col4,col5,col6=st.columns(4)
    with col3:
        AI_button=st.button("AI",use_container_width=True)
        # st.write(f"AI_button {AI_button}")
        if AI_button:
            textToShow=get_traning_data_from_database("AI")
        
    with col4:
        I_button=st.button("I",use_container_width=True)
        if I_button:
            textToShow=get_traning_data_from_database("I")
        
    with col5:
        We_button=st.button("We",use_container_width=True)
        if We_button:
            textToShow=get_traning_data_from_database("WE")
    with col6:
        You_button=st.button("You",use_container_width=True)
        if You_button:
            textToShow=get_traning_data_from_database("You")
    
    st.text_area(label="Sample Data",value=textToShow)

if __name__ == "__main__":
    main()
