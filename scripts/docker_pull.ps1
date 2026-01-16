# 一つ上の親ディレクトリをカレントフォルダリに設定（環境に合わせて変更してください）
Set-Location -Path (Join-Path $PSScriptRoot "..")
# Dockerイメージのプル
docker pull ghcr.io/bteam-toku/encode_convert:latest