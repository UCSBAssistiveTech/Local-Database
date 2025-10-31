# Local-Database
Backend Local Mockup - AWS S3 Simulation with LocalStack

## Overview

This project demonstrates how to simulate AWS S3 bucket functionality locally using LocalStack, allowing you to develop and test S3 operations without requiring an actual AWS account. The implementation uploads PDF files to a local S3 bucket and provides multiple ways to access the uploaded data.

## Prerequisites

- Docker
- Python 3.9+
- LocalStack CLI
- LocalStack Desktop (recommended for visual management)

## LocalStack Setup

### 1. Install LocalStack CLI
Follow the [LocalStack CLI installation guide](https://docs.localstack.cloud/getting-started/installation/) for your operating system.

### 2. Create LocalStack Account
- Create a free account at [LocalStack](https://app.localstack.cloud/)
- Access the Hobby Subscription for non-commercial use
- Retrieve your authentication token from the Auth Tokens page

### 3. Configure Environment Variables
```bash
export LOCALSTACK_AUTH_TOKEN="your-auth-token"
export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"
```

### 4. Start LocalStack
```bash
DEBUG=1 localstack start
```
Wait for the "Ready." message to confirm LocalStack is running.

## Project Structure

- `app.py` - Flask web server with file upload endpoints
- `base.py` - Core S3 upload functionality
- `file.pdf` - Sample PDF file to upload
- `requirements.txt` - Python dependencies
- `.env` - Environment configuration (untracked)

## How It Works

### Flask Server Architecture
The Flask server (`app.py`) provides a complete web interface and API for file uploads to LocalStack S3. It consists of:

- **Web Interface**: User-friendly HTML form for file uploads
- **REST API**: Programmatic endpoints for integration
- **S3 Integration**: Seamless connection to LocalStack S3 bucket
- **File Management**: Upload, list, and download capabilities
- **Error Handling**: Comprehensive error handling and logging

### S3 Bucket Simulation
The application creates a simulated S3 bucket named `my-new-bucket` in LocalStack with the following configuration:

- **Endpoint**: `http://localhost:4566` (LocalStack default)
- **Credentials**: Uses test credentials (`tester`/`test`)
- **Bucket Name**: `my-new-bucket`
- **File Path**: Files are uploaded to `images/` directory within the bucket

### File Upload Process
1. **File Reception**: Flask receives file via HTTP POST request
2. **Validation**: Validates file presence, size, and security
3. **Processing**: Reads file bytes and determines MIME type
4. **S3 Upload**: Uses boto3 to upload to LocalStack S3 endpoint
5. **Response**: Returns success/error status with file information
6. **Logging**: Provides detailed upload status and error handling

### Supported File Types
The server automatically detects MIME types for:
- **Documents**: PDF, DOC, DOCX, TXT, CSV, JSON, XML
- **Images**: JPG, JPEG, PNG, GIF
- **Archives**: ZIP
- **Generic**: Any file type (defaults to `application/octet-stream`)

## Usage

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Flask Server
```bash
python app.py
```

The server will start on `http://localhost:8080`

### Available Endpoints

#### Web Interface
- **GET** `/` - Upload page with web form
- **POST** `/upload-web` - Upload file via web form

#### API Endpoints
- **POST** `/upload` - Upload file via API (JSON response)
- **GET** `/files` - List all uploaded files
- **GET** `/download/<filename>` - Download a specific file
- **GET** `/health` - Health check endpoint

### Flask Server Features

#### Security Features
- **File Size Limits**: 16MB maximum file size per upload
- **Secure Filenames**: Uses `secure_filename()` to prevent path traversal
- **Input Validation**: Validates file presence and content
- **Error Handling**: Comprehensive error handling with detailed logging

#### User Experience
- **Responsive Design**: Mobile-friendly web interface
- **Real-time Feedback**: Immediate upload status and file information
- **Drag & Drop**: Modern file input with visual feedback
- **Progress Indication**: Clear success/error messages

#### API Capabilities
- **RESTful Design**: Standard HTTP methods and status codes
- **JSON Responses**: Structured API responses for easy integration
- **File Metadata**: Returns file size, type, and S3 path information
- **Health Monitoring**: Built-in health check endpoint

### Upload via Web Interface
1. Open `http://localhost:8080` in your browser
2. Select a file using the file picker
3. Click "Upload to S3"
4. View upload status and file information

### Upload via API
```bash
# Upload a file using curl
curl -X POST -F "file=@your_file.pdf" http://localhost:8080/upload

# List uploaded files
curl http://localhost:8080/files

# Download a file
curl -O http://localhost:8080/download/your_file.pdf
```

### API Response Examples

#### Successful Upload Response
```json
{
  "message": "File uploaded successfully!",
  "file_info": {
    "filename": "document.pdf",
    "s3_path": "images/document.pdf",
    "size": 1024000,
    "content_type": "application/pdf"
  }
}
```

#### File List Response
```json
{
  "files": [
    {
      "key": "images/document.pdf",
      "size": 1024000,
      "last_modified": "2024-01-15T10:30:00.000Z",
      "etag": "abc123def456"
    }
  ],
  "count": 1
}
```

#### Health Check Response
```json
{
  "status": "healthy",
  "s3_connection": "ok",
  "bucket": "my-new-bucket"
}
```

### Expected Output
```
2024-01-XX XX:XX:XX - __main__ - INFO - Starting Flask S3 Upload Server...
2024-01-XX XX:XX:XX - __main__ - INFO - Available endpoints:
2024-01-XX XX:XX:XX - __main__ - INFO -   GET  / - Upload page
2024-01-XX XX:XX:XX - __main__ - INFO -   POST /upload - Upload file via API
2024-01-XX XX:XX:XX - __main__ - INFO -   POST /upload-web - Upload file via web form
2024-01-XX XX:XX:XX - __main__ - INFO -   GET  /files - List uploaded files
2024-01-XX XX:XX:XX - __main__ - INFO -   GET  /download/<filename> - Download file
2024-01-XX XX:XX:XX - __main__ - INFO -   GET  /health - Health check
```

## Accessing Uploaded Data

### Method 1: LocalStack Desktop (Recommended)
1. Open LocalStack Desktop application
2. Navigate to S3 service
3. Select `my-new-bucket`
4. Browse to `images/` directory
5. Click on `file.pdf` to download and view

### Method 2: AWS CLI with LocalStack
```bash
# List files in the bucket
awslocal s3 ls s3://my-new-bucket/images/

# Download the file
awslocal s3 cp s3://my-new-bucket/images/file.pdf ./downloaded_file.pdf
```

### Method 3: Direct HTTP Access
```bash
# Download via curl
curl -X GET "http://localhost:4566/my-new-bucket/images/file.pdf" -o downloaded_file.pdf
```

### Method 4: Flask Server Download
```bash
# Download via Flask server
curl -O http://localhost:8080/download/file.pdf
```

### Method 5: Python Script Access
```python
import boto3

s3_client = boto3.client(
    's3',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    endpoint_url='http://localhost:4566'
)

# Download file
s3_client.download_file('my-new-bucket', 'images/file.pdf', 'local_file.pdf')
```

## Flask Server Components

### Core Functions (`app.py`)

#### `get_file_mimetype(filename)`
- Automatically detects MIME type based on file extension
- Supports 15+ file types including documents, images, and archives
- Falls back to `application/octet-stream` for unknown types

#### `list_s3_files()`
- Retrieves all files from the S3 bucket
- Returns file metadata including size, modification date, and ETag
- Handles S3 connection errors gracefully

#### `upload_file()` (API endpoint)
- Handles programmatic file uploads via POST requests
- Returns JSON responses with file information
- Includes comprehensive error handling

#### `upload_file_web()` (Web endpoint)
- Processes file uploads from the web form
- Renders HTML responses with upload status
- Provides user-friendly error messages

#### `download_file(filename)`
- Streams files directly from S3 to the client
- Sets appropriate HTTP headers for file downloads
- Handles file not found errors

#### `health_check()`
- Monitors S3 connection status
- Returns system health information
- Useful for monitoring and debugging

### HTML Template Features
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface with CSS styling
- **Real-time Feedback**: Dynamic status messages and file information display
- **Form Validation**: Client-side file selection validation
- **API Documentation**: Built-in endpoint reference

## Key Benefits

- **No AWS Account Required**: Develop and test S3 functionality locally
- **Cost Effective**: No charges for API calls or storage
- **Fast Development**: Instant feedback without network latency
- **Offline Development**: Works without internet connection
- **Visual Management**: LocalStack Desktop provides intuitive file management
- **Web Interface**: User-friendly upload page with drag-and-drop support
- **API Integration**: RESTful endpoints for programmatic access
- **Multiple File Types**: Supports PDF, images, documents, and more
- **Production Ready**: Comprehensive error handling and logging
- **Scalable Architecture**: Modular design for easy extension

## Troubleshooting

### Common Issues
1. **LocalStack not running**: Ensure Docker is running and LocalStack is started
2. **Authentication errors**: Verify LOCALSTACK_AUTH_TOKEN is set correctly
3. **File not found**: Ensure `file.pdf` exists in the project directory
4. **Connection refused**: Check if LocalStack is running on port 4566
5. **Flask server not starting**: Install dependencies with `pip install -r requirements.txt`
6. **Upload failures**: Check file size limits (16MB max) and file permissions
7. **Port conflicts**: Ensure port 8080 is available for Flask server
8. **Method not allowed errors**: Ensure form posts to `/upload-web` endpoint
9. **CORS issues**: Flask server runs on `0.0.0.0` to accept connections from any IP
10. **File type detection**: Check file extension is supported or manually set MIME type

### Verification Commands
```bash
# Check LocalStack status
curl http://localhost:4566/_localstack/health

# Check Flask server health
curl http://localhost:8080/health

# List all buckets
awslocal s3 ls

# Check specific bucket contents
awslocal s3 ls s3://my-new-bucket/images/

# List files via Flask API
curl http://localhost:8080/files
```

## References

### Primary Guide
- **[How to Simulate AWS S3 on Your Local Machine with LocalStack](https://dev.to/nagatodev/how-to-simulate-aws-s3-on-your-local-machine-with-localstack-53dl)** - Comprehensive step-by-step guide covering LocalStack setup, S3 bucket creation, file uploads, and verification methods. This article provides the foundation for understanding LocalStack S3 simulation and includes practical examples with code snippets.

### Additional Resources
- [LocalStack Documentation](https://docs.localstack.cloud/) - Official LocalStack documentation and API reference
- [AWS S3 with boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/service/s3.html) - AWS SDK for Python S3 service documentation
- [LocalStack CLI Installation](https://docs.localstack.cloud/getting-started/installation/) - LocalStack CLI setup guide
- [LocalStack Desktop](https://app.localstack.cloud/) - Visual management interface for LocalStack services
Backend Local Mockup

# LocalStack
We're using localstack to simulate AWS infrastructure we may be using later. LocalStack emulates an AWS-like environment so we can practice creating these kinds of processes then apply them later.

## Prerequisites 

### Python
- we probably gonna use Python so have that I assume u have it if not download!!!, and get pip or whatver package manager u like

### Boto3 / AWS SDK for Python
- This allows us to interact with AWS services from within our Python code using `pip install boto3` unless u use a different package manager then u can figure it out

### Docker 
- Install Docker [Install Docker](https://www.docker.com/get-started/) 
- Very useful tool, read about it, it is good if you wanna be a SWE
- We're gonna use it to run LocalStack within a container on our machines

### Docker Compose
- This should be included in the base Docker download ^
- Docker Compose helps us orchestrate more than one container and lots of useful config all in one file (docker-compose.yaml)


## Quick Start

- Go to the directory these files are in on your computer 
- Open up your terminal
- `docker compose up` will automatically find the file named docker-compose.yaml in the current working directory and then do all of that stuff for u
- `docker compose down` takes it down, make sure to do this whenever you're done since it uses up resources on your machine
