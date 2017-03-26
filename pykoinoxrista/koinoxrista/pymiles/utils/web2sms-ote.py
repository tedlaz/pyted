# -*- coding: utf-8 -*-
import mechanicalsoup


def sent_sms(user, passwd, mobile, msg):
    if not user:
        return False
    if not passwd:
        return False
    if not mobile:
        return False
    if not msg:
        return False

    browser = mechanicalsoup.Browser()
    login_page = browser.get("https://tools.otenet.gr/index.php")
    login_form = login_page.soup.select("#login-form")[0].select("form")[0]

    # specify username and password
    login_form.select("#rcmloginuser")[0]['value'] = user
    login_form.select("#rcmloginpwd")[0]['value'] = passwd

    # submit form
    browser.submit(login_form, login_page.url)

    smsurl = "https://tools.otenet.gr/?_task=websms&_action="
    smsurl += "plugin.websms_compose&_framed=1"
    page3 = browser.get(smsurl)
    websmsform = page3.soup.select("#sms-compose-area")[0].select("form")[0]
    websmsform.select("#_to")[0].string = mobile
    websmsform.select("#_message")[0].string = msg
    browser.submit(websmsform, page3.url)
    return True


if __name__ == '__main__':
    usr = 'tedlaz'
    pwd = 'misthos7'
    tel = '6937736649'
    tel2 = ""
    msg = u"Καλημέρα φίλε μου καλέ :-)"
    print(sent_sms(usr, pwd, tel, msg))
