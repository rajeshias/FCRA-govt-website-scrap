import csv
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pyautogui as pya
import pyperclip
import time


def copy_clipboard():
    pya.moveTo(1450, 500)
    pya.click()
    pya.hotkey('ctrl', 'a')
    time.sleep(0.4)
    pya.hotkey('ctrl', 'c')
    time.sleep(.01)
    return pyperclip.paste()
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver.exe')

action = ActionChains(driver)
wait = WebDriverWait(driver, 600)

driver.get("https://fcraonline.nic.in/fc3_Amount.aspx")
webs = driver.window_handles[0]

driver.switch_to.window(webs)
def extract():
    x = driver.find_elements_by_xpath('//td')
    y = []
    while x:
        y += [x[:6]]
        x = x[6:]
    return y
dist = 35
while dist < 40:
    wait.until(EC.presence_of_element_located((By.XPATH, '//select[@name="DdnListBlockYear"]'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//option[@value="2018-2019"]'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//select[@name="DdnListState"]'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//option[@value="01"]'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//select[@name="DdnListdist"]'))).click()
    try:
        time.sleep(0.2)
        # wait.until(EC.presence_of_element_located((By.XPATH, ))).click()
        # pya.hotkey('end')
        # time.sleep(0.1)
        driver.find_element_by_xpath(f'//option[@value="0{dist}"]').click()
    except:
        dist += 1
        print(dist)
        continue
    time.sleep(0.1)
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="submit"]'))).click()

    final = []
    wait.until(EC.presence_of_element_located((By.XPATH, '//font[@color="red"]')))
    places = driver.find_elements_by_xpath('//font[@color="red"]')
    reqrowdata = [i.text for i in places][1:]

    pdfs = driver.find_elements_by_xpath('//a[@style="color:Blue;"]')
    if not pdfs:
        final.append(reqrowdata)
    for i in tqdm(range(len(pdfs))):
        temp = driver.find_elements_by_xpath('//a[@style="color:Blue;"]')
        temp[i].click()
        while True:
            try:
                time.sleep(0.4)
                driver.switch_to.window(driver.window_handles[1])
                break
            except:
                pass
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/embed')))
        time.sleep(0.4)
        sotere = copy_clipboard()
        pya.hotkey('ctrl', 'w')
        time.sleep(0.3)
        driver.switch_to.window(webs)
        y = extract()
        with open(f'./2018/{y[i][1].text}.txt', 'w') as ok:
            ok.write(sotere)
        final.append(reqrowdata + [k.text for k in y[i]][1:-1])

    with open("new.csv", "a") as fp:
        wr = csv.writer(fp)
        wr.writerows(final)
    print(final)
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="submit"]'))).click()
    dist += 1
