import streamlit as st

# Title
st.title('📄 Documents Manager 📚')

# Description
st.write("""
Welcome to the Documents Manager! 🎉

You can view existing documents and their summaries, or upload new documents. 

Uploaded documents will be stored in AWS S3 and their metadata will be stored in DynamoDB.
         
Summaries of the documents will also be stored in DynamoDB.
""")

# Instructions
st.write("""
🔍 To view documents, navigate to the `View_Documents` page.
         
📤 To upload a new document, navigate to the `Upload_Documents` page.
""")