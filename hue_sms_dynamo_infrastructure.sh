#!/bin/bash
source ./get_data_from_pi.sh
python3 create_user_data_db.py
python3 create_color_rgb_db
echo "DynamoDB Table Initializing..."
sleep 10