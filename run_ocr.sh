#!/bin/bash

# batch_ocr.pyをDockerコンテナ上で実行するためのヘルパースクリプト

set -e

# デフォルト値
DIRECTORY="/app/image"
LANGUAGE="jpn"

# ヘルプ表示
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -d, --directory DIR    処理するディレクトリ (default: /app/image)"
    echo "  -l, --language LANG    言語コード (default: jpn)"
    echo "  -h, --help             このヘルプを表示"
    echo ""
    echo "Examples:"
    echo "  $0                           # imageディレクトリを日本語で処理"
    echo "  $0 -d /app/images           # imagesディレクトリを日本語で処理"
    echo "  $0 -l eng                   # imageディレクトリを英語で処理"
    echo "  $0 -d /app/images -l eng    # imagesディレクトリを英語で処理"
    echo ""
    echo "対応言語コード:"
    echo "  jpn - 日本語"
    echo "  eng - 英語"
    echo "  fra - フランス語"
    echo "  deu - ドイツ語"
}

# 引数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--directory)
            DIRECTORY="$2"
            shift 2
            ;;
        -l|--language)
            LANGUAGE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            show_help
            exit 1
            ;;
    esac
done

# コンテナが起動しているかチェック
if ! docker ps | grep -q mcp-ocr-server; then
    echo "エラー: mcp-ocr-serverコンテナが起動していません"
    echo "以下のコマンドでコンテナを起動してください:"
    echo "  docker-compose up -d"
    exit 1
fi

# OCR処理実行
echo "OCR処理を開始します..."
echo "ディレクトリ: $DIRECTORY"
echo "言語: $LANGUAGE"
echo ""

docker exec mcp-ocr-server python batch_ocr.py "$DIRECTORY" "$LANGUAGE"

echo ""
echo "OCR処理が完了しました。"
echo "結果は各画像ファイルと同じディレクトリに.txtファイルとして保存されています。"
