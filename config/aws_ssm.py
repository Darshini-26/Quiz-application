import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def quiz_application1(name,with_decryption=True,region_name=None):

    print(f"Retrieving parameter:{name}")

    try:
        region_name=region_name or os.getenv('AWS_DEFAULT_REGION','us-east-1')
        ssm_client=boto3.client('ssm',region_name=region_name)

        response=ssm_client.get_parameter(Name=name,WithDecryption=with_decryption)
        parameter_value=response['Parameter']['Value']
        return parameter_value
    
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not found")
    except PartialCredentialsError:
        raise RuntimeError("Incomplete AWS credentials")
    except Exception as e:
        raise RuntimeError(f"Error retrieving SSM parameters:{e}")