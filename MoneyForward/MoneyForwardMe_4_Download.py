import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from bs4 import BeautifulSoup
import time
import os
import shutil  # shutilモジュールをインポート
from googleapiclient.discovery import build  # build関数をインポート
import glob
from googleapiclient.http import MediaFileUpload  # MediaFileUploadクラスをインポート

#1. MoneyForward ME にログインする
# WebDriverの設定と起動
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-s hm-usage')

chrome_driver = webdriver.Chrome(options=options)
chrome_driver.delete_all_cookies()

# MoneyForward Meにログイン
try:
    # 1-1. MoneyForwardのトップページにアクセス
    chrome_driver.get("https://moneyforward.com/login")

    # 1-2. 「ログイン」ボタンを押下
    wait = WebDriverWait(chrome_driver, 30)
    first_login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/div/div/div[3]/a'))
    )

    # スクリーンショットを撮る
    #chrome_driver.save_screenshot('MoneyForward_screenshot1.png')
    #print("MoneyForwardのトップページにアクセス:成功！")

    first_login_button.click()
    #time.sleep(10)
    # email/password を入れる
    email = "devmiyoko2024@gmail.com"
    
    password = "Miy877937811"

    # 1-3.マネーフォワード IDでログインページの「ログイン」ボタンを押下
    #タイマーを１０秒に設定
    EC.wait = WebDriverWait(chrome_driver, 10)
    login_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mfid_user[email]"]'))
    )
    if login_input:
        #print("ログインページにアクセス:成功！")
        login_input.send_keys(email)

        second_login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submitto"]'))
        )        
       # print("マネーフォワード IDでログインページにアクセス:成功！")
        second_login_button.click()
    else:
        pass
    
    # 1-4. パスワードを入力 @マネーフォワード IDでログイン(パスワード入力)ページ
    password_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mfid_user[password]"]'))
    )
    #print("マネーフォワード IDでログイン(パスワード入力)ページにアクセス:成功！")

    time.sleep(2)

    # password = getpass("パスワードを入力してください: ")  # パスワードを非表示で入力
    password_input.send_keys(password)  # パスワードを入力

    # 1-5. 「ログインする」ボタンを押下 @マネーフォワード IDでログイン(パスワード入力)ページ
    third_login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="submitto"]'))
    )
    third_login_button.click()

    # 1-6. 「家計簿」タブを押下
    kakeibo_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="header-container"]/header/div[2]/ul/li[2]/a'))
    )
  
    kakeibo_link.click()
    print("MoneyForwardMe/「家計簿」タブにログイン成功！")


    #2. 家計簿データを MoneyForward ME からダウンロードする。
    #2-1. 今月の入出金データをダウンロード

    #ダウンロードボタンを押下
    download_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="js-dl-area"]/a'))
    )
    download_button.click()

    #CSVリンクを押下
    time.sleep(2)
    csv_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="js-csv-dl"]/a'))
    )
  
    csv_link.click()
    print("当月のcsvファイルダウンロード成功！")


    #前月から過去⚪︎⚪︎ヶ月分の入出金データをダウンロード（⚪︎⚪︎分繰り返し）
    #for i in range(1, 12): #11回前矢印ボタンを押下
    for i in range(1, 3): #開発中は2回までに設定
        print(f"{i}回目のボタン押下")
        time.sleep(2)        
        # 前矢印ボタンをクリック
        prev_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="in_out"]/div[2]/button[1]'))
        )
        prev_button.click()
        time.sleep(2)  

        #ダウンロードボタンを押下
        download_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="js-dl-area"]/a'))
        )
        download_button.click()

        #CSVリンクを押下
        time.sleep(2)
        csv_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="js-csv-dl"]/a'))
        )
    
        csv_link.click()

except Exception as e:
    print("エラーが発生しました:", e)

finally:
    # ブラウザを閉じる
    chrome_driver.quit()
    print("ブラウザを終了しました。")


# 4. ダウンロードしたファイルを「mfmedata」フォルダに格納
download_folder = os.path.expanduser("~/Downloads")  # ダウンロードフォルダのパスを取得
mfmedata_folder = os.path.join(download_folder, "mfmedata")  # mfmedataフォルダのパスを作成

if not os.path.exists(mfmedata_folder):  # mfmedataフォルダが存在しない場合は作成
    os.makedirs(mfmedata_folder)

for filename in os.listdir(download_folder):  # ダウンロードフォルダ内のファイルをループ
    if filename.startswith("収入・支出詳細_"):  # moneyforward_で始まるファイルのみ処理
        source_path = os.path.join(download_folder, filename)  # ダウンロードフォルダ内のファイルパス
        destination_path = os.path.join(mfmedata_folder, filename)  # mfmedataフォルダ内のファイルパス
        shutil.move(source_path, destination_path)  # ファイルを移動

# 5. 「mfmedata」フォルダ内にあるファイルを全てGoogleドライブにアップロード
# Google スプレッドシートに接続するための認証情報を取得

# 認証情報ファイルのパスを指定
jsonf = "/Users/aokikazuteru/Downloads/samurai/MoneyForward/credentials.json"

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
gc = gspread.authorize(credentials)

# Google Drive APIのサービスオブジェクトを作成
drive_service = build('drive', 'v3', credentials=credentials)

# アップロード先のフォルダIDを指定
folder_id = '1PZjhy-l2Bf2wcRojjXqR6o7wX9m1WUHc'

# 「mfmedata」フォルダ内のCSVファイルを全てアップロード
for filename in glob.glob(os.path.join(mfmedata_folder, '*.csv')):
    file_metadata = {'name': os.path.basename(filename), 'parents': [folder_id]}
    media = MediaFileUpload(filename, mimetype='text/csv')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")} をアップロードしました')