#!/usr/bin/env bash
set -e

# ASCII banner
cat << "EOF"


  █████████  █████                                        █████████  █████                 █████   
 ███░░░░░███░░███                                        ███░░░░░███░░███                 ░░███    
░███    ░░░  ░███████    ██████   ████████   ██████     ███     ░░░  ░███████    ██████   ███████  
░░█████████  ░███░░███  ░░░░░███ ░░███░░███ ███░░███   ░███          ░███░░███  ░░░░░███ ░░░███░   
 ░░░░░░░░███ ░███ ░███   ███████  ░███ ░░░ ░███████    ░███          ░███ ░███   ███████   ░███    
 ███    ░███ ░███ ░███  ███░░███  ░███     ░███░░░     ░░███     ███ ░███ ░███  ███░░███   ░███ ███
░░█████████  ████ █████░░████████ █████    ░░██████     ░░█████████  ████ █████░░████████  ░░█████ 
 ░░░░░░░░░  ░░░░ ░░░░░  ░░░░░░░░ ░░░░░      ░░░░░░       ░░░░░░░░░  ░░░░ ░░░░░  ░░░░░░░░    ░░░░░  
                                
                                ShareChat Setup Script


EOF

# Step 1: Ensure requests library is installed
if ! python3 -c "import requests" &> /dev/null; then
  echo "📦 Installing Python 'requests' module..."
  pip3 install --user requests
else
  echo "✅ Python 'requests' already installed"
fi

echo
# Step 2: Prompt for Google Chat webhook URL
cat << "INSTR"
To send messages to Google Chat, you need an Incoming Webhook URL:
  1. Open your Chat space in Google Chat.
  2. Click the space name > Configure webhooks > Add webhook.
  3. Copy the generated URL.
INSTR
read -p "Enter your Google Chat Webhook URL: " GCHAT_WEBHOOK_URL

echo
# Step 3: Prompt for GoFile API token
cat << "INSTR"
To get your GoFile API token:
  1. Visit https://gofile.io/ and log in or create an account.
  2. Go to your profile page and locate 'API token'.
INSTR
read -p "Enter your GoFile API Token: " GOFILE_TOKEN

echo
# Step 4: Prompt for folder IDs
cat << "INSTR"
You have created three folders in your GoFile account:
  • Image_Files   (e.g. https://gofile.io/d/<shortLink> )
  • Python_Files  
  • Other_Files   
To find each folder's ID:
  - Go to https://gofile.io/managefiles, open the folder.
  - The URL will be https://gofile.io/managefiles/<folderId>.

Please enter the IDs below.
INSTR
read -p "Image_Files Folder ID: " IMAGE_FOLDER_ID
read -p "Python_Files Folder ID: " PYTHON_FOLDER_ID
read -p "Other_Files Folder ID: " OTHER_FOLDER_ID

echo
# Step 5: Write to shell config
RCFILE="$HOME/.bashrc"
{
  echo "# -- ShareChat setup --"
  echo "export GCHAT_WEBHOOK_URL=\"$GCHAT_WEBHOOK_URL\""
  echo "export GOFILE_TOKEN=\"$GOFILE_TOKEN\""
  echo "export IMAGE_FOLDER_ID=\"$IMAGE_FOLDER_ID\""
  echo "export PYTHON_FOLDER_ID=\"$PYTHON_FOLDER_ID\""
  echo "export OTHER_FOLDER_ID=\"$OTHER_FOLDER_ID\""
  echo "alias sendtext='python3 ~/path/to/FileMsgShare.py --message'"
  echo "alias sendfile='python3 ~/path/to/FileMsgShare.py --file'"
} >> "$RCFILE"

echo "♻️ Reloading $RCFILE..."
# shellcheck source=/dev/null
source "$RCFILE"

echo
# Step 6: Usage instructions
cat << "USAGE"
🎉 Setup complete!
You can now use:
  sendtext "Your message here"
  sendfile "/path/to/your/file.ext"
USAGE
