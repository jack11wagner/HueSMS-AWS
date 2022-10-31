#!/bin/bash
source ./get_data_from_pi.sh
python3 create_db.py
echo "DynamoDB Table Initializing..."
sleep 10
python3 upload_data.py