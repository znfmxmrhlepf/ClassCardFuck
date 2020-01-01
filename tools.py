import getpass
from selenium import webdriver
import time

def getInfo():
    print('---------------------------------------------------------------------------------------------------')
    print("[ 모드를 선택하세요 (s : 스피드퀴즈 / a : 암기학습 / r : 리콜학습) ] (여러개 선택할 땐 공백으로 구분)")
    print('---------------------------------------------------------------------------------------------------')

    Info = {
      'options' : input('>>> : ').split(),
      'Id' : input('아이디를 입력하세요 : '),
      'passwd' : getpass.getpass('비밀번호를 입력하세요 : '),
      'cards_idx' : input('단어장 번호를 입력하세요 (1부터) : '),
      'class_idx' : input('클래스 번호를 입력하세요 (1부터) : ')
    }
   
    return Info

def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(3)

    return driver

def LOGIN(driver, Info):
    '''
    login
    '''
    driver.get('https://www.classcard.net/login')

    # get id/passwd
    driver.find_element_by_id('login_id').send_keys(Info['Id'])
    driver.find_element_by_id('login_pwd').send_keys(Info['passwd'])

    # push login button
    driver.find_element_by_xpath('//*[@id="loginForm"]/div[2]/button').click()
    
    print('로그인 완료')
    try:
        driver.find_element_by_xpath('//*[@id="YBMEventModal"]/div[2]/div/div/div[1]/a').click()
    except:
        pass

    # select class
    multiple_classes = input('가입한 클래스가 여러개인가요? (y/n) : ')
    
    if multiple_classes == 'y':
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div[3]/div[2]/a['+str(Info['class_idx'])+']').click()

    else:
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div[3]/div[2]/a').click()
        
    # get the number of words
    cards_cnt = int(driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div['+str(Info['cards_idx'])+']/div[2]/div[1]/a/span').text.split(' ')[0])
 
    # enter word card page  
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div['+str(Info['cards_idx'])+']/div[2]/div[1]/a').click()

    # if popup exists, remove
    try:
        driver.find_element_by_xpath('//*[@id="tab_set_all"]/div[1]/div/div[2]/div/div[1]/i').click()
    except:
        pass

    # change study setting by all 
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[3]/div[1]/div[2]/a').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[3]/div[1]/div[2]/ul/li[1]/a').click()

    return cards_cnt

def AMGI(driver, cards_cnt):
    '''
    AMGI
    '''

    print('암기학습을 시작합니다')
    driver.find_element_by_xpath('//*[@id="tab_set_all"]/div[1]/div/div[2]/a[1]').click()
    time.sleep(1)

    for cnt in range(cards_cnt):
        driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[3]/div[1]/a').click()
        driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[3]/div[2]/a').click()
        driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[2]/div[4]/a').click()

    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/a').click()

def RECALL(driver, cards_cnt):
    '''
    리콜 학습
    '''

    driver.find_element_by_xpath('//*[@id="tab_set_all"]/div[1]//div/div[2]/a[2]').click()
    time.sleep(1)

    for i in range(1, cards_cnt+1):
        time.sleep(0.1)
        while True:
            state = driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[2]/div[2]/div['+str(i)+']/div[4]').get_attribute('class')
            if state != 'card-cover':
                break

        ans_hidden = driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[2]/div[2]/div['+str(i)+']/div[2]/div/div[1]/span').get_attribute('innerHTML').split('\n')[0]
        print(ans_hidden)
        for j in range(1,5):
            ans = driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[2]/div[2]/div['+str(i)+']/div[3]/div['+str(j)+']/div[2]/div').get_attribute('innerHTML').split('\n')[0]
            print(ans)
            if ans == ans_hidden:
                try:
                    driver.find_element_by_xpath('//*[@id="wrapper-learn"]/div/div/div[2]/div[2]/div['+str(i)+']/div[3]/div['+str(j)+']').click()
                except:
                    pass

    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/a').click()

def SPEED(driver, cards_cnt):
    '''
    스피드 퀴즈
    '''
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[3]/a').click()
    driver.find_element_by_xpath('//*[@id="wrapper-test"]/div/div[1]/div[1]/div[5]/a').click()
    driver.find_element_by_xpath('//*[@id="wrapper-test"]/div/div[1]/div[2]/div[3]/a').click()

    time.sleep(1)
    elems_cnt = len(driver.find_elements_by_xpath('//*[@class="cc-table middle fill-parent font-36"]'))
    for i in range(1, elems_cnt+1):
        ans = driver.find_element_by_xpath('//*[@id="testForm"]/div['+str(i)+']/div/div[2]/div/div[2]/span[2]').get_attribute('innerHTML').split('\n')[0] # 정답

        try:
            driver.find_element_by_xpath('//*[@id="testForm"]/div['+str(i)+']/div/div[1]/div/div').click()
        except:
            pass

        for j in range(1, 5):
            txt = driver.find_element_by_xpath('//*[@id="testForm"]/div['+str(i)+']/div/div[2]/div/div[1]/div['+str(j)+']/label/div/div').get_attribute('innerHTML').split('\n')[0]

            if txt == ans:
                driver.find_element_by_xpath('//*[@id="testForm"]/div['+str(i)+']/div/div[2]/div/div[1]/div['+str(j)+']/label').click()

    driver.find_element_by_xpath('//*[@id="wrapper-test"]/div/div[3]/div[1]/div[3]/a').click()
    driver.find_element_by_xpath('//*[@id="wrapper-test"]/div/div[3]/div[2]/div[3]/a[2]').click()

def getFuncDict():
    fdict = {
        "a" : AMGI,
        "r" : RECALL,
        "s" : SPEED
    }
    
    return fdict