import json
import os
import subprocess
import boto3
import tempfile
from typing import Dict, Any, List
from urllib.parse import unquote_plus

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler that processes S3 events for file decryption.
    
    When a file is uploaded to an S3 bucket (excluding /decrypted path),
    this handler downloads the file, decrypts it using the DES tool,
    and uploads the decrypted file to the /decrypted folder in the same bucket.
    
    Args:
        event: S3 event object containing bucket and key information
        context: Lambda context object
        
    Returns:
        Dictionary containing status code and JSON response
    """
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3')
        
        # Process S3 events
        for record in event.get('Records', []):
            # Extract S3 information from the event
            s3_info = record.get('s3', {})
            bucket_name = s3_info.get('bucket', {}).get('name')
            object_key = unquote_plus(s3_info.get('object', {}).get('key', ''))
            
            # Skip files in the /decrypted path to avoid infinite loops
            if object_key.startswith('decrypted/'):
                print(f"Skipping file in decrypted folder: {object_key}")
                continue
            
            print(f"Processing file: {object_key} from bucket: {bucket_name}")
            
            # Create temporary files for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.enc') as encrypted_file:
                encrypted_path = encrypted_file.name
                
            with tempfile.NamedTemporaryFile(delete=False, suffix='.dec') as decrypted_file:
                decrypted_path = decrypted_file.name
            
            try:
                # Download the encrypted file from S3
                print(f"Downloading {object_key} from S3...")
                s3_client.download_file(bucket_name, object_key, encrypted_path)
                
                # Run DES decryption
                print(f"Decrypting file with DES...")
                des_command = [
                    '/var/task/des',
                    '-k', 'my_key',
                    '-d',
                    encrypted_path,
                    decrypted_path
                ]
                
                result = subprocess.run(
                    des_command,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result.returncode != 0:
                    raise Exception(f"DES decryption failed: {result.stderr}")
                
                # Generate the output key for the decrypted file
                # Remove any existing file extension and add .dec
                base_name = os.path.splitext(os.path.basename(object_key))[0]
                output_key = f"decrypted/{base_name}.dec"
                
                # Upload the decrypted file to S3
                print(f"Uploading decrypted file to s3://{bucket_name}/{output_key}")
                s3_client.upload_file(decrypted_path, bucket_name, output_key)
                
                print(f"Successfully processed {object_key} -> {output_key}")
                
            finally:
                # Clean up temporary files
                try:
                    os.unlink(encrypted_path)
                except OSError:
                    pass
                try:
                    os.unlink(decrypted_path)
                except OSError:
                    pass
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'S3 file decryption completed successfully',
                'processed_files': len(event.get('Records', [])),
                'event': event
            }, indent=2)
        }
        
    except subprocess.TimeoutExpired:
        return {
            'statusCode': 408,
            'body': json.dumps({
                'error': 'DES decryption operation timed out',
                'details': 'The decryption process took longer than 5 minutes'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'S3 file decryption failed',
                'details': str(e)
            })
        } 