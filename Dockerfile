# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.13-slim

# 作業ディレクトリを/appに設定
WORKDIR /app

# requirements.txtをコンテナにコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトをコンテナにコピー
COPY ./encode_convert ./encode_convert
COPY ./restore_orgfile ./restore_orgfile

# 作業ディレクトリの/workフォルダを作成
RUN mkdir /work

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "-m"]

# メタデータの追加
LABEL org.opencontainers.image.source="https://github.com/bteam-toku/encode_convert_develop.git"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.description="エンコード一括変換／復元（Dockerコンテナ）"