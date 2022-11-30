"""
This program creates our ColorsRGB DynamoDB Table in AWS.
Uses our colors.csv file locally to create a cloud Database used for looking up color RGB values.
Entry Example:
    - {"Color": "Blue", "R":46, "B":230, "G":180}
Program handles the creation and loading of the table.

"""
import boto3

def set_up():
    return boto3.resource("dynamodb"), boto3.client("dynamodb")


def create_table(resource, tbl_list, tbl_name):
    if tbl_name not in tbl_list:
        # ALL ATTRIBUTES WILL BE SAVED WITH UPPER CASE LETTERS
        partition_key = "Color"
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


def load_data(resource):
    table = resource.Table("ColorsRGB")
    colors_file = open("./hue_sms/src/colors.csv")
    for line in colors_file.readlines():
        line = line.strip()
        color, R,G,B = line.split(',')
        item_json = {"Color":color, "R":int(R), "G":int(G), "B":int(B)}
        table.put_item(Item=item_json)


def get_table_list(client):
    return list(client.list_tables()["TableNames"])


def main():
    resource, client = set_up()
    create_table(resource, get_table_list(client), "ColorsRGB")
    load_data(resource)


if __name__ == '__main__':
    main()
