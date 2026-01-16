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
COPY ./settings.yaml .
COPY ./pyproject.toml .

# IS_DOCKER環境変数を設定
ENV IS_DOCKER=true
# 標準出力がバッファリングされないよう設定（C#側でリアルタイムに進捗を拾うため）
ENV PYTHONUNBUFFERED=1

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "-m", "encode_convert"]
CMD []

# メタデータの追加
LABEL org.opencontainers.image.source="https://github.com/bteam-toku/encode_convert_develop.git"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.description="エンコード一括変換／復元（Dockerコンテナ）"