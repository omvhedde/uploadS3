from flask import Flask, request, render_template, redirect, url_for
import boto3
import os

app = Flask(__name__)

# S3 Configuration
BUCKET_NAME = 'sampleapp2024'  # Replace with your bucket name
s3_client = boto3.client('s3')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename:
            # Upload file to S3
            s3_client.upload_fileobj(file, BUCKET_NAME, file.filename)
            return f"File uploaded successfully to S3: {file.filename}"
    return render_template('upload.html')

@app.route('/results/<filename>')
def results(filename):
    # Generate a presigned URL for downloading the file from S3
    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': filename},
        ExpiresIn=3600  # URL expiration in seconds
    )
    return render_template('results.html', filename=filename, url=presigned_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    