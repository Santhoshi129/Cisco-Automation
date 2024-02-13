from playwright.sync_api import Playwright, sync_playwright,Page
import time,json,requests,base64

url = "https://www.netacad.com/portal/learning"
sleepTime = 3
mail = "adckkd_2244520009@adc.aditya.ac.in"
password = "Thub@123"
server_link = "https://script.google.com/macros/s/AKfycbzF35y1tucDE8B749XDsUICZ4jYWm9h-0bdJ5hyeAiaLh57jx0rYrN9JibGunYqRV_96g/exec"

def SendUpdate(email,password,status):
    data = {"Email":email,"Status":status,"Password":password}
    baseData = base64.b64encode(str(data).replace("'",'"').encode('utf-8'))
    baseData = str(baseData).replace("b'","").replace("'","")
    link =  server_link+"?func=Create&Data="+baseData
    requests.get(link)

def startAnswers(page:Page,module:int):
    try:
        page.wait_for_selector(selector=".quiz-progress",state="visible")
        if module == 1:
            time.sleep(sleepTime)
        time.sleep(sleepTime+sleepTime)
        print(f"Module {module}")
        page.query_selector_all("button")[0].click()
        page.query_selector_all("button")[0].click()
        page.query_selector_all("button")[0].click()
        no = page.query_selector_all("span")[5].text_content()
        no = int(no.split("/")[1])
        print(f"Total Questions : {no}")
        config_path = f"Answers/{module}.json"
        file = open(config_path,"r",encoding="utf-8")
        body = json.loads(file.read())
        for index in range(no):
            Answers = []
            question = str(page.query_selector_all(".quiz-left-box")[0].text_content()).replace("'","").replace('"',"").strip()
            for quest in body:
                if quest["Question"].lower() == question.lower():
                    for answer in quest["Options"]:
                        Answers.append(answer)

            options = page.query_selector_all(".custom-checkbox-wrapper")
            option_no = 0
            for option in options:
                label = option.text_content().replace("'","").replace('"',"").strip()
                if label != "":
                    for val in Answers:
                        if val == label:
                            if "What happens if you try to compile and run this program?\n\n#include <stdio.h> \n\nint fun(int *t) {\n    return *(++t);\n}\n\nint main(void) { \n    int arr[] = { 8, 4, 2, 1 };\n\n    printf(%d\\n, fun(arr + 2));\n    return 0; \n}"==question:
                                if option.get_attribute("for") == "123993":
                                    option.click()
                            else:
                                option.click()
                option_no += 1
            if index == 0 :
                page.query_selector_all("button")[0].click()
            elif index != (no-1):
                page.query_selector_all("button")[1].click()
            elif index == (no-1):
                page.query_selector_all("button")[1].click()
                page.query_selector_all("button")[0].click()
                page.query_selector_all("button")[24].click()
                time.sleep(3)
                page.close()
    except:
        SendUpdate(mail,password,"Failed")


def SelectModule(page : Page,module):
    page.wait_for_selector(selector=".instancename",state="visible")
    linker = page.url
    links = page.query_selector_all(".instancename")
    for link in links:
        if module == 6 :
            if "Part 1" in link.text_content():
                time.sleep(sleepTime)
                with page.expect_popup() as moduleIO:
                    link.click()
                startAnswers(page=moduleIO.value,module=module)
                module+=1
                time.sleep(sleepTime)
                page.reload()
                time.sleep(sleepTime)
                SelectModule(page=page,module=module)
                break
        elif module == 10 :
            if  "Part 2" in link.text_content():
                time.sleep(sleepTime)
                with page.expect_popup() as moduleIO:
                    link.click()
                startAnswers(page=moduleIO.value,module=module)
                module+=1
                time.sleep(sleepTime)
                page.reload()
                time.sleep(sleepTime)
                SelectModule(page=page,module=module)
                break
        elif module == 11 :
            if "Final Test" in link.text_content():
                time.sleep(sleepTime)
                with page.expect_popup() as moduleIO:
                    link.click()
                time.sleep(sleepTime)
                startAnswers(page=moduleIO.value,module=module)
                time.sleep(sleepTime)
                module+=1
                page.goto(linker)
                startingSurvey(page)
                break
        elif module > 6 :
            if f"Module {module-1} Test" in link.text_content():
                time.sleep(sleepTime)
                with page.expect_popup() as moduleIO:
                    link.click()
                time.sleep(sleepTime)
                startAnswers(page=moduleIO.value,module=module)
                time.sleep(sleepTime)
                module+=1
        elif f"Module {module} Test" in link.text_content():
            time.sleep(sleepTime)
            with page.expect_popup() as moduleIO:
                link.click()
            time.sleep(sleepTime)
            startAnswers(page=moduleIO.value,module=module)
            time.sleep(sleepTime)
            module+=1


def startingSurvey(page:Page):
    try:
        numbers = [1,8,15,22,29,31,40,45]
        with page.expect_popup() as pager:
            page.query_selector_all(".instancename")[25].click()
        page = pager.value
        page.wait_for_selector(selector=".required",state="visible")
        for index in numbers:
            page.query_selector_all(".required")[index].click()
        page.query_selector_all(".btn.btn-primary")[0].click()
        print("Satisfaction Survey Completed")
        time.sleep(sleepTime*5)
    except:
        pass


def Login(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    context.set_default_timeout(600*1000)
    context.set_default_navigation_timeout(600*1000)
    try:
        page = context.new_page()
        page.goto(url=url)
        try:
            page.wait_for_selector(selector="#idp-discovery-username",state="visible")
            page.query_selector("#idp-discovery-username").fill(str(mail))
            page.query_selector("#idp-discovery-submit").click()
            time.sleep(3)
        except:
            pass
        page.wait_for_selector(selector="#okta-signin-password",state="visible")
        page.query_selector("#okta-signin-password").fill(str(password))
        with page.expect_navigation():
                page.query_selector("#okta-signin-submit").click()
        page.wait_for_selector(selector=".course-launcher",state="visible")
        time.sleep(3)
        page.query_selector_all(".course-launcher")[0].click()
        SelectModule(page=page,module=1)
        print("All Levels Are Completed")
        SendUpdate(mail,password,"Completed")
        browser.close()
    except :
        browser.close()
        SendUpdate(mail,password,"Failed")


with sync_playwright() as playwright:
    for index in range(10):
        response = requests.get(server_link+"?func=Read")
        object = base64.b64decode(response.text)
        object = json.loads(object)
        if object != {}:
            mail=object['mail']
            password=object['password']
            SendUpdate(mail,password,"Inprogress")
            print("Starting Account...!\nEmail : "+str(mail)+"\nPassword : "+str(password))
            Login(playwright)
