from keys import CarKeys
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

car = CarKeys()

aws_access_key_id =  boto3.client("dynamodb",
                                  region_name="localhost",
                                  endpoint_url="http://localhost:8000",
                                  aws_access_key_id=car.get_access_key(),
                                  aws_secret_access_key=car.get_secret_key())
# Use the following function instead when using DynamoDB in the Cloud
def create_dynamodb_client_put_cloud(region):
    return boto3.client("dynamodb", region_name=region)

def create_dynamodb_client_query_cloud(region):
    return boto3.resource("dynamodb", region_name=region)

# use the following functions when pointing to localhost
def create_dynamodb_client_put(dynamodb=None):
   return boto3.client("dynamodb", endpoint_url="http://localhost:8000")

def create_dynamodb_client_query(dynamodb=None):
    return boto3.resource("dynamodb", endpoint_url="http://localhost:8000")


def register_nonProfit(id, name, email, category, tagline, mission, website):
     # need to hide region
    dynamodb_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")


    companyInfo = {
        "TableName": "Animals",
        "Item": {
            "ID": {"N": "{id}".format(id=id)},
            "Name": {"S": name},
            "Email": {"S": email},
            "Category": {"S": category},
            "Tagline": {"S": tagline},
            "Mission": {"S": mission},
            "Website": {"S": website},
            "TotalContribution": {"N": "0"}
        }
    }

    try:
        response = dynamodb_client.put_item(**companyInfo)
        print("Successfully put item.")
        print(response)
        # Handle response
    except BaseException as error:
        print("Unknown error while putting item: " + error.response['Error']['Message'])


def GetNextId(tableName):
    # need to hide region
    dynamodb_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")

    lastItem = dynamodb_client.scan(
        TableName=str(tableName)
    )

    try:
        print(len(lastItem["Items"]))
        nextIDNumber = len(lastItem["Items"]) + 1
        return nextIDNumber
        # Handle response
    except BaseException as error:
        print("Unknown error while putting item: " + error.response['Error']['Message'])


# Create the DynamoDB Client with the region you want
dynamodb_client_put_cloud = create_dynamodb_client_put_cloud("us-east-2") # hide region
dynamodb_client_query_cloud = create_dynamodb_client_query_cloud("us-east-2")

#local DynamoDB client
dynamodb_client_put = create_dynamodb_client_put()
dynamodb_client_query = create_dynamodb_client_query()