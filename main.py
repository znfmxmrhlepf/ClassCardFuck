from selenium import webdriver
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--AMGI", help="AMGI HAKSUB")
parser.add_argument("--SPEED", help="SPEED QUIZ")
args = parser.parse_args()

Id = input('아이디를 입력하세요 : ')
passwd = input('비번을 입력하세요 : ')
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome('C:\\Users\\choim\\OneDrive\\바탕 화면\\chromedriver', options=options)
driver.implicitly_wait(3)

def LOGIN(driver):
    '''
    로그인
    '''
    driver.get('https://www.classcard.net/Login')

    driver.find_element_by_id('login_id').send_keys(Id)
    driver.find_element_by_id('login_pwd').send_keys(passwd)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div[2]/button').click()
    
    print('로그인 완료')

    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div[3]/div[2]/a').click()

    # 단어 개수 구함
    cards = int(driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/a/span').text.split(' ')[0])
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/a').click()

    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[2]/div[1]/div/a').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[2]/div[1]/div/ul/li[1]/a').click()
    
    return cards

def AMGI(driver, cards):
    '''
    암기 학습
    '''

    driver.find_element_by_xpath('//*[@id="tab_set_all"]/div[1]/div/div[2]/a[1]').click()
    time.sleep(1)

    for _ in range(cards):
        driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[3]/div[1]/a').click()
        driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[3]/div[2]/a').click()
        driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[2]/div[4]/a').click()

    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/a').click()

def SPEED(driver):
    '''
    스피드 퀴즈
    '''
    
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/a').click()
    driver.find_element_by_xpath('//*[@id="wrapper-test"]/div/div[1]/div[1]/div[5]/a').click()
    driver.find_element_by_xpath('//*[@id="wrapper-test"]/div/div[1]/div[2]/div[3]/a').click()

    time.sleep(1)
    all_elems = driver.find_elements_by_xpath('//*[@class="cc-table middle fill-parent font-36"]')

    for i in range(1, len(all_elems)+1):
        ans = driver.find_element_by_xpath('//*[@id="testForm"]/div[' + str(i) + ']/div[1]').get_attribute('outerHTML') # 정답
        ans = ans[ans.find('>') + 1:-6]

        try:
            all_elems[i-1].click()
        except:
            pass

        time.sleep(0.3)

        for j in range(1, 5):
            txt = driver.find_element_by_xpath('//*[@id="testForm"]/div[' + str(i) + ']/div[2]/div[2]/div/div[1]/div[' + str(j) + ']/label/div/div').get_attribute('outerHTML')
            txt = txt[txt.find('>') + 1:-6]

            if txt == ans:
                try:
                    driver.find_element_by_xpath('//*[@id="testForm"]/div[' + str(i) + ']/div[2]/div[2]/div/div[1]/div[' + str(j) + ']/label/div').click()
                except:
                    pass

                try:
                    driver.find_element_by_xpath('//*[@id="testForm"]/div[' + str(i) + ']/div[2]/div[2]/div/div[1]/div[' + str(j) + ']/label/div').click()
                except:
                    pass

                time.sleep(1.55)

    driver.find_element_by_xpath('//*[@id="wrapper-test"]/div/div[3]/div[1]/div[3]/a').click()
    driver.find_element_by_xpath('//*[@id="wrapper-test"]/div/div[3]/div[2]/div[3]/a[2]').click()

cards = LOGIN(driver)

if args.AMGI:
    AMGI(driver, cards)

if args.SPEED:
    SPEED(driver)

# # 리콜 학습
# driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/a').click()
# driver.find_element_by_xpath('//*[@id="tab_set_section"]/div[1]/div[1]/div/div[3]/a[3]').click()

# time.sleep(1)

# for i in range(10):
#     print(driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/span').text)
#     time.sleep(1)
#     driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[2]/div[3]/a').click()

driver.close()