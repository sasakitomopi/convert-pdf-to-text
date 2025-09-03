# Docker OCR 実行ガイド

## 概要
`batch_ocr.py`をDockerコンテナ上で実行するためのセットアップ手順です。

## 前提条件
- Docker
- Docker Compose

## セットアップ

### 1. コンテナをビルドして起動
```bash
docker-compose up -d
```

### 2. 画像ファイルの配置
- `image/` ディレクトリに処理したい画像ファイルを配置
- `images/` ディレクトリも使用可能

### 3. OCR処理の実行

#### コンテナ内でbatch_ocrスクリプトを実行
```bash
# 日本語で処理（デフォルト）
docker exec mcp-ocr-server python batch_ocr.py /app/image

# 英語で処理
docker exec mcp-ocr-server python batch_ocr.py /app/image eng

# 特定のディレクトリを処理
docker exec mcp-ocr-server python batch_ocr.py /app/images jpn
```

#### ワンライナーで実行
```bash
# 日本語OCR（imageディレクトリ）
docker exec mcp-ocr-server python batch_ocr.py /app/image

# 英語OCR（imagesディレクトリ）
docker exec mcp-ocr-server python batch_ocr.py /app/images eng
```

## 出力
- OCRの結果は各画像ファイルと同じディレクトリに`.txt`ファイルとして保存されます
- 例: `image.jpg` → `image.jpg.txt`
- `output/` ディレクトリもマウントされているので、必要に応じて結果をそこにコピーできます

## 対応ファイル形式
- `.jpg`, `.jpeg`
- `.png`
- `.bmp`
- `.tiff`, `.tif`
- `.gif`

## 言語コード
- `jpn`: 日本語（デフォルト）
- `eng`: 英語
- `fra`: フランス語
- `deu`: ドイツ語
- その他のTesseract対応言語

## トラブルシューティング

### コンテナの状態確認
```bash
docker-compose ps
```

### ログの確認
```bash
docker-compose logs mcp-ocr
```

### コンテナ内での対話式実行
```bash
docker exec -it mcp-ocr-server bash
```

### コンテナの再ビルド
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```
