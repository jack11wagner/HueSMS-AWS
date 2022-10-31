import boto3


def set_up():
    return boto3.resource("dynamodb"), boto3.client("dynamodb")


def create_table(resource, tbl_list, tbl_name):
    if tbl_name not in tbl_list:
        # ALL ATTRIBUTES WILL BE SAVED WITH UPPER CASE LETTERS
        partition_key= "PHONE-NUMBER"
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

def get_table_list(client):
    return list(client.list_tables()["TableNames"])

def main():
    resource, client = set_up()
    # TABLE NAMES WILL BE SAVED WITH TITLE LETTER CASE
    create_table(resource, get_table_list(client), "HueLightUserData")

if __name__ == '__main__':
    main()
