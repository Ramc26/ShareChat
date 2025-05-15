#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from requests.exceptions import RequestException

# File extensions
IMAGE_EXTS = {"png", "jpg", "jpeg", "gif", "bmp"}

def send_text_message(webhook: str, text: str):
    """Send a simple text message to Google Chat webhook."""
    print("🤖 Sending your message now…")
    resp = requests.post(webhook, json={"text": text})
    resp.raise_for_status()
    print("✅ Message sent! 🎉")

def choose_folder_id(ext: str) -> str:
    """Return the appropriate GoFile folder ID based on file extension."""
    image_id  = os.environ.get("IMAGE_FOLDER_ID")
    python_id = os.environ.get("PYTHON_FOLDER_ID")
    other_id  = os.environ.get("OTHER_FOLDER_ID")

    if not all([image_id, python_id, other_id]):
        raise EnvironmentError("Missing one or more folder IDs in environment variables.")

    if ext in IMAGE_EXTS:
        return image_id
    if ext == "py":
        return python_id
    return other_id

def upload_file_to_gofile(path: str, token: str, folder_id: str) -> str:
    """Upload the file to GoFile and return the download link."""
    url = "https://upload.gofile.io/uploadfile"
    headers = {"Authorization": f"Bearer {token}"}
    filename = os.path.basename(path)
    print(f"🚀 Uploading `{filename}` to GoFile folder `{folder_id}`…")
    with open(path, "rb") as f:
        resp = requests.post(
            url,
            headers=headers,
            files={"file": f},
            data={"folderId": folder_id}
        )
    resp.raise_for_status()
    data = resp.json().get("data", {})
    link = data.get("directLink") or data.get("downloadPage")
    if not link:
        raise RuntimeError(f"Unexpected GoFile response: {resp.text}")
    print(f"🔗 File uploaded! Download link: {link}")
    return link

def send_file_link(webhook: str, link: str):
    """Send the GoFile download link to the Chat webhook."""
    send_text_message(webhook, f"📁 Your file is ready: {link}")

def main():
    parser = argparse.ArgumentParser(
        description="Send text or upload a file to GoFile and post link to Google Chat"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--message", nargs='+', help="Text message to send")
    group.add_argument("-f", "--file", help="Path to file to upload and share link")
    args = parser.parse_args()

    webhook = os.environ.get("GCHAT_WEBHOOK_URL")
    token   = os.environ.get("GOFILE_TOKEN")
    if not webhook:
        parser.error("Environment variable GCHAT_WEBHOOK_URL not set")
    if not token:
        parser.error("Environment variable GOFILE_TOKEN not set")

    if args.message:
        text = " ".join(args.message)
        send_text_message(webhook, text)
    else:
        path = args.file
        if not os.path.isfile(path):
            print(f"⚠️ Ooops! File not found: {path}", file=sys.stderr)
            sys.exit(1)
        ext = os.path.splitext(path)[1].lower().lstrip('.')
        try:
            folder_id = choose_folder_id(ext)
            link = upload_file_to_gofile(path, token, folder_id)
            send_file_link(webhook, link)
        except Exception as e:
            err = f"⚠️ Ooops! Error: {e}"
            print(err, file=sys.stderr)
            try:
                requests.post(webhook, json={"text": err})
            except:
                pass
            sys.exit(1)

if __name__ == "__main__":
    main()
