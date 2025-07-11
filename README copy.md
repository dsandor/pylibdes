# DES Lambda Container

This project creates a Docker container that combines the AWS Lambda Python 3.13 runtime with a compiled DES (Data Encryption Standard) binary. The container includes a Lambda function that automatically processes S3 events to decrypt files using the DES algorithm.

## 🚀 Recent Updates

### ✅ **S3 Event Processing**
- **Automatic file decryption**: Lambda function processes S3 events for encrypted files
- **S3 integration**: Downloads encrypted files, decrypts them, and uploads to `/decrypted` folder
- **Event filtering**: Only processes files in `encrypted/` folder with `.enc` extension
- **Infinite loop prevention**: Ignores files in `decrypted/` path

### ✅ **Infrastructure as Code**
- **CloudFormation template**: Complete AWS infrastructure definition
- **Automated deployment**: GitLab CI/CD pipeline for build and deployment
- **Multi-architecture support**: amd64 and arm64 Docker images
- **Security best practices**: IAM roles, encryption, and access controls

### ✅ **Development Tools**
- **Local testing script**: Automated testing with sample S3 events
- **Docker optimization**: Multi-stage builds and layer caching
- **Comprehensive documentation**: Deployment guide and troubleshooting

## Overview

The container uses a multi-stage build process:
1. **Builder stage**: Compiles the DES binary from C source code using `make gcc`
2. **Runtime stage**: Uses the official AWS Lambda Python 3.13 base image and layers the compiled DES binary on top

### **Workflow**
1. **File Upload**: Encrypted files uploaded to S3 `encrypted/` folder
2. **Event Trigger**: S3 event automatically invokes Lambda function
3. **Processing**: Lambda downloads file, decrypts with DES, uploads to `decrypted/` folder
4. **Cleanup**: Temporary files automatically removed

## Features

- ✅ **Multi-architecture support** (amd64 and arm64)
- ✅ **Official AWS Lambda Python 3.13 base image**
- ✅ **Optimized build process** with .dockerignore
- ✅ **Automated build script** with Docker buildx
- ✅ **S3 event processing** for automatic file decryption
- ✅ **Infrastructure as Code** with CloudFormation
- ✅ **GitLab CI/CD pipeline** for automated deployment
- ✅ **Local testing tools** for development
- ✅ **Security best practices** (IAM, encryption, access controls)
- ✅ **Monitoring and logging** with CloudWatch

## Prerequisites

### **Local Development**
- Docker with buildx support
- Access to the `c_code` directory containing the DES source code
- `jq` for JSON processing (for local testing)

### **AWS Deployment**
- AWS CLI configured with appropriate permissions
- AWS account with access to:
  - CloudFormation
  - ECR (Elastic Container Registry)
  - Lambda
  - S3
  - IAM
  - CloudWatch Logs

### **GitLab CI/CD**
- GitLab project with CI/CD enabled
- GitLab runner with Docker executor
- AWS credentials configured in GitLab CI/CD variables

## Building the Container

### Using the build script (recommended)

```bash
# Build for both amd64 and arm64 (default)
./build.sh

# Build for specific platforms
./build.sh --platforms linux/amd64
./build.sh --platforms linux/arm64

# Custom image name and tag
./build.sh --image-name my-des-lambda --tag v1.0.0

# Show help
./build.sh --help
```

### Manual build

```bash
# Build for current platform only
docker build -t libdes-lambda:latest .

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t libdes-lambda:latest .
```

### **GitLab CI/CD Build**

The GitLab pipeline automatically builds and pushes multi-architecture images:

```bash
# Push to main/develop branch triggers automatic build
git push origin main
```

## Container Structure

The final container contains:
- **AWS Lambda Python 3.13 runtime**
- **Compiled DES binary** at `/var/task/des`
- **Python Lambda handler** at `/var/task/lambda_function.py`
- **Python dependencies** (boto3, botocore) for S3 operations
- **Working directory** set to `/var/task`

