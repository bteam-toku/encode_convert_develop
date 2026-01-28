# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.13-slim

# uvの実行ファイルを公式バイナリからコピー
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 作業ディレクトリを/appに設定
WORKDIR /app

# requirements.txtをコンテナにコピー
COPY ./pyproject.toml .
COPY ./uv.lock .
# 依存関係をインストール
RUN uv sync --frozen --no-install-project


# スクリプトをコンテナにコピー
COPY ./src ./src
# COPY ./settings.yaml . # 必要に応じて設定ファイルをコピー

# 3. プロジェクト自体をインストール（srcを認識させる）
RUN uv sync --frozen

# IS_DOCKER環境変数を設定
ENV IS_DOCKER=true
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "-m", "encode_convert"]
CMD []

# メタデータの追加
LABEL org.opencontainers.image.source="https://github.com/bteam-toku/encode_convert_develop.git"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.description="エンコード一括変換／復元（Dockerコンテナ）"