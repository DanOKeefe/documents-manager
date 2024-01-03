import os
import uuid
import boto3
import streamlit as st
import datetime
from pymongo import MongoClient
from pdfminer.high_level import extract_text
from transformers import pipeline, AutoTokenizer
from dotenv import load_dotenv

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def write_to_s3(bucket_name, file_name, object_name):
    s3_client = boto3.client('s3')
    s3_client.upload_file(file_name, bucket_name, object_name)
    s3_url = f'https://{bucket_name}.s3.amazonaws.com/{object_name}'
    return s3_url

def write_to_documents_table(file_name, s3_url, summaries):
    """
    Write metadata about a document to a documents collection in DynamoDB
    Include the filename, the s3_url, and summaries.
    Use DynamoDB Python client
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('documents')
    # generate a random UUID for the document_id
    document_id = str(uuid.uuid4())
    table.put_item(
        Item={
            'filename': file_name,
            's3_url': s3_url,
            'summaries': summaries,
            'document_id': document_id
        }
    )
    return True

def generate_summary(text):
    tokenizer = AutoTokenizer.from_pretrained(os.getenv('HF_MODEL'), use_fast=False)
    all_tokens = tokenizer.tokenize(text)
    max_seq_len = 256
    chunks = []
    chunk = []
    for token in all_tokens:
        if len(chunk) + len(token) < max_seq_len -3:
            chunk.append(token)
        else:
            chunks.append(chunk)
            chunk = [token]

    print(f'Number of chunks: {len(chunks)}')

    summarizer = pipeline('summarization', model=os.getenv('HF_MODEL'))

    summaries = []
    for chunk in chunks:
        chunk_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(chunk))
        summary = summarizer(chunk_text, min_length=25)[0]['summary_text']
        summaries.append(summary)
        print(summary)
        st.write(summary)

    return summaries

load_dotenv()

# Button to upload a document
uploaded_file = st.file_uploader('Upload a PDF file', type=['pdf'])

if uploaded_file is not None:
    file_name = uploaded_file.name

    # put file in tmp folder
    # create tmp folder if it doesnt exist
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # write pdf temp folder
    file_path = f'tmp/{file_name}'
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text_from_pdf(file_path)

    # Upload the file to S3
    bucket_name = os.getenv('S3_BUCKET_NAME')
    s3_url = write_to_s3(bucket_name, file_path, file_name)

    # Delete the file from tmp
    os.remove(file_path)

    # Gererate a summary of the document
    summaries = generate_summary(text)

    # Write the metadata to DynamoDB
    write_to_documents_table(file_name, s3_url, summaries)
