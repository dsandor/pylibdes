import json
import os
import subprocess
from typing import Dict, Any, List

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler that lists the contents of /var/task directory
    and returns the results as a JSON array response.
    
    Args:
        event: Lambda event object
        context: Lambda context object
        
    Returns:
        Dictionary containing status code and JSON response with directory listing
    """
    try:
        # Get the task root directory (should be /var/task)
        task_root = os.environ.get('LAMBDA_TASK_ROOT', '/var/task')
        
        # List all files and directories in /var/task
        files = []
        try:
            for item in os.listdir(task_root):
                item_path = os.path.join(task_root, item)
                stat_info = os.stat(item_path)
                
                file_info = {
                    'name': item,
                    'path': item_path,
                    'is_directory': os.path.isdir(item_path),
                    'is_file': os.path.isfile(item_path),
                    'size': stat_info.st_size,
                    'permissions': oct(stat_info.st_mode)[-3:],  # Last 3 digits for permissions
                    'executable': os.access(item_path, os.X_OK)
                }
                files.append(file_info)
        except PermissionError as e:
            return {
                'statusCode': 403,
                'body': json.dumps({
                    'error': f'Permission denied accessing {task_root}',
                    'details': str(e)
                })
            }
        except FileNotFoundError as e:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': f'Directory {task_root} not found',
                    'details': str(e)
                })
            }
        
        # Sort files by name for consistent output
        files.sort(key=lambda x: x['name'])
        
        # Create response
        response = {
            'directory': task_root,
            'total_files': len(files),
            'files': files,
            'des_binary_present': any(f['name'] == 'des' and f['is_file'] for f in files),
            'lambda_function_present': any(f['name'] == 'lambda_function.py' and f['is_file'] for f in files)
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response, indent=2)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            })
        } 