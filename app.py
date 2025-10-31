from flask import Flask, request, jsonify, render_template_string
import os
import logging
from werkzeug.utils import secure_filename
from base import upload_to_s3, create_S3_client
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# HTML template for the upload page
UPLOAD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S3 File Upload</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .upload-form {
            margin: 20px 0;
        }
        input[type="file"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 2px dashed #ddd;
            border-radius: 5px;
            background: #fafafa;
        }
        button {
            background: #007bff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        button:hover {
            background: #0056b3;
        }
        .status {
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .file-info {
            background: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 S3 File Upload</h1>
        <p>Upload files to your LocalStack S3 bucket</p>
        
        <form class="upload-form" method="post" action="/upload-web" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload to S3</button>
        </form>
        
        {% if message %}
        <div class="status {{ 'success' if success else 'error' }}">
            {{ message }}
        </div>
        {% endif %}
        
        {% if file_info %}
        <div class="file-info">
            <h3>File Information:</h3>
            <p><strong>Filename:</strong> {{ file_info.filename }}</p>
            <p><strong>S3 Path:</strong> {{ file_info.s3_path }}</p>
            <p><strong>Size:</strong> {{ file_info.size }} bytes</p>
            <p><strong>Content Type:</strong> {{ file_info.content_type }}</p>
        </div>
        {% endif %}
        
        <div style="margin-top: 30px; text-align: center;">
            <h3>API Endpoints:</h3>
            <p><code>POST /upload</code> - Upload file via API</p>
            <p><code>GET /files</code> - List uploaded files</p>
            <p><code>GET /download/&lt;filename&gt;</code> - Download file</p>
        </div>
    </div>
</body>
</html>
"""


def get_file_mimetype(filename):
    """Get MIME type based on file extension"""
    mimetypes = {
        '.pdf': 'application/pdf',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.zip': 'application/zip',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    }
    
    ext = os.path.splitext(filename.lower())[1]
    return mimetypes.get(ext, 'application/octet-stream')


def list_s3_files():
    """List all files in the S3 bucket"""
    try:
        s3_client = create_S3_client()
        response = s3_client.list_objects_v2(Bucket='my-new-bucket')
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'etag': obj['ETag'].strip('"')
                })
        
        return files
    except ClientError as e:
        logger.error(f"Error listing S3 files: {e}")
        return []


@app.route('/')
def index():
    """Main upload page"""
    return render_template_string(UPLOAD_TEMPLATE)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload file endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Read file bytes
        file_bytes = file.read()
        
        # Get MIME type
        mimetype = get_file_mimetype(filename)
        
        # Create S3 path (upload to images/ directory)
        s3_path = f"images/{filename}"
        
        # Upload to S3
        success = upload_to_s3(file_bytes, s3_path, mimetype)
        
        if success:
            file_info = {
                'filename': filename,
                's3_path': s3_path,
                'size': len(file_bytes),
                'content_type': mimetype
            }
            
            logger.info(f"File {filename} uploaded successfully to S3")
            return jsonify({
                'message': 'File uploaded successfully!',
                'file_info': file_info
            }), 200
        else:
            logger.error(f"Failed to upload file {filename}")
            return jsonify({'error': 'Failed to upload file to S3'}), 500
            
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/upload-web', methods=['POST'])
def upload_file_web():
    """Upload file endpoint for web form"""
    try:
        if 'file' not in request.files:
            return render_template_string(UPLOAD_TEMPLATE, 
                                        message="No file provided", 
                                        success=False)
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template_string(UPLOAD_TEMPLATE, 
                                        message="No file selected", 
                                        success=False)
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Read file bytes
        file_bytes = file.read()
        
        # Get MIME type
        mimetype = get_file_mimetype(filename)
        
        # Create S3 path (upload to images/ directory)
        s3_path = f"images/{filename}"
        
        # Upload to S3
        success = upload_to_s3(file_bytes, s3_path, mimetype)
        
        if success:
            file_info = {
                'filename': filename,
                's3_path': s3_path,
                'size': len(file_bytes),
                'content_type': mimetype
            }
            
            logger.info(f"File {filename} uploaded successfully to S3")
            return render_template_string(UPLOAD_TEMPLATE, 
                                        message="File uploaded successfully!", 
                                        success=True,
                                        file_info=file_info)
        else:
            logger.error(f"Failed to upload file {filename}")
            return render_template_string(UPLOAD_TEMPLATE, 
                                        message="Failed to upload file to S3", 
                                        success=False)
            
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return render_template_string(UPLOAD_TEMPLATE, 
                                    message=f"Error: {str(e)}", 
                                    success=False)


@app.route('/files', methods=['GET'])
def list_files():
    """List all uploaded files"""
    try:
        files = list_s3_files()
        return jsonify({
            'files': files,
            'count': len(files)
        }), 200
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    """Download file from S3"""
    try:
        s3_client = create_S3_client()
        s3_path = f"images/{filename}"
        
        # Get file from S3
        response = s3_client.get_object(Bucket='my-new-bucket', Key=s3_path)
        
        # Return file data
        return response['Body'].read(), 200, {
            'Content-Type': response['ContentType'],
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        
    except ClientError as e:
        logger.error(f"Error downloading file {filename}: {e}")
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test S3 connection
        s3_client = create_S3_client()
        s3_client.head_bucket(Bucket='my-new-bucket')
        
        return jsonify({
            'status': 'healthy',
            's3_connection': 'ok',
            'bucket': 'my-new-bucket'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    logger.info("Starting Flask S3 Upload Server...")
    logger.info("Available endpoints:")
    logger.info("  GET  / - Upload page")
    logger.info("  POST /upload - Upload file via API")
    logger.info("  POST /upload-web - Upload file via web form")
    logger.info("  GET  /files - List uploaded files")
    logger.info("  GET  /download/<filename> - Download file")
    logger.info("  GET  /health - Health check")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
