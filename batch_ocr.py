import sys
import os
import asyncio
import mcp_ocr_patch
from mcp_ocr import perform_ocr

async def process_file(file_path, language="jpn"):
    """1つのファイルをOCR処理する"""
    try:
        print(f"処理中: {file_path}")
        ocr_result = await perform_ocr(file_path, language=language)
        
        # 結果をファイルに保存
        output_path = file_path + ".txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ocr_result)
        
        print(f"完了: {file_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"エラー ({file_path}): {e}")
        return False

async def process_directory(directory_path, language="jpn"):
    """ディレクトリ内のすべての画像ファイルを処理する"""
    # 対応する画像ファイルの拡張子
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif']
    
    success_count = 0
    error_count = 0
    
    # ディレクトリ内のファイルを取得
    files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) 
             if os.path.isfile(os.path.join(directory_path, f))]
    
    # 画像ファイルのみをフィルタリング
    image_files = [f for f in files if os.path.splitext(f.lower())[1] in image_extensions]
    
    if not image_files:
        print(f"警告: {directory_path} に画像ファイルが見つかりませんでした")
        return
    
    print(f"{len(image_files)}個の画像ファイルを処理します...")
    
    # すべてのファイルを処理
    for file_path in image_files:
        if await process_file(file_path, language):
            success_count += 1
        else:
            error_count += 1
    
    print(f"処理完了: 成功={success_count}, 失敗={error_count}")

async def main():
    if len(sys.argv) < 2:
        print("使用方法: python batch_ocr.py <画像ディレクトリ> [言語コード]")
        sys.exit(1)

    directory_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "jpn"
    
    if not os.path.isdir(directory_path):
        print(f"エラー: {directory_path} はディレクトリではありません")
        sys.exit(1)
    
    await process_directory(directory_path, language)

if __name__ == "__main__":
    asyncio.run(main())