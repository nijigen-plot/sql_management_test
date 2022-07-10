# ルートディレクトリからの実行を想定しています。
import os
import pathlib


def search(target_directory: str):
    os.chdir(target_directory)
    return list(map(lambda x: str(x), list(pathlib.Path(".").glob("**/*.sql"))))
