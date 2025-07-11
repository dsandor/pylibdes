# Deployment Guide

This guide explains how to deploy the DES Lambda function using the provided CloudFormation template and GitLab CI pipeline.

## Prerequisites

### AWS Requirements
- AWS CLI configured with appropriate permissions
- AWS account with access to:
  - CloudFormation
  - ECR (Elastic Container Registry)
  - Lambda
  - S3
  - IAM
  - CloudWatch Logs

### GitLab Requirements
- GitLab project with CI/CD enabled
- GitLab runner with Docker executor
- AWS credentials configured in GitLab CI/CD variables

## GitLab CI/CD Setup

### 1. Configure GitLab Variables

Add the following variables in your GitLab project's **Settings > CI/CD > Variables**:

| Variable | Description | Required | Protected | Masked |
|----------|-------------|----------|-----------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key for deployment | Yes | Yes | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for deployment | Yes | Yes | Yes |
| `AWS_DEFAULT_REGION` | AWS region for deployment | No | No | No |

### 2. Environment Setup

Create environments in GitLab for different deployment stages:

1. Go to **Deployments > Environments**
2. Create environments:
   - `dev` (for development)
   - `staging` (for staging)
   - `prod` (for production)

## Deployment Process

### Automatic Deployment

The GitLab CI pipeline automatically deploys on:
- **main branch**: Deploys to `dev` environment
- **develop branch**: Deploys to `dev` environment
- **merge requests**: Builds and tests (no deployment)

### Manual Deployment

For other environments or manual deployments:

1. Go to **CI/CD > Pipelines**
2. Click on a successful pipeline
3. Click **deploy-manual** job
4. Select the target environment
5. Click **Play**

## CloudFormation Template Details

### Resources Created

1. **S3 Bucket** (`DataBucket`)
   - Stores encrypted and decrypted files
   - Versioning enabled
   - Server-side encryption (AES256)
   - Public access blocked
   - Lifecycle policy for old versions

2. **ECR Repository** (`ECRRepository`)
   - Stores Docker container images
   - Image scanning enabled
   - Lifecycle policy (keeps last 5 images)

3. **IAM Role** (`LambdaExecutionRole`)
   - Lambda execution role
   - S3 read/write permissions
   - CloudWatch Logs permissions

4. **Lambda Function** (`DESLambdaFunction`)
   - Uses container image from ECR
   - 15-minute timeout
   - 1024MB memory
   - Environment variables for configuration

5. **S3 Event Notification** (`S3EventNotification`)
   - Triggers Lambda on file upload to `encrypted/` folder
   - Filters for `.enc` files only

6. **CloudWatch Log Group** (`LambdaLogGroup`)
   - Logs Lambda function execution
   - 14-day retention

### Parameters

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `ProjectName` | Project name for resource naming | `libdes-lambda` | No |
| `Environment` | Environment name (dev/staging/prod) | `dev` | No |
| `ECRRepositoryName` | ECR repository name | `libdes-lambda` | No |
| `ECRImageTag` | Container image tag | `latest` | No |
| `S3BucketName` | S3 bucket name (globally unique) | - | Yes |

## Usage

### 1. Upload Encrypted Files

Upload encrypted files to the S3 bucket in the `encrypted/` folder:

```bash
# Example: Upload an encrypted file
aws s3 cp myfile.enc s3://your-bucket-name/encrypted/myfile.enc
```

### 2. Monitor Processing

The Lambda function will automatically:
1. Detect the new file in `encrypted/` folder
2. Download it to temporary storage
3. Decrypt it using DES with key "my_key"
4. Upload the decrypted file to `decrypted/` folder
5. Clean up temporary files

### 3. Access Decrypted Files

Decrypted files will be available in the `decrypted/` folder:

```bash
# Example: Download a decrypted file
aws s3 cp s3://your-bucket-name/decrypted/myfile.dec ./myfile.dec
```

## Monitoring and Troubleshooting

### CloudWatch Logs

Monitor Lambda function execution in CloudWatch Logs:
- Log Group: `/aws/lambda/libdes-lambda-{environment}-des-decrypt`
- Logs include download, decryption, and upload steps

### S3 Event Monitoring

Monitor S3 events in CloudTrail:
- Look for `s3:ObjectCreated` events
- Filter by bucket name and prefix `encrypted/`

### Common Issues

1. **Lambda timeout**: Increase timeout in CloudFormation template
2. **Memory issues**: Increase memory allocation
3. **S3 permissions**: Verify IAM role has correct permissions
4. **ECR image not found**: Ensure image is built and pushed before deployment

## Security Considerations

### IAM Permissions
- Lambda role has minimal required permissions
- S3 access limited to specific bucket and paths
- No public access to S3 bucket

### Encryption
- S3 bucket uses server-side encryption
- ECR repository uses encryption at rest
- Lambda environment variables for configuration

### Network Security
- Lambda runs in VPC (if configured)
- No public internet access required
- S3 and ECR access via AWS internal network

## Cost Optimization

### S3 Costs
- Use lifecycle policies to delete old versions
- Consider S3 Intelligent Tiering for infrequently accessed files

### Lambda Costs
- Optimize memory allocation (affects CPU allocation)
- Monitor execution time and adjust timeout

### ECR Costs
- Lifecycle policy keeps only last 5 images
- Cleanup job removes old images automatically

## Cleanup

To remove all resources:

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name libdes-lambda-dev

# Wait for deletion to complete
aws cloudformation wait stack-delete-complete --stack-name libdes-lambda-dev
```

**Note**: This will delete all resources including the S3 bucket and its contents. 