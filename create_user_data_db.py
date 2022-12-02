"""
This program creates our HueLightUserData DynamoDB Table in AWS
You need to make sure you set your AWS credentials -- nano ~.aws/credentials
Uses our data.csv file to make data into the form of {"4842747408" :{"blue": 42, "purple":16}
Handles the creation and loading of the table

"""
import boto3
import pandas as pd


def set_up():
    return boto3.resource("dynamodb"), boto3.client("dynamodb")


def create_table(resource, tbl_list, tbl_name):
    if tbl_name not in tbl_list:
        # ALL ATTRIBUTES WILL BE SAVED WITH UPPER CASE LETTERS
        partition_key = "PHONE-NUMBER"
        table = resource.create_table(
            TableName=tbl_name,
            KeySchema=[
                {
                    'AttributeName': partition_key,
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': partition_key,
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }

        )
        print(f"Table {tbl_name} created successfully.")
    else:
        print("Table exists already.")


def delete_table(client, tbl_name):
    try:
        client.delete_table(TableName=tbl_name)
        print(f"Table {tbl_name} deleted successfully")
    except (Exception):
        print("Error deleting table, resource not found")


def format_data(color_data):
    def normalize_phone_num(phone_num):
        phone_num = str(phone_num)
        return phone_num[1:]

    def format_phone_number(data):
        data['Phone #'] = data['Phone #'].apply(normalize_phone_num)
        return data

    def format_time(data):
        data['Time'] = pd.to_datetime(data['Time'])
        return data

    def format_color(data):
        data["Colors"] = data["Colors"].str.title()

    format_color(format_time(format_phone_number(color_data)))
    return color_data


def get_color_counts_dict_for_phone_number(color_data, phone_number):
    color_data_dict = pd.DataFrame(
        pd.DataFrame(color_data[color_data['Phone #'].str.startswith(phone_number)])["Colors"].value_counts()).to_dict()
    color_data_dict["PHONE-NUMBER"] = phone_number

    return color_data_dict


def upload_phone_num_data_to_table(resource, item_json):
    table = resource.Table("HueLightUserData")
    table.put_item(Item=item_json)
    print("Data for", item_json["PHONE-NUMBER"], "added.")


def upload_batch_data(resource, phone_number_list, color_data):
    for curr, phone_number in enumerate(phone_number_list):  ## Get rid of [:3] for all phone numbers
        phone_num_data = get_color_counts_dict_for_phone_number(color_data, phone_number)
        print(phone_num_data)
        upload_phone_num_data_to_table(resource, phone_num_data)
        print(f"---{curr + 1}/{len(phone_number_list)} uploaded.---")


def load_data(resource):
    color_data = format_data(pd.read_csv("./data.csv", names=['Time', 'Phone #', 'Colors', 'Message']))
    phone_number_list = list(color_data["Phone #"].unique())
    upload_batch_data(resource, phone_number_list, color_data)


def get_table_list(client):
    return list(client.list_tables()["TableNames"])


def main():
    resource, client = set_up()
    create_table(resource, get_table_list(client), "HueLightUserData")
    load_data(resource)


if __name__ == '__main__':
    main()
