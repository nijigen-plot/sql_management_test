#!/bin/sh

# 直近のcloseしたPRの番号を取得する
pulls=$(curl \
-H "Accept: application/vnd.github+json" \
-H "Authorization: token ${GITHUB_TOKEN}" \
"https://api.github.com/repos/${OWNER}/${REPOSITORY}/pulls?state=closed&sort=updated&direction=desc")
pull_number=$(echo $pulls | jq '.[0].number')

# 直近のcloseしたPR番号から変更差分のあるsqlファイル名を取得する
file_names=$(curl \
-H "Accept: application/vnd.github+json" \
-H "Authorization: token ${GITHUB_TOKEN}" \
"https://api.github.com/repos/${OWNER}/${REPOSITORY}/pulls/${pull_number}/files" | \
jq '[.[].filename]' | find -name '*.sql')

echo $file_names
