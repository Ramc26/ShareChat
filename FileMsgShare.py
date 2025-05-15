#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from requests.exceptions import RequestException

# Upload folder IDs
IMAGE_FOLDER_ID  = "f0c5703a-1a54-4447-9496-f0e0de57f44b"
PYTHON_FOLDER_ID = "a834a081-3be8-49fe-b92c-f6e48a7e6f66"
OTHER_FOLDER_ID  = "f38fa7e0-f164-4737-9b5e-76274410ed90"

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
    if ext in IMAGE_EXTS:
        return IMAGE_FOLDER_ID
    if ext == "py":
        return PYTHON_FOLDER_ID
    return OTHER_FOLDER_ID


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
        folder_id = choose_folder_id(ext)
        try:
            link = upload_file_to_gofile(path, token, folder_id)
            send_file_link(webhook, link)
        except Exception as e:
            err = f"⚠️ Ooops! Error: {e}"
            print(err, file=sys.stderr)
            # send error to chat
            try:
                requests.post(webhook, json={"text": err})
            except:
                pass
            sys.exit(1)


if __name__ == "__main__":
    main()