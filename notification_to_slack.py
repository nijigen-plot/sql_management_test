import os
import subprocess

from slack_sdk import WebClient


def hide_directory_name(d: str):
    return "/".join(d.split("/")[1:])


class notificationDiffFilesToSlack:
    def __init__(self, channel_id: str):
        # 直前のPRで更新されたファイル一覧を取得
        result = subprocess.run("bash get_pr_diff.sh", shell=True, capture_output=True, text=True).stdout
        result_list = result.split(" ")
        self.diff_sql_files = [hide_directory_name(list_str) for list_str in result_list if ".sql" in list_str]
        print(self.diff_sql_files)

        # Slackの通知の為の認証
        self.slack_client = WebClient(token=os.environ["SLACK_OAUTH_TOKEN"])
        self.slack_channel_id = channel_id

    def send(self):
        nl = "\n"
        # マージ時sqlファイルの更新が無い場合は通知を送らない
        if len(self.diff_sql_files) == 0:
            pass
        else:
            post_text = f"以下のファイルを作成/更新しました。{nl}{nl}{nl.join(self.diff_sql_files)}"
            self.slack_client.chat_postMessage(channel=self.slack_channel_id, text=post_text)
