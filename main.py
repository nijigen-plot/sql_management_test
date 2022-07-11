import os
import pathlib

from google_drive import googleDriveSync
from notification_to_slack import notificationDiffFilesToSlack

# ファイルを同期するGoogle Drive フォルダ
GOOGLE_DRIVE_TARGET_ID = "1CpEDoL_vLWibMKar2pFsGAY-F-MSJ9P7"
# 同期元のフォルダ名
SYNC_TARGET_FOLDER = "sql_template"


def search():
    sync_file_list = list(map(lambda x: str(x), list(pathlib.Path(".").glob("**/*.sql"))))
    return sync_file_list


def main():
    os.chdir(SYNC_TARGET_FOLDER)
    # sql_template内のファイルを同期する
    target = search()
    GDS = googleDriveSync(gd_target_folder_id=GOOGLE_DRIVE_TARGET_ID, upload_target_data=target)
    GDS.sync()
    # Slackへ通知を行う
    os.chdir("../")
    NDFTS = notificationDiffFilesToSlack(channel_id="C03NHHQS62K")
    NDFTS.send()


if __name__ == "__main__":
    main()
