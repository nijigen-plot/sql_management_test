import subprocess


class notificationDiffFilesToSlack:
    def __init__(self):
        # 直前のPRで更新されたsqlファイル一覧を取得
        result = subprocess.run("bash get_pr_diff.sh", shell=True, capture_output=True, text=True).stdout
        self.diff_sql_files = result.split(" ")
        print(self.diff_sql_files)

        # Slackの通知の為の認証

    def send(self):
        
