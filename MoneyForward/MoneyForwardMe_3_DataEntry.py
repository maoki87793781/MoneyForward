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

#1. Google スプレッドシートからデータを読み込む
def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    return worksheet

# 認証情報ファイルのパスを指定
# jsonf = "credentials.json"
jsonf = "/Users/aokikazuteru/Downloads/samurai/MoneyForward/credentials.json"

# スプレッドシートのキーを指定
spread_sheet_key = "1SJ_s0zWG1xw-6JfeP2IIubMe7bAcqyX8DdM5SdJ4ahk"

# スプレッドシートに接続
worksheet = connect_gspread(jsonf, spread_sheet_key)

# 家計簿データを読み込む
# pandasを使ってデータを読み込み、データフレームに格納
records = worksheet.get_all_records()
df = pd.DataFrame(records).head()

# データフレームを表示
#print(df)

#2. MoneyForward ME にログインする
# WebDriverの設定と起動
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-s hm-usage')

chrome_driver = webdriver.Chrome(options=options)
chrome_driver.delete_all_cookies()

# MoneyForward Meにログイン
try:
    # 2-1. MoneyForwardのトップページにアクセス
    chrome_driver.get("https://moneyforward.com/login")

    # 2-2. 「ログイン」ボタンを押下
    wait = WebDriverWait(chrome_driver, 30)
    first_login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/div/div/div[3]/a'))
    )

    # スクリーンショットを撮る
    chrome_driver.save_screenshot('MoneyForward_screenshot1.png')
    print("MoneyForwardのトップページにアクセス:成功！")

    first_login_button.click()
    #time.sleep(10)
    # email/password を入れる
    email = "devmiyoko2024@gmail.com"
    
    password = "Miy877937811"

    # 2-3.マネーフォワード IDでログインページの「ログイン」ボタンを押下
    #タイマーを１０秒に設定
    EC.wait = WebDriverWait(chrome_driver, 10)
    login_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mfid_user[email]"]'))
    )
    if login_input:
        print("ログインページにアクセス:成功！")
        login_input.send_keys(email)

        second_login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submitto"]'))
        )        
        print("マネーフォワード IDでログインページにアクセス:成功！")
        second_login_button.click()
    else:
        pass
    
    # 2-4. パスワードを入力 @マネーフォワード IDでログイン(パスワード入力)ページ
    password_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mfid_user[password]"]'))
    )
    print("マネーフォワード IDでログイン(パスワード入力)ページにアクセス:成功！")

    time.sleep(2)

    # password = getpass("パスワードを入力してください: ")  # パスワードを非表示で入力
    password_input.send_keys(password)  # パスワードを入力

    # 2-5. 「ログインする」ボタンを押下 @マネーフォワード IDでログイン(パスワード入力)ページ
    third_login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="submitto"]'))
    )
    third_login_button.click()

    # 2-6. 「家計簿」タブを押下
    kakeibo_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="header-container"]/header/div[2]/ul/li[2]/a'))
    )
  
    kakeibo_link.click()
    print("MoneyForwardMe/「家計簿」タブにログイン成功！")

    #3. 家計簿データを MoneyForward ME に登録する
    for index, row in df.iterrows():
        time.sleep(2)        
        # 手入力ボタンをクリック
        input_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kakeibo"]/section/div[1]/div[1]/div/button'))
        )
        input_button.click()

        if row['振替'] == 1:
            # 振替タブをクリック
            transfer_tab = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="success"]'))
            )
            transfer_tab.click()
            print("振替の入力")
            print(row['振替'])        
            print(row['日付'])
            print(row['内容'])
            print(row['金額（円）'])    
            print(row['大項目'])
            print(row['中項目'])
            print(row['メモ'])                            

            # 日付を入力
            date_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="updated-at"]'))
            )
            time.sleep(2)
            date_input.clear()
            date_input.send_keys(row['日付'])
            time.sleep(2)
            # 振替金額を入力
            amount_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="appendedPrependedInput"]'))
            )
            amount_input.send_keys(row['金額（円）'])

            # 項目を入力
            large_category_select = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="js-large-category-selected"]'))
            )
            large_category_option = large_category_select.find_element(By.XPATH, f'//option[text()="{row["大項目"]}"]')
            large_category_option.click()

            # 内容を入力
            memo_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="js-content-field"]'))
            )
            memo_input.send_keys(str(row['内容'])) 

            # 登録ボタンをクリック
            save_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-button"]'))
            )
            save_button.click()

            # 続けて入力ボタンをクリック
            coninue_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="confirmation-button"]'))
            )
            coninue_button.click()
            time.sleep(2)
            print("続けて入力ボタン成功！")

            # closeボタンをクリック
            close_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form-user-asset-act"]/div[1]/div'))
            )
            close_button.click()     

        elif row['金額（円）'] < 0:
            # 支出タブをクリック
            expense_tab = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="important"]'))
            )
            expense_tab.click()
            print("支出の入力")
            print(row['振替'])        
            print(row['日付'])
            print(row['内容'])
            print(row['金額（円）'])    
            print(row['大項目'])
            print(row['中項目'])
            print(row['メモ'])                            

            # 日付を入力
            date_input = WebDriverWait(chrome_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="updated-at"]'))
            )
            time.sleep(2)
            date_input.clear()
            date_input.send_keys(row['日付'])
            time.sleep(2)
            # 支払金額を入力
            amount_input = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="appendedPrependedInput"]'))
            )
            #マイナスは入力できないのでプラスに変換
            amount =row['金額（円）'] * -1
            amount_input.send_keys(amount)

            # 項目を入力
            large_category_select = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="js-large-category-selected"]'))
            )
            large_category_option = large_category_select.find_element(By.XPATH, f'//option[text()="{row["大項目"]}"]')
            large_category_option.click()

            # 内容を入力
            memo_input = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="js-content-field"]'))
            )
            memo_input.send_keys(str(row['内容'])) 

            # 登録ボタンをクリック
            save_button = WebDriverWait(chrome_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-button"]'))
            )
            save_button.click()

            # 続けて入力ボタンをクリック
            coninue_button = WebDriverWait(chrome_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="confirmation-button"]'))
            )
            coninue_button.click()
            time.sleep(2)
            print("続けて入力ボタン成功！")

            # closeボタンをクリック
            close_button = WebDriverWait(chrome_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form-user-asset-act"]/div[1]/div'))
            )
            close_button.click()        

        else:
            # 収入タブをクリック
            income_tab = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="info"]'))
            )
            income_tab.click()
            print("収入の入力")
            print(row['振替'])        
            print(row['日付'])
            print(row['内容'])
            print(row['金額（円）'])    
            print(row['大項目'])
            print(row['中項目'])
            print(row['メモ'])                            

            # 日付を入力
            date_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="updated-at"]'))
            )
            time.sleep(2)
            date_input.clear()
            date_input.send_keys(row['日付'])
            time.sleep(2)
            # 収入金額を入力
            amount_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="appendedPrependedInput"]'))
            )
            amount_input.send_keys(row['金額（円）'])

            # 項目を入力
            # ①要素をクリック
            time.sleep(2)            
            large_category_select = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="js-large-category-selected"]')))
            large_category_select.click()  # クリックして選択肢を表示
            if row['大項目'] == "通信費":
                large_category_option = large_category_select.find_element(By.XPATH, '//*[@id="6"]')
                large_category_option.click()

            elif row['大項目'] == "食費":
                large_category_option = large_category_select.find_element(By.XPATH, '//*[@id="11"]')
                large_category_option.click()
            else:
                large_category_option = large_category_select.find_element(By.XPATH, '//*[@id="11"]')
                large_category_option.click()

            # 内容を入力
            memo_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="js-content-field"]'))
            )
            memo_input.send_keys(str(row['内容'])) 

            # 登録ボタンをクリック
            save_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-button"]'))
            )
            save_button.click()

            # 続けて入力ボタンをクリック
            coninue_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="confirmation-button"]'))
            )
            coninue_button.click()
            time.sleep(2)
            print("続けて入力ボタン成功！")

            # closeボタンをクリック
            close_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form-user-asset-act"]/div[1]/div'))
            )
            close_button.click()          
        
    # 登録完了まで待機
    time.sleep(2)


except Exception as e:
    print("エラーが発生しました:", e)

finally:
    # ブラウザを閉じる
    chrome_driver.quit()
    print("ブラウザを終了しました。")

