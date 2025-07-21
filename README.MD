Install Required Dependencies:

bash
pip install python-pptx zipfile36 openai boto3
npm install @adobe/ccweb-add-on-sdk
Set Environment Variables:

bash
export OPENAI_API_KEY="your_openai_api_key"
export AWS_ACCESS_KEY_ID="your_aws_key"
export AWS_SECRET_ACCESS_KEY="your_aws_secret"
Deploy Lambda Function:

bash
zip -r adscribe-lambda.zip lambda_function.py
aws lambda create-function --function-name adscribe-zip-processor --zip-file fileb://adscribe-lambda.zip