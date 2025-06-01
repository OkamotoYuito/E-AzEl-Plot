# Pythonの公式イメージをベースイメージとして使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピーし、インストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# Railwayが提供するPORT環境変数をリッスンし、外部からアクセス可能なように0.0.0.0で起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"] 