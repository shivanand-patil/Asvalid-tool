#!/bin/bash

# Command to add to cron
CRON_COMMAND="*/10 * * * * /usr/local/bin/asvalid verify"

# Check if the cron job already exists
if ! crontab -l | grep -qF "$CRON_COMMAND"; then
    # If it doesn't exist, add it
    (crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -
    echo "Cron job added: $CRON_COMMAND"
else
    echo "Cron job already exists: $CRON_COMMAND"
fi
