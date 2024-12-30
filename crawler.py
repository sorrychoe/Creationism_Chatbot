import os
import warnings
import platform
from time import sleep

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

warnings.filterwarnings("ignore")

if platform.system() in ["Windows", "Linux"]:
    Control = Keys.CONTROL

elif platform.system() == "Darwin":
    Control = Keys.COMMAND

else:
    print("Unsupported OS.")


def get_driver():
    """driver setup"""
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split(".")[0]
    driver_path = f"./{chrome_ver}/chromedriver"
    if os.path.exists(driver_path):
        print(f"chrome driver is installed: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()})

    options = ["--headless", "--no-sandbox"]
    for option in options:
        chrome_options.add_argument(option)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def clear():
    """clear the terminal"""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    sleep(0.5)


def main(url: str):
    """program activation"""
    driver = get_driver()
    driver.get(url)
    sleep(3)
    for num in range(1, 17):
        print("\033[31m" + f"Q{num}번 데이터 추출 시작" + "\033[0m")
        
        driver.find_element(By.XPATH, f'//div[@id="accordion"]/div[{num}]/div[1]/h4/a').click()
        sleep(2)
        
        try:
            even = 2
            while True:
                file_name = driver.find_element(By.XPATH, f'//div[@id="accordion"]/div[{num}]/div[2]/div/div[2]/strong/p[{even-1}]').text
                element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="accordion"]/div[{num}]/div[2]/div/div[2]/strong/p[{even}]/span/a')),
                    )

                actions = ActionChains(driver)
                actions.key_down(Control).click(element).key_up(Control).perform()
                sleep(2)

                main_window = driver.window_handles
                driver.switch_to.window(main_window[1])
                sleep(3)
                    
                try:
                    text = driver.find_element(By.XPATH, '/html/body/div[5]/main/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[1]').text

                    data_path = "./data/"
                    f = open(f'{data_path+file_name}.txt', 'w')
                    f.write(text)
                    f.close()
                    print("\033[96m" + "Crawled" + "\033[0m")
                
                except:
                    print("\033[32m" + "passed" + "\033[0m")

                finally:
                    driver.close()
                    driver.switch_to.window(main_window[0])
                    sleep(1)
                    even += 2
        except :
            print("\033[96m" + f"===Q{num}번 추출 완료===" + "\033[0m")
            
    print("crawling 종료")
    driver.quit()


if __name__ == "__main__":
    url = "https://creation.kr/question05/"
    main(url)