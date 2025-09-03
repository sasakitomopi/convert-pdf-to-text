FROM python:3.11

WORKDIR /app

RUN pip install uv

COPY requirements.txt .

# gitがインストールされていないとgit+...は動作しないため、インストールしておく
RUN apt-get update && apt-get install -y git libgl1 tesseract-ocr tesseract-ocr-jpn poppler-utils

RUN uv pip install --system -r requirements.txt

# OCRスクリプトと依存ファイルをコピー
COPY batch_ocr.py .
COPY mcp_ocr_patch.py .

# デフォルトコマンド（対話モードで起動）
CMD ["bash"]

