import msvcrt
import tools as tls

Info = tls.getInfo()
driver = tls.getDriver()
cards = tls.LOGIN(driver, Info)
funcDict = tls.getFuncDict()

for option in Info['options']:
    funcDict[option](driver, cards)

print('아무키나 눌러 종료하세요...')
msvcrt.getch()
driver.close()