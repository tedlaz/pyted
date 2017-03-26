# -*- coding: utf-8 -*-
import argparse
import mechanicalsoup

parser = argparse.ArgumentParser(description='Send sms from your ΟΤΕ account')
parser.add_argument("user")
parser.add_argument("password")
parser.add_argument("mobile")
parser.add_argument("message")
args = parser.parse_args()

browser = mechanicalsoup.Browser()
login_page = browser.get("https://tools.otenet.gr/index.php")
login_form = login_page.soup.select("#login-form")[0].select("form")[0]

# specify username and password
login_form.select("#rcmloginuser")[0]['value'] = args.user
login_form.select("#rcmloginpwd")[0]['value'] = args.password

# submit form
page2 = browser.submit(login_form, login_page.url)

smsurl = "https://tools.otenet.gr/?_task=websms&_action="
smsurl += "plugin.websms_compose&_framed=1"
page3 = browser.get(smsurl)
websmsform = page3.soup.select("#sms-compose-area")[0].select("form")[0]
websmsform.select("#_to")[0].string = args.mobile
websmsform.select("#_message")[0].string = args.message
page4 = browser.submit(websmsform, page3.url)
