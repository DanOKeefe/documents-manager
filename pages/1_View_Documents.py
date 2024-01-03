import streamlit as st
import boto3
from dotenv import load_dotenv

load_dotenv()

# Retrieve documents from the documents table in DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('documents')
response = table.scan()
documents = response['Items']

# Make a list of the filenames of the documents
filenames = [document['filename'] for document in documents]

# Sort the filenames alphabetically
filenames.sort()

# Create a dropdown with the filenames
selected_filename = st.selectbox('Select a document:', filenames, index=None)

if selected_filename:
    # Retrieve the selected document from DynamoDB
    selected_document = table.get_item(Key={'filename': selected_filename})['Item']

    # Display the summary of the selected docuemnt
    for summary in selected_document['summaries']:
        st.write(summary)
        st.write('---')