### **File Organization**
```
/var/task/
├── des                    # DES binary (executable)
├── lambda_function.py     # Lambda handler
├── requirements.txt       # Python dependencies
└── __pycache__/          # Python cache (created at runtime)
```

## Usage in AWS Lambda

### **Quick Deployment**
1. **Set up GitLab variables** (AWS credentials)
2. **Push to main branch** - Automatic deployment to `dev` environment
3. **Upload encrypted files** to S3 `encrypted/` folder
4. **Monitor processing** via CloudWatch Logs

### **Manual Deployment**
1. Build the container using the build script
2. Push to Amazon ECR (if using the build script with `--push`)
3. Deploy CloudFormation stack with `cloudformation.yaml`
4. Configure S3 trigger to invoke the Lambda function when files are uploaded
5. The Lambda function will automatically decrypt files and upload them to the `/decrypted` folder

### **S3 Event Processing**

The Lambda function processes S3 events and:
- **Downloads encrypted files** from S3
- **Decrypts them** using the DES binary with key "my_key" (`des -k "my_key" -d input_file output_file`)
- **Uploads decrypted files** to the same bucket in the `/decrypted` folder
- **Ignores files** already in the `/decrypted` path to prevent infinite loops
- **Handles multiple files** in a single event
- **Includes proper error handling** and cleanup

### **Included Python Lambda Handler**

The container includes a pre-built Python handler (`lambda_function.py`) that processes S3 events for automatic file decryption.

**S3 Event Processing:**
- **Monitors S3 bucket** for new file uploads
- **Downloads encrypted files** to Lambda's temporary storage
- **Decrypts files** using DES binary with key "my_key" (`des -k "my_key" -d input output`)
- **Uploads decrypted files** to `/decrypted` folder in the same bucket
- **Handles multiple files** in a single event
- **Includes proper error handling** and cleanup

**Example S3 Event Response:**
```json
{
  "statusCode": 200,
  "body": {
    "message": "S3 file decryption completed successfully",
    "processed_files": 1,
    "event": { /* S3 event details */ }
  }
}
```

**Error Handling:**
- **Timeout protection**: 5-minute timeout for DES operations
- **S3 permission errors**: Graceful handling of access issues
- **DES operation failures**: Detailed error reporting
- **File cleanup**: Ensures temporary files are removed

### **Custom Python Lambda Function Example**

You can also create your own Lambda function that uses the DES binary:

```python
import subprocess
import json

def lambda_handler(event, context):
    try:
        # Execute the DES binary
        result = subprocess.run(
            ['/var/task/des', '-e', '-k', 'your-key', 'input-file'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            })
        }
    except subprocess.TimeoutExpired:
        return {
            'statusCode': 408,
            'body': json.dumps({'error': 'DES operation timed out'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### **Local Testing**

Use the provided testing script for local development:

```bash
# Run comprehensive local tests
./scripts/local-test.sh

# This script will:
# 1. Build the Docker image
# 2. Start the Lambda container
# 3. Test directory listing functionality
# 4. Test S3 event processing (simulated)
# 5. Test multiple file handling
# 6. Clean up containers automatically
```

## Build Process Details

### **Stage 1: Builder**
- Uses `python:3.13-slim` as base
- Installs gcc and make
- Copies C source code from `c_code/` directory
- Runs `make gcc` to compile the DES binary

### **Stage 2: Runtime**
- Uses `public.ecr.aws/lambda/python:3.13` (official AWS Lambda base)
- Copies the compiled DES binary from the builder stage
- Installs Python dependencies (boto3, botocore)
- Copies Lambda handler and requirements
- Sets proper permissions and working directory

### **Dependencies**
- **boto3**: AWS SDK for S3 operations
- **botocore**: Core AWS functionality
- **requirements.txt**: Proper dependency management

## Architecture Support

The build script supports:
- **`linux/amd64`** - x86_64 architecture
- **`linux/arm64`** - ARM64 architecture (AWS Graviton)

### **Multi-Architecture Benefits**
- **Cost optimization**: ARM64 instances are typically cheaper
- **Performance**: ARM64 can be faster for certain workloads
- **Flexibility**: Deploy to any AWS region with different instance types

## Testing Locally

### **Quick Test**
You can test the Lambda function locally using Docker:

```bash
# Build the image
docker build -t libdes-lambda:test .

