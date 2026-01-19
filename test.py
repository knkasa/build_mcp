import boto3
from langchain_aws import ChatBedrock

bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id="",
    aws_secret_access_key="",
)

llm = ChatBedrock(
    client=bedrock_runtime,
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    model_kwargs={
        "temperature": 0.5,
        "max_tokens": 5000,
    },
)

response = llm.invoke("Hello.")
print(response.content)
