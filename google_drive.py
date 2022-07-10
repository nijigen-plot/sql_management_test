import base64
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class googleDriveSync:
    def __init__(self, gd_target_folder_id: str):
        # 対象のGoogle DriveフォルダID
        self.sync_folder_id = gd_target_folder_id
        # 環境変数からcredentials情報を作成
        target_env = os.environ.get("GCP_SERVICE_ACCOUNT_KEY")
        if target_env == None:
            raise KeyError("GCP_SERVICE_ACCOUNT_KEY environment not cound.")
        else:
            credentials_json = eval(base64.b64decode(target_env))
        # SCOPEを選択 https://developers.google.com/identity/protocols/oauth2/scopes#drive
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        # 認証を通す
        creds = service_account.Credentials.from_service_account_info(credentials_json, scopes=SCOPES)
        self.service = build("drive", "v3", credentials=creds)

    # 対象のフォルダがあるかを探す
    def folder_exist_check(self):
        results = (
            self.service.files()
            .list(
                q="mimeType='application/vnd.google-apps.folder'", pageSize=10, fields="nextPageToken, files(id, name)"
            )
            .execute()
        )
        items = results.get("files", [])
        if not items:
            print("Folder not found.")
        file_exist = False
        for item in items:
            if item["id"] == self.sync_folder_id:
                file_exist = True
        if file_exist:
            print("Folder is exist.")
            return
        else:
            print("Folder not found.")
            return
