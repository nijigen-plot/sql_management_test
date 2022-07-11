import search_upload_files
from google_drive import googleDriveSync
from notification_to_slack import notificationDiffFilesToSlack

# ファイルを同期するGoogle Drive フォルダ
GOOGLE_DRIVE_TARGET_ID = "1CpEDoL_vLWibMKar2pFsGAY-F-MSJ9P7"
# 同期元のフォルダ名
SYNC_TARGET_FOLDER = "sql_template"


def main():
    # sql_template内のファイルを同期する
    target = search_upload_files.search(SYNC_TARGET_FOLDER)
    GDS = googleDriveSync(gd_target_folder_id=GOOGLE_DRIVE_TARGET_ID, upload_target_data=target)
    GDS.sync()
    # 指定フォルダ内のファイルを消したいだけの場合以下を実行する
    # GDS.file_delete()
    NDFTS = notificationDiffFilesToSlack(channel_id="C03NHHQS62K")
    NDFTS.send()


if __name__ == "__main__":
    main()
