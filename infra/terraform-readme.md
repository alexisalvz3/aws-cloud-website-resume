# Terraform Configuration for AWS Lambda Function

This Terraform configuration sets up an AWS Lambda function with the necessary IAM roles and policies, and creates a function URL for easy invocation. The Lambda function is designed to update a view count in a DynamoDB table.

## Components

### 1. AWS Lambda Function

```hcl
resource "aws_lambda_function" "myfunc" {
    filename         = data.archive_file.zip.output_path
    source_code_hash = data.archive_file.zip.output_base64sha256
    function_name    = "myfunc"
    role             = aws_iam_role.iam_for_lambda.arn
    handler          = "func.lambda_handler"
    runtime          = "python3.12"
}
```

This resource creates a Lambda function named "myfunc". It uses a zip file as the source, sets the function name, assigns an IAM role, specifies the handler (entry point), and sets the runtime to Python 3.12.

### 2. IAM Role for Lambda

```hcl
resource "aws_iam_role" "iam_for_lambda" {
    name = "iam_for_lambda"
    assume_role_policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
            "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }
EOF
}
```

This creates an IAM role that allows the Lambda service to assume this role. This is necessary for the Lambda function to execute with the specified permissions.

### 3. IAM Policy

```hcl
resource "aws_iam_policy" "iam_policy_for_resume_project" {
  name        = "aws_iam_policy_for_terraform_resume_project_policy"
  path        = "/"
  description = "AWS IAM Policy for managing the resume project role"
  policy = jsonencode({...})
}
```

This defines an IAM policy that grants permissions to:

- Write logs to CloudWatch
- Perform UpdateItem, GetItem, and PutItem operations on a specific DynamoDB table named "resume-challenge"

### 4. IAM Role Policy Attachment

```hcl
resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
    role = aws_iam_role.iam_for_lambda.name
    policy_arn = aws_iam_policy.iam_policy_for_resume_project.arn
}
```

This attaches the IAM policy to the IAM role created for the Lambda function, ensuring the Lambda has the necessary permissions. This also decouples the policy for the role and maintains resuability for other roles in the future.

### 5. Archive File

```hcl
data "archive_file" "zip" {
    type         = "zip"
    source_dir   = "${path.module}/lambda/"
    output_path  = "${path.module}/packedlambda.zip"
}
```

This creates a zip file from the contents of the "lambda" directory, which contains the Lambda function code.

### 6. Lambda Function URL

```hcl
resource "aws_lambda_function_url" "url1" {
  function_name = aws_lambda_function.myfunc.function_name
  authorization_type = "NONE"
  cors {...}
}
```

This creates a function URL for the Lambda, allowing it to be invoked via HTTP(S) requests. It sets up CORS (Cross-Origin Resource Sharing) to allow requests from any origin.

## Summary

This Terraform configuration:

1. Creates a Lambda function
2. Sets up the necessary IAM role and policy for the Lambda to access DynamoDB and write logs
3. Packages the Lambda code into a zip file
4. Creates a public URL for the Lambda function with CORS configured

This setup allows a website to call this Lambda function, which can then update the view count in the specified DynamoDB table.
