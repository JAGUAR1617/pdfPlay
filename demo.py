import streamlit as st
import PyPDF2
import os
import time

from PyPDF2 import PdfFileReader, PdfFileWriter
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from PyPDF2 import PdfFileMerger, PdfFileReader
from PIL import Image

st.set_page_config(layout="wide")

st.markdown("""

<style>
p1 {
    back
  animation-duration: 3s;
  animation-name: slide;
}

@keyframes slide {
  from {
    margin-left: 100%;
    width: 100%;
  }

  to {
    margin-left: 0%;
    width: 100%;
  }
}
.big-font {
    border-radius: 15px 35px;
    font-size:70px !important;
    font: italic small-caps bold 16px/2 cursive;
    line-height: 1.4;
    font-weight: bolder;
    font-stretch: normal;
    font-family: emoji;
    text-align: center;
    background-image: linear-gradient(orange, lime, yellow);

    

}
</style>
<p1 class="big-font" style="background-color:crimson;"> Welcome to pdfPlay📑</p1>


""", unsafe_allow_html=True)



def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://cdn.pixabay.com/photo/2019/09/05/06/49/garden-4453249_1280.png");
             
             background-size: cover;
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()


def intro():
    st.sidebar.success("Select options above.")
    st.markdown(
        """
    <style>
    p2 {

    }
    
    .normal-font {
        border-radius: 20px;
        font-size:20px;
        font-weight: bold;
        font-family:Verdana, sans-serif;
        
        

    }
    </style>
    <h2 class="normal-font" style="background-color:Darksalmon; text-align: center;">  ⏎ Choose from left dropdown menu </h2>

    <p class="normal-font"> 🅐 Convert pdf to text </p>
    <p class="normal-font"> 🅑 split pdf </p>
    <p class="normal-font"> 🅒 Merge all your pdf </p>




    """, unsafe_allow_html=True)

def mergePdf():
    st.markdown(f'# {list(page_names_to_funcs.keys())[4]}')
    st.write("""upload all pdf and merge it """)
    # uploaded_files={}

    
    uploaded_files = st.file_uploader("Choose a pdf file", accept_multiple_files=True, type=['pdf'])
    if uploaded_files is not None:
        with st.spinner('Wait for it...'):
            time.sleep(2)
            st.success('Completed!')
        # Call the PdfFileMerger
        mergedObject = PdfFileMerger()
 
# I had 116 files in the folder that had to be merged into a single document
# Loop through all of them and append their pages
        for fileNumber in uploaded_files:
            mergedObject.append(PdfFileReader(fileNumber))
 
# Write all the files into a file which is named as shown below
        mergedObject.write("mergedfilesoutput.pdf")

    with open(os.path.join("mergedfilesoutput.pdf"), "rb") as f:
        PDFbyte = f.read()
                
        st.download_button(label="download merged pdf's", 
            data=PDFbyte,
            file_name="merged.pdf",
            mime='application/octet-stream')    


    st.button("Re-run")

    
# closing the pdf file object 
def pdf2text():
    st.markdown(f'# {list(page_names_to_funcs.keys())[3]}')
    st.write(
        """
        upload pdf and convert into text 
"""
    )
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    if uploaded_file is not None:
        with st.spinner('Wait for it...'):
            time.sleep(2)
            st.success('Completed!')

        # pdfFileObj = open(uploaded_file, 'rb') 
        st.write("file uploaded")
    # creating a pdf reader object 
        pdfReader = PyPDF2.PdfFileReader(uploaded_file) 
    
# printing number of pages in pdf file 
        st.write(pdfReader.numPages) 
        # creating a page object 
        pageObj = pdfReader.getPage(0) 
    
# extracting text from page 
        txt = pageObj.extractText()
        st.download_button('Download the text', txt)
        st.write(txt)
    st.button("Re-run")


def pdfTominer():
    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        upload pdf and convert into text
"""
    )

    uploaded_miner = st.file_uploader('Choose your .pdf file', type="pdf")
    if uploaded_miner is not None:
        with st.spinner('Wait for it...'):
            time.sleep(2)
            st.success('Completed!')
        # pdfFileObj = open(uploaded_file, 'rb') 
        st.write("file uploaded")
        output_string = StringIO()
    
        parser = PDFParser(uploaded_miner)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

        st.write(output_string.getvalue())
        st.download_button('Download the text', output_string.getvalue())


# closing the pdf file object 
def pdf2split():
    st.markdown(f'# {list(page_names_to_funcs.keys())[2]}')
    st.write(
        """
        split all pages of your pdf
"""
    )


    
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    if uploaded_file is not None:
        with st.spinner('Wait for it...'):
            time.sleep(2)
            st.success('Completed!')
        # pdfFileObj = open(uploaded_file, 'rb') 
        st.write("file uploaded")
        inputpdf = PdfFileReader(uploaded_file)

        for i in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open("document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)
            
            with open(os.path.join("document-page%s.pdf" % i), "rb") as f:
                PDFbyte = f.read()
                
                st.download_button(label="dwonload_split_page"+str(i+1), 
                    data=PDFbyte,
                    file_name="split_pdf.pdf",
                    mime='application/octet-stream')    


    st.button("Re-run")


   

page_names_to_funcs = {
    "Home Page": intro,
    "pdf to full text" : pdfTominer,
    "Split pdf" : pdf2split,

    "pdf to Text" : pdf2text,
    "Merge pdf's" : mergePdf
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()



footer="""<style>
a:link , a:visited{
color: aqua;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: lime;
background-color: aquamarine;
text-decoration: underline;
}

.footer {
position: fixed;
left: 100px;
bottom: 0;
width: 100%;
background-color: cornflowerblue;
color: black;
text-align: center;


}



</style>
<div class="footer">
<p>Developed by <a class="normal-font" style="background-color:Darksalmon; text-align: center;"' href="https://www.linkedin.com/in/panchanand-jha-7767674b/" target="_blank" > Panchanand Jha</a></p>
<p> "Think hundred times before you take prints" </p>
</div>
"""
st.write(footer,unsafe_allow_html=True)


