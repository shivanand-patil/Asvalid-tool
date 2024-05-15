#!/bin/bash

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip is not installed, installing now..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
    echo "pip installed successfully."
else
    echo "pip is already installed."
fi

# Install Python packages from requirements.txt
if [ -f requirements.txt ]; then
    echo "Installing Python packages from requirements.txt..."
    sudo pip install -r requirements.txt
else
    echo "requirements.txt not found. No Python packages to install."
fi

# Install the tool
echo "Installing the tool..."
mkdir -p /usr/local/bin/asvalid-tool
sudo cp * /usr/local/bin/asvalid-tool/
sudo chmod +x /usr/local/bin/asvalid-tool/*.sh

# Create symbolic link
sudo ln -sf /usr/local/bin/asvalid-tool/asvalid.sh /usr/local/bin/asvalid

# Install cron
bash /usr/local/bin/asvalid-tool/cron.sh

echo "Installation complete."

