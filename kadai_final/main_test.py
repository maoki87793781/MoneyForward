import pandas as pd
import glob
import os
import chardet  # 文字コード判定ライブラリを追加

# CSVファイルが格納されているフォルダのパスを指定
#folder_path = '/path/to/your/csv/files'  # ご自身の環境に合わせて変更してください

download_folder = os.path.expanduser("~/Downloads")  # ダウンロードフォルダのパスを取得
folder_path = os.path.join(download_folder, "mfmedata")  # mfmedataフォルダのパスを作成

def csv_to_json(folder_path):
    """
    指定されたフォルダ内のCSVファイルを全て読み込み、JSON形式に変換して返す関数

    Args:
        folder_path (str): CSVファイルが格納されているフォルダのパス

    Returns:
        str: JSON形式の文字列
    """
    try:
        # フォルダ内のCSVファイルを全て読み込み、データフレームに結合
        all_df = pd.DataFrame()
        for filename in glob.glob(os.path.join(folder_path, "収入・支出詳細_*.csv")):
            
            # ファイルのエンコーディングを検出
            with open(filename, 'rb') as f:
                result = chardet.detect(f.read())
            encoding = result['encoding']

            # 検出したエンコーディングでCSVファイルを読み込む
            df = pd.read_csv(filename, encoding=encoding)
            
            all_df = pd.concat([all_df, df])

        # データフレームをJSON形式に変換
        json_data = all_df.to_json(orient='records')

        return json_data

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

if __name__ == '__main__':
    json_data = csv_to_json(folder_path)
    if json_data:
        print(json_data)  # JSONデータを出力