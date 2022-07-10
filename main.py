import search_upload_files
from google_drive import googleDriveSync

# ファイルを同期するGoogle Drive フォルダ
GOOGLE_DRIVE_TARGET_ID = "1CpEDoL_vLWibMKar2pFsGAY-F-MSJ9P7"


def main():
    target = search_upload_files.search("sql_template")
    GDS = googleDriveSync(gd_target_folder_id=GOOGLE_DRIVE_TARGET_ID, upload_target_data=target)
    GDS.folder_exist_check()
    GDS.sync()


if __name__ == "__main__":
    main()
