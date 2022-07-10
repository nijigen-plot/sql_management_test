# SQLテンプレートファイル同期

## SQLフォーマッターについて
sql-formatter使ってます<br>
使える環境を用意するか、Dockerfileを用意しているので、buildしてその環境で使ってください

```
bash sql_format.sh
```

## Google Driveへの同期について
mainブランチへのプッシュ時にGithub Actionsで同期が走ります<br>
ローカルでのテスト環境としてpoetryを使用
```
pip install poetry==1.2.0b1
poetry install
poetry run python main.py
```