from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from bs4 import BeautifulSoup
import time

# WebDriverの設定と起動
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-s hm-usage')

chrome_driver = webdriver.Chrome(options=options)

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
    chrome_driver.save_screenshot('MoneyForward_screenshot1.png')
    print("MoneyForwardのトップページにアクセス:成功！")

    first_login_button.click()

    # 1-3.マネーフォワード IDでログインページの「ログイン」ボタンを押下
    second_login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="submitto"]'))
    )

    # スクリーンショットを撮る
    chrome_driver.save_screenshot('MoneyForward_screenshot2.png')
    print("マネーフォワード IDでログインページにアクセス:成功！")

    second_login_button.click()

    # 1-4. パスワードを入力 @マネーフォワード IDでログイン(パスワード入力)ページ
    password_input = wait.until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="mfid_user[password]"]'))
    )
    # スクリーンショットを撮る
    chrome_driver.save_screenshot('MoneyForward_screenshot3.png')
    print("マネーフォワード IDでログイン(パスワード入力)ページにアクセス:成功！")

    time.sleep(5)

#    password = getpass("パスワードを入力してください: ")  # パスワードを非表示で入力
#    password_input.send_keys(password)  # パスワードを入力

    password_input.send_keys("Miy877937811")  # パスワードを入力

    # 1-5. 「ログインする」ボタンを押下 @マネーフォワード IDでログイン(パスワード入力)ページ
    third_login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="submitto"]'))
    )
    third_login_button.click()

    # 2. ログイン成功確認のため、スクリーンショットを取得
    # 2-1. 「家計簿」タブを押下
    kakeibo_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="header-container"]/header/div[2]/ul/li[2]/a'))
    )
    # スクリーンショットを撮る
    chrome_driver.save_screenshot('MoneyForward_screenshot4.png')
    print("MoneyForwardMeにログイン成功！")

    kakeibo_link.click()

    # 3. ログアウト
    # 3-1. 「ログアウト」ボタンを押下
    header_logout = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="header-container"]/header/div[1]/nav/ul/li[4]/a'))
    )

    header_logout.click()

    # 3-2. マネーフォワード ME へのログインページに戻る
    first_login_button_2 = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/div/div/div[3]/a'))
    )

    # スクリーンショットを撮る
    chrome_driver.save_screenshot('MoneyForward_screenshot5.png')
    print("ログアウト成功！")

except Exception as e:
    print("エラーが発生しました:", e)

finally:
    # ブラウザを閉じる
    chrome_driver.quit()
    print("ブラウザを終了しました。")