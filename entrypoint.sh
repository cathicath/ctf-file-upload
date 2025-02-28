#!/bin/bash
# Start PHP server in the background
php -S 0.0.0.0:8000 -t /app/uploads &

# Wait 1 sec to make sure PHP starts
sleep 1

# Start Flask
python3 /app/app.py
