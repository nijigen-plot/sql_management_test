import os
import subprocess

from slack_sdk import WebClient


class notificationDiffFilesToSlack:
    def __init__(self, channel_id: str):
        # 直前のPRで更新されたsqlファイル一覧を取得
        result = subprocess.run("bash get_pr_diff.sh", shell=True, capture_output=True, text=True).stdout
        self.diff_sql_files = result.split(" ")

        # Slackの通知の為の認証
        self.slack_client = WebClient(token=os.environ["SLACK_OAUTH_TOKEN"])
        self.slack_channel_id = channel_id

    def send(self):
        nl = "\n"
        post_text = f"以下のファイルを作成/更新しました。{nl}{nl}{nl.join(self.diff_sql_files)}"
        self.slack_client.chat_postMessage(channel=self.slack_channel_id, text=post_text)
