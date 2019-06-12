#! python3
# Verflink.py - for automated testing of links on the page

import os
import bs4
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def status_link(link):
    '''Checks the status of links(200 - working link, another code - non-working)'''
    try:
        res_link = requests.get(link)
        res_link.raise_for_status()
        code_link = res_link.status_code
        return code_link
    except requests.exceptions.HTTPError as err:
        code_link = res_link.status_code
        return code_link
    except:
        print('Error. Could not connect to ' + link + '.')
        code_link = 'unknown'

def click_browser(clickLink):
    '''Clicks on links'''
    try:
        clickElem = WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="'+clickLink+'"]')))
        clickElem.click()
    except:
        print('Runtime Error: unable to click item ' + clickLink + '.')

def sendmail(address, text, file, subject):
    '''Sending letter'''
    try:
        adresElem = browser.find_element_by_id('to')
        adresElem.send_keys(address)
        if text != None:
            textElem = browser.find_element_by_class_name('mi')
            textElem.send_keys(text)
        if file != None:
            #fileElem = browser.find_element_by_name('file0')
            browser.find_element(By.NAME, 'file0').send_keys(file)
        if subject != None:
            subjectElem = browser.find_element_by_name('subject')
            subjectElem.send_keys(subject)
        sendElem = browser.find_element_by_name('nvp_bu_send')
        sendElem.click()
        print('Message to address ' + address + ' sent.')
    except err:
        print(str(err))
        print('Error. Message to address ' + address + ' not sent.')

def auth(login, password):
    '''User authentication'''
    try:
        emailElem = browser.find_element_by_id('identifierId')
        nextElem = browser.find_element_by_id('identifierNext')
        print('id=#login found. Enter the form data.')
        emailElem.send_keys(login)
        nextElem.click()
        passElem = WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.NAME, 'password')))
        print('id=#pass found. Enter the form data.')
        passElem.click()
        passElem.send_keys(password)
        nextElem = browser.find_element_by_id('passwordNext')
        nextElem.click()
    except:
        print('Authorisation Error. Login failed.')


# Verifying link performance
# open browser
url = input('Enter the address of the site page: ')
statusDict = dict()
browser = webdriver.Firefox()

# just in case
browser.maximize_window()

# open the main page
browser.get(url)

# check the main page
status = status_link(url)
if status == 200:

    # add the main page to the dictionary
    code_date = (str(status_link(url)), str(datetime.datetime.now()))
    statusDict[url] = code_date

    # collect items with links
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html5lib')
    linkElem = soup.select('a')

    # pull links
    for i in range(len(linkElem)):
        click = linkElem[i].get('href')

        # exclude contact links
        if click.startswith('mailto:') or click.startswith('tel:') or click.startswith('skype:'):
            click_browser(click)

            # switch to the first tab
            if len(browser.window_handles) > 1:
                browser.switch_to.window(browser.window_handles[0])

            # go back to the main page
            browser.back()

        # pages, transitions, etc.
        elif not click.startswith('https://') or click.startswith('http://'):
            click_browser(click)
            if len(browser.window_handles) > 1:
                browser.switch_to.window(browser.window_handles[0])
            browser.back()
            click = url + click
            status = status_link(click)

            # get the link opening time, add data to the dictionary
            code_date = (str(status), str(datetime.datetime.now()))
            statusDict[click] = code_date

        # like all other links
        else:
            click_browser(click)
            if len(browser.window_handles) > 1:
                browser.switch_to.window(browser.window_handles[0])
            browser.back()
            status = status_link(click)
            code_date = (str(status), str(datetime.datetime.now()))
            statusDict[click] = code_date

else:
    print('Error. Homepage is not working.')
    code_date = (str(status_link(url)), str(datetime.datetime.now()))
    statusDict[url] = code_date
browser.quit()

print('Display the value on the screen: ')
print(str(statusDict))

# Write values to logfile
print('Create logfile...')
folder = 'D:\folder'
folder = os.path.join(folder)
os.chdir(folder)
if click.startswith('https://'):
    name = url[8:-1] + '_' + 'log' + '.txt'
else:
    name = url[7:-1] + '_' + 'log' + '.txt'
logfile = open(name, 'w')
for lin, code in statusDict.items():
    logfile.write(lin + ' - ' + code[0] + ' - ' + code[1] + '\n')
logfile.close()
print('File ' + name + ' create.')

# Send to mail
# open browser without graphical interface
opts = Options()
opts.headless = True
browser = webdriver.Firefox(options=opts)
browser.get('https://accounts.google.com/signin/v2/identifier')

# data required to send mail
logingmail = 'your_mail@gmail.com'
passwordgmail = 'your_password'
textmail = 'Hello, admin'
subj = 'Verification link'
folder = folder + '\\' +  name
folder = os.path.join(folder)

# enter the mail
auth(logingmail, passwordgmail)

# emailing list of recipients
addresslist = ['recipient_email1@gmail.com', 'recipient_email2@gmail.com']

# send emails with logfile
for mailto in addresslist:
    browser.get('https://mail.google.com/mail/u/0/h/x76t70j6yk08/?&cs=b&pv=tl&v=b')
    sendmail(mailto, textmail, folder, subj)

browser.quit()












