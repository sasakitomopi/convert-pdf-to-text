FROM python:3.11-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-jpn \
    git \
    libgl1 \ 
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 依存関係をインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# mcp-ocrを直接インストール
RUN pip install mcp-ocr

# アプリケーションファイルをコピー
COPY . .

# MCPサーバーとしてstdio接続で起動
CMD ["python", "-m", "mcp_ocr"]