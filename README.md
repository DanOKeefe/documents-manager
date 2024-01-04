# 📄 Documents Manager 📚

This project is a document management app that allows users to view and upload PDF documents. It uses Streamlit for the web interface, AWS S3 for document storage, DynamoDB for metadata storage, and a transformer model for summarizing the documents.

## 🚀 Getting Started

### Steps

1. Clone the repository.

```sh
git clone https://github.com/DanOKeefe/documents-manager
```

2. Install the required Python packages using pip:

```sh
pip3 install -r requirements.txt
```

3. Set up your AWS credentials in the ```.env``` file. You will need to provide the following:

```sh
AWS_ACCESS_KEY_ID="your_access_key"
AWS_SECRET_ACCESS_KEY="your_secret_access_key"
AWS_DEFAULT_REGION="your_region"
```

4. Set the ```HF_MODEL``` environment variable in the .env file to the model you want to use for text summarization, for example:

```sh
HF_MODEL="Falconsai/text_summarization"
```

5. Set the ```S3_BUCKET``` environment variable in the ```.env``` file to the name of your S3 bucket:

```sh
S3_BUCKET="your_bucket_name"
```

### 📑 How to Use

Start the app using ```streamlit run Home.py```

### View Documents

Open the page 1_View_Documents to view the documents. You can select a document from the dropdown to view its summary.

### Upload Documents

Open 2_Upload_Documents to upload a document. You can upload a PDF file, which will be stored in S3 and its metadata will be stored in DynamoDB. The document will be summarized using a transformer model.

## 📚 Built With
 - [Streamlit](https://streamlit.io/)
 - [AWS S3](https://aws.amazon.com/s3/)
 - [AWS DynamoDB](https://aws.amazon.com/dynamodb/)
 - [Transformers](https://huggingface.co/)

