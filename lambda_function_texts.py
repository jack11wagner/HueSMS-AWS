import json
import boto3

## Lambda function to add data to dynamo after a text comes in

def lambda_handler(event, context):
    data = insert_data_into_dynamo(event)
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
    
def db_set_up():
    return boto3.resource("dynamodb"), boto3.client("dynamodb")

def get_phone_number_list(table):
    return [pn["PHONE-NUMBER"] for pn in 
table.scan(AttributesToGet=['PHONE-NUMBER'])["Items"]]
    
def insert_data_into_dynamo(event):
    
    phone_num = list(event.keys())[0]
    color = event[phone_num]
    
    resource, client = db_set_up()
    table = resource.Table("HueLightUserData")
    
    # check that phone number is in Dynamo already
    if phone_num not in get_phone_number_list(table):
        print("Phone-Number not found")
        table.put_item(Item = {"PHONE-NUMBER":phone_num, "Colors": 
{color:1}})
    
    else:
        # confirmed this phone_number has texted the light before
        item = table.get_item(Key={'PHONE-NUMBER': phone_num})
        
        colors_chosen = list(item["Item"]["Colors"].keys())
        
        if color in colors_chosen:
            # increment value of colors if the color has been texted 
before
            colors_dict = dict(item["Item"]["Colors"])
            colors_dict[color]+=1
            table.put_item(Item = {"PHONE-NUMBER":phone_num, 
"Colors":colors_dict})
        else:
            # add a single new color with 1 as the value to the table
            colors_dict = dict(item["Item"]["Colors"])
            colors_dict[color]=1
            table.put_item(Item = {"PHONE-NUMBER":phone_num, "Colors": 
colors_dict})

    return event
    
    

