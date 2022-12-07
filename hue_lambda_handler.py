import requests
import boto3 
from rgbxy import Converter
import json
import string
import random


resource = boto3.resource("dynamodb")

def lambda_handler(event, context):
    print("Received event: " + str(event))
    # Get color from event
    color = clean_name(event["Body"])
    if "SmsMessageSid" not in event.keys():
        return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"\
          "<Response><Message><Body>Non Twilio API 
Call</Body></Message></Response>"
    if not event["SmsMessageSid"].startswith("SM"):
        return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"\
        "<Response><Message><Body>Non Twilio API 
Call</Body></Message></Response>"
    
    phone_num = str(event["From"])[4:] ## Gets rid of prefix from Twilio
    ngrok_address = "https://huesmsaws.ngrok.io" + "/"
    is_Random =False
    if color == "Random":
        is_Random = True
        colors_list = [pn["Color"] for pn in 
resource.Table("ColorsRGB").scan(AttributesToGet=['Color'])["Items"]]
        color = colors_list[random.randint(1, len(colors_list))]
        
    if lookup_rgb_values(color) is None:
        return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"\
          "<Response><Message><Body>Color '{}' Not Recognized - AWS 
Lambda</Body></Message></Response>".format(color)
    
    r,g,b =lookup_rgb_values(color)
    print(color)
    if is_Random:
        insert_data_into_dynamo(phone_num,"Random")
    else:
        insert_data_into_dynamo(phone_num, color)
    x, y, saturation_val = convert(r,g,b)
    
    response_code = requests.post(ngrok_address, json = {'Body':f'{x} {y} 
{saturation_val}'}).status_code
    if response_code == 200:
        if is_Random:
            twilio_response = "<?xml version=\"1.0\" 
encoding=\"UTF-8\"?>"\
          "<Response><Message><Body>Random was used. The light was changed 
to the color '{}' - AWS Lambda</Body></Message></Response>".format(color, 
phone_num)
        else:
            twilio_response = "<?xml version=\"1.0\" 
encoding=\"UTF-8\"?>"\
              "<Response><Message><Body>The light was changed to the color 
'{}' - AWS Lambda</Body></Message></Response>".format(color, phone_num)
        print("Successful HTTP Message Sent to Ngrok")
        return twilio_response
        
    elif 400 <= response_code< 500:
        twilio_response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"\
          "<Response><Message><Body>Error Sending Message to Hue Light - 
AWS Lambda</Body></Message></Response>"
        print("Server not started or Invalid Address...")
        return twilio_response
    else:
        twilio_response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"\
          "<Response><Message><Body>P Error Sending Message to Hue Light - 
AWS Lambda</Body></Message></Response>"
        print("Internal Error")
        return twilio_response
        
    
def lookup_rgb_values(color):
    ## need to look up rgbs from dynamo db
    table = resource.Table("ColorsRGB")
    try:
        color_entry = table.get_item(
        Key={
            'Color': color
        })
        R,G,B = color_entry['Item']["R"], color_entry['Item']["G"], 
color_entry['Item']["B"]
        return int(R),int(G),int(B)
    except Exception as e:
        print("Sorry, the color was not recognized")
        return None
    
    
    
def convert(r,g,b):
    converter = Converter()
    if r == 255 and b == 255 and g == 255:
        saturation_val = 0
        [x, y] = converter.rgb_to_xy(r, g, b)
    else:
        saturation_val = 255
        [x, y] = converter.rgb_to_xy(r, g, b)

    return x, y, saturation_val


def clean_name(name):
    name = name.title()
    name = name.replace('+', ' ') #twilio encodes spaces as + signs for 
some reason
    name = name.strip()
    name = name.replace('\'', '')
    name = name.replace('-', ' ')
    return name.translate(str.maketrans("", "", string.punctuation))


def insert_data_into_dynamo(phone_num, color):
    table = resource.Table("HueLightUserData")
    phone_num_list = [pn["PHONE-NUMBER"] for pn in 
table.scan(AttributesToGet=['PHONE-NUMBER'])["Items"]]
    
    # check that phone number is in Dynamo already
    if phone_num not in phone_num_list:
        table.put_item(Item = {"PHONE-NUMBER":phone_num, "Colors": 
{color:1}})
    
    else:
        # this phone_number has texted the light before
        item = table.get_item(Key={'PHONE-NUMBER': phone_num})
        
        colors_chosen = list(item["Item"]["Colors"].keys())
        
        if color in colors_chosen:
            # increment value of colors if the color has been texted 
before
            colors_dict = dict(item["Item"]["Colors"])
            colors_dict[color]+=1
            table.put_item(Item = {"PHONE-NUMBER":phone_num, 
"Colors":colors_dict})
            print(f"Entered new '{color}' entry for", phone_num)
        else:
            # add a single new color with 1 as the value to the table
            colors_dict = dict(item["Item"]["Colors"])
            colors_dict[color]=1
            table.put_item(Item = {"PHONE-NUMBER":phone_num, "Colors": 
colors_dict})
            print(f"Entered new '{color}' entry for", phone_num)

