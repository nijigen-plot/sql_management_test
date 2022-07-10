import base64
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class googleDriveSync:
    def __init__(self, gd_target_folder_id: str, upload_target_data: list):
        # ファイル配置対象のGoogle DriveフォルダID
        self.sync_folder_id = gd_target_folder_id
        # アップロード対象のデータ群ディレクトリリスト
        self.upload_target_data = upload_target_data
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
            return
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

    # フォルダを作成する
    def create_folder(self, folder_name: str):
        try:
            file_metadata = {"title": folder_name, "mimeType": "application/vnd.google-apps.folder"}

            file = self.service.files().create(body=file_metadata, fields="id").execute()

            print(f'Folder has created with ID: "{file.get("id")}".')
        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None
        return file.get("id")

    # ファイルを作成する
    def create_file(self, file_name: str, parent_id=None):
        # parend_idの指定がない場合は、指定フォルダ直下
        if parent_id == None:
            parent_id = self.gd_target_folder_id
        try:
            file_metadata = {"name": file_name, "parents": [parent_id]}
            media = MediaFileUpload(file_name, minetype="text/x-sql", resumable=True)
            file = self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            print(f'File with ID: "{file.get("id")}" has added to the folder with ' f'ID "{parent_id}".')
        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None

    # githubのファイル構造のままsqlファイルをアップロードする
    def create_flow(self, directory: str):
        split_directory = directory.split("/")
        directory_length = len(split_directory)
        parent_id = None
        for i in range(directory_length):
            # directory_lengthよりもiが小さい場合、その名前でフォルダを作成する
            if i + 1 < directory_length:
                parent_id = self.create_folder(folder_name=split_directory[i])
            else:
                self.create_file(file_name=split_directory[i], parent_id=parent_id)

    # sqlファイルを同期する
    def sync(self):
        for target_directory in self.upload_target_data:
            self.create_flow(target_directory)
