import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
# from datetime import datetime, timedelta
import time
import os

# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

TOTAL = 300

browser = webdriver.Chrome(executable_path='D:\ChromeDriver\chromedriver.exe')
wait = WebDriverWait(browser, 10)
total = 0


def isElementExist(byhow, element):
    flag = True
    try:
        browser.find_element(byhow, element)
        # wait.until(EC.presence_of_element_located(element))
        return flag
    except :
        print("No such element:'%s' by %s" % (str(element), str(byhow)))
        flag = False
        return flag


def search():
    try:

        housinglocation = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#searchcityd")))
        housinglocation.clear()
        housinglocation.send_keys('太原')
        time.sleep(1)
        housinglocation.send_keys(Keys.ENTER)


        # chain = ActionChains(browser)
        # menu = browser.find_element_by_css_selector('#list_filter > div.city_l > div.clearfix.mb_14 > div.date_box.city_bg')
        # chain.move_to_element(menu).perform()
        # menu.click()
        #
        # datastart = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#calendar-box > div:nth-child(2) > ul.calendar-day > li:nth-child(16)')))
        # dataend = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#calendar-box > div:nth-child(2) > ul.calendar-day > li:nth-child(17)')))
        # datastart.click()
        # dataend.click()

        # 翻页的时候需要加载完毕

        return True
    except TimeoutException:
        return print("error")

#传递页码
def turn_page(page_to):
    try:
        current_page = 1
        while current_page < page_to:
            # print(current_page)
            # next_page = current_page + 1
            if isElementExist(By.LINK_TEXT, '>'):
                flip = browser.find_element(By.LINK_TEXT, '>')
                # wait.until(EC.element_to_be_clickable, flip).click()
                flip.click()
                pagetag = browser.find_element_by_css_selector('#page_list > div.pagination_v2.pb0_vou > span')
                current_page = int(re.compile('(\d+)').search(pagetag.text).group(1))
                print(current_page)
            else:
                break
            # print(type(browser.find_element(By.LINK_TEXT, '>')))
            # print(type(browser.find_element(By.LINK_TEXT, 'asda')))

            # else:
            #     print("No pages next.")
            #     return False
            # time.sleep(1)

        time.sleep(1)

    except TimeoutException:
        print("TimeOutError")
        return False
    finally:
        return current_page

def get_lodges():
    information = []
    lodges = browser.find_elements_by_css_selector(".lodgeunitpic")
    homepage = browser.current_window_handle
    # time.sleep(1)

    for lodge in lodges:
        lodge.click()
        pages = browser.window_handles
        for page in pages:
            if page != homepage:
                browser.switch_to_window(page)
        information.append(get_info())
        browser.close()
        browser.switch_to_window(homepage)
        time.sleep(1)
        if total >= TOTAL:
            break
    return homepage, information


def get_info():
    global total
    # 拿到网页源代码，进行解析
    html = browser.page_source
    # print(type(html()))
    doc = pq(html)
    # print(doc)

    # if isElementExist(By.CSS_SELECTOR, "#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span"):
    try:
        stringmatch = re.search('_\w*_', str(doc("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span")))
        sex = str(re.search('[a-z]+', stringmatch.group(0)).group(0))
    except:
    # else:
        sex = 'Unknown'
    finally:

    # print(str(doc("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span")))
    # print(stringmatch.group(0))
    # print(type(stringmatch))
    # print(sex.group())

        total += 1
        info = {
            'index': str(total),
            'houseimage': doc("#curBigImage").attr('src'),
            'rent': doc("#pricePart > div.day_l > span").text(),
            'location': doc("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span").text(),
            'title': doc("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em").text(),
            'householder': {
                'name': doc("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a").text(),
                'portrait': doc("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a").attr('href'),
                'sex': sex
            }
        }
        # print(info)
        print("%d:%s" % (total, info))
        # time.sleep(1)

        return info


def write_to_file(pagenum, pageinfo):
    try:
        # now_time = datetime.now()
        # print(now_time)
        # new_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
        # std = now_time.strftime('%c')
        # print(new_time)
        # print(std)


        # parent = os.path.abspath('..')
        # relative_path = 'data'
        # path = os.path.join(parent, relative_path)
        path = 'F:\FOLDER\工作\爬虫\data'
        # print(os.getcwd())
        os.chdir(path)
        # print(os.getcwd())
        info = 'Housing Information' + ' Page ' + str(pagenum) + '.txt'
        file = open(info, 'w', encoding='utf-8')
        # file.write('Start:')
        for element in pageinfo:
            # file.write(str(total))
            file.write(str(element))
            file.write('\n')
        time.sleep(1)

        file.close()
    except TimeoutException:
        print("TimeOutError")
    finally:
        if file:
            file.close()


def main():
    browser.get('http://bj.xiaozhu.com')
    pageto = 1
    search()

    while total < TOTAL:
        before = total
        pagenum = turn_page(pageto)
        if pagenum == pageto:
            # continue
            homepage, pageinfo = get_lodges()
            write_to_file(int(pagenum), pageinfo)
            pageto += 1
        after = total
        print("Number of lodges written:%d" % int(total))
        print("Page:%d, Writted lodges this page:%d" % (int(pagenum), after - before))
        print(total)
        # time.sleep(1)

        # page = browser.current_window_handle
        # if page != homepage:
        #     browser.switch_to_window(homepage)
        #     print("Switch to homepage manually")

        if total >= TOTAL:
            break
    time.sleep(2)
    browser.quit()


    # if isElementExist(By.LINK_TEXT, '>'):
    #     print("True")
    #
    # if isElementExist(By.LINK_TEXT, 'asda'):
    #     print("Found")
    # else:
    #     print("error")

    # lodges = browser.find_elements_by_css_selector(".lodgeunitpic")
    # homepage = browser.current_window_handle
    #
    # for lodge in lodges[0:3]:
    #     lodge.click()
    #     pages = browser.window_handles
    #     for page in pages:
    #         if homepage != page:
    #             browser.switch_to_window(page)
    #     print(get_info())
    #     # information.append(get_info())
    #     time.sleep(1)
    #     browser.close()
    #     browser.switch_to_window(homepage)

    # print(information)
    # turn_page(3)
    # try:
    #     print(type(browser.find_element(By.LINK_TEXT, '>')))
    #     print(type(browser.find_element(By.LINK_TEXT, 'asda')))
    #     if browser.find_element(By.LINK_TEXT, '>'):
    #         print("OK")
    # except:
    #
    #     print("error")
    # finally:
    #     time.sleep(2)
    #     browser.quit()


if __name__ == '__main__':
    main()