# Run the container locally
docker run -p 9000:8080 libdes-lambda:test lambda_function.lambda_handler

# In another terminal, invoke the function
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{}'
```

### **Comprehensive Testing**
Use the automated testing script for thorough testing:

```bash
# Run all tests automatically
./scripts/local-test.sh

# This includes:
# - Directory listing test
# - S3 event simulation
# - Multiple file processing
# - Error handling verification
```

## AWS Deployment

### **CloudFormation Template**

A complete CloudFormation template (`cloudformation.yaml`) is provided that creates:

- **S3 Bucket**: For encrypted/decrypted files with proper security settings
- **ECR Repository**: For storing the Lambda container image
- **Lambda Function**: Using the container image with S3 event triggers
- **IAM Roles**: With minimal required permissions
- **S3 Event Notifications**: Triggers Lambda on file uploads to `encrypted/` folder
- **CloudWatch Logs**: For monitoring and debugging

### **GitLab CI/CD Pipeline**

The `.gitlab-ci.yml` file provides automated deployment:

1. **Build Stage**: 
   - Builds multi-architecture Docker image (amd64/arm64)
   - Pushes to ECR with commit-based tagging
   - Uses Docker layer caching for faster builds

2. **Deploy Stage**:
   - Deploys CloudFormation stack
   - Configures S3 event triggers
   - Sets up IAM permissions
   - Provides deployment outputs

3. **Cleanup Stage**:
   - Removes old ECR images (keeps last 10)
   - Manages storage costs

### **Quick Deployment**

1. **Set up GitLab variables**:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_DEFAULT_REGION`

2. **Push to main branch** - Automatic deployment to `dev` environment

3. **Manual deployment** - Use the `deploy-manual` job for other environments

### **Infrastructure Benefits**
- **Infrastructure as Code**: Version-controlled infrastructure
- **Security**: IAM roles, encryption, access controls
- **Monitoring**: CloudWatch logs and metrics
- **Cost optimization**: Lifecycle policies and cleanup
- **Scalability**: Multi-architecture support

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## IAM Permissions

The Lambda function requires the following IAM permissions for S3 operations:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": "arn:aws:s3:::your-bucket-name/decrypted/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::your-bucket-name"
        }
    ]
}
```

### **Security Features**
- **Principle of least privilege**: Minimal required permissions
- **Resource-level permissions**: Specific bucket and path access
- **No public access**: S3 bucket blocks all public access
- **Encryption**: Server-side encryption for all data

## Notes

### **Build Optimizations**
- The source code is not included in the final image, only the compiled binary
- The DES binary is compiled with gcc optimizations (`-O3 -fomit-frame-pointer`)
- Multi-stage Docker build reduces final image size
- Docker layer caching speeds up builds

### **Security & Best Practices**
- The container follows AWS Lambda best practices for size and security
- The Lambda function uses temporary files for processing and cleans them up automatically
- Files in the `/decrypted` path are ignored to prevent infinite processing loops
- IAM roles follow principle of least privilege
- S3 bucket has encryption and access controls

### **Performance Considerations**
- Lambda timeout set to 15 minutes for large files
- Memory allocation of 1024MB for optimal performance
- Temporary file cleanup prevents storage issues
- Multi-architecture support for cost optimization

### **Monitoring & Debugging**
- CloudWatch Logs capture all Lambda execution details
- S3 event monitoring via CloudTrail
- Stack outputs provide resource information
- Local testing script for development debugging 