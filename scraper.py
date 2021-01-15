from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import random
import sys
import unicodedata

# XPATHS STARTS HERTE------->
XtopIntro = '//div[contains(@class, "display-flex mt2")]'

Xabout = '//section[contains(@class, "artdeco-container-card pv-profile-section pv-about-section artdeco-card ember-view")]'
XexpandAbout = '//a[@id="line-clamp-show-more-button"]'

XclosePath = '//header[@class="msg-overlay-bubble-header"]'
XcloseCookieAlert = "//*[contains(@class,'artdeco-global-alert__dismiss artdeco-button artdeco-button--circle artdeco-button--inverse artdeco-button--1 artdeco-button--tertiary ember-view')]"

Xexper_Sec = '//*[@id="experience-section"]'
Xedu_Sec = '//*[@id="education-section"]'
Xrec_Sec = '//section[@class="pv-profile-section pv-recommendations-section artdeco-container-card artdeco-card ember-view"]'

Xexperience = '//section[@class="pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view"]'
XexperienceMulti = './/li[contains(@class,"pv-entity__position-group-role-item")]'
Xeducation = '//li[@class="pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view"]'
Xrecommendation = '//li[@class="pv-recommendation-entity ember-view"]'

XexpandExp = './/button[@class="pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state"]'
Xsee_moreExp = '//a[@id="inline-show-more-text__button link"]'
Xrecsee_more = '//*[@id="line-clamp-show-more-button"][@aria-expanded="false"]'

XloginError = "//div[contains(@class,'form__label--error')]"
Xpin = "//input[contains(@class,'input_verification_pin') or contains(@id,'verification_pin') or contains(@placeholder, 'Enter code')]"
XpinBut = "//button[contains(@id,'pin-submit-button')]"

xAboutCom = "//p[contains(@class,'about-us__description')]"


# email-pin-submit-button
# XPATHS ENDS HERTE<-------


# ACTION METHODS START HERE------>

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return chrome_options


def check_win_open(driver):
    try:
        driver.current_url
        return True
    except:
        return False


# LOG IN
def loginUser(driver):
    driver.get(
        'https://www.linkedin.com/checkpoint/lg/login?trk=homepage-basic_signin-form_submit')
    waitTime = 5
    while ("feed" not in driver.current_url):
        time.sleep(waitTime)


def closeBarriers(driver):
    try:
        time.sleep(2)
        closeChat(driver)
        closeCookieAlert(driver)
    except:
        pass


# LOAD PAGE
def loadPage(link, driver):
    link = link.strip()
    driver.get(link)


# FIND AN  ELEMENT IN A GIVEN LIST
def find(list, target):
    i = 0
    for element in list:
        if target == element:
            return i
            break
        i += 1
    return None


def ListToDic(suffix, givenList):
    keys = []
    i = len(givenList)
    for x in range(1, i + 1):
        keys.append(suffix + str(x))
    data = dict(zip(keys, givenList))
    return data


# CLOSE CHAT
def closeChat(driver):
    while True:
        try:
            closeBut = getElement(driver, XclosePath)
            check = closeBut.get_attribute("data-control-name")
            if "overlay.minimize_connection" in check:
                closeBut.click()
                break
            elif "overlay.maximize_connection" in check:
                break
        except:
            break
            time.sleep(1)


# CLOSE COOKIE ALERT
def closeCookieAlert(driver):
    try:
        closeCookie = getElement(driver, XcloseCookieAlert)
        closeCookie.click()
    except:
        pass


# ERROR FORMATTER
# def printError(e, msg):
#     print('\n_______________________________')
#     print(msg)
#     print(f"Error Type: {type(e).__name__}")
#     print(f"Error Message: {str(e)}")
#     print('_______________________________\n')


# X ACTION METHODS ENDS HERE------>

# ELEMENT EXTRACTOR METHODS START HERE ------>

# GET A ELEMENT SPECIFIC ELEMENT
def getElement(container, xpath):
    element = container.find_element_by_xpath(xpath)
    return element


# GET A LIST OF ELEMENT BELONGING TO SAME CLASS
def getElements(driver, xpath):
    elements = driver.find_elements_by_xpath(xpath)
    return elements


# GET ELEMENT BY FORCE
def findElement(xpath, container, driver):
    scroll = 100
    exp = None
    inc = 100
    while True:
        scroll = scroll + inc
        try:
            exp = getElement(container, xpath)
            break
        except:
            driver.execute_script(f"scroll(0,{scroll})")
            if driver.execute_script("return document.body.offsetHeight;") < scroll:
                scroll = 100
                inc = inc - 10

    return exp


# FIND EXPANSIONS AND EXPAND
def findexpansions(Xcontainer, Xtarget, driver, check):
    if check is True:
        container = Xcontainer
    else:
        container = findElement(Xcontainer, driver, driver)
    if container is not None:
        loc = container.location['y']
        size = container.size['height']
        scroll = loc
        inc = 50
        while scroll < (loc + size):
            driver.execute_script(f"scroll(0,{scroll})")
            try:
                expand = getElement(container, Xtarget)
                expand.click()
                break
            except NoSuchElementException as e:
                pass
            except ElementClickInterceptedException as e:
                inc = 5
                scroll = scroll - 100
            scroll = scroll + inc


# ACTION METHODS ENDS HERE <-----------

# TEXT STRUCTURING METHODS START HERE -------------->

# GET THE NAME OF THE COMPANY THAT EXPERIENCE BELONGS TO
def getCompanyExp(exp):
    companyName = "UNKNOWN"
    if exp is not None:
        lines = exp.split('\n')
        x = find(lines, 'Company Name')
        if x is not None:
            companyName = lines[x + 1]
    return companyName


# TEXT TO STRUCTURED DATA FOR RECOMMENDATIONS
def processRec(rec):
    try:
        lines = rec.split('\n')
        name = lines[0]
        post = lines[1]
        x = lines[2].split(',')
        date = x[0].strip() + " " + x[1].strip()
        relation = ' '.join(x[2:])
        desc = '\n'.join(lines[3:])
        desc = remove_unicode(desc)
        content = {
            "Recommender's Name": name,
            "Recommender's Post": post,
            "Date": date,
            "Recommender's Relation": relation.strip(),
            "Description": desc.strip()
        }
    except:
        content = {}
        pass
    return content


# TEXT TO STRUCTURED DATA FOR EXPERIENCE
def processExp(exp):
    if exp is not None:
        lines = exp.split('\n')
        currentPost = lines[0]
        del lines[0]
        x = find(lines, 'Dates Employed')
        if x is not None:
            dates = lines[x + 1]
            del lines[x + 1]
            del lines[x]
        else:
            dates = " UNKNOWN "
        x = find(lines, 'Employment Duration')
        if x is not None:
            duration = lines[x + 1]
            del lines[x + 1]
            del lines[x]
        else:
            duration = " UNKNOWN "

        x = find(lines, 'Location')
        if x is not None:
            location = lines[x + 1]
            del lines[x + 1]
            del lines[x]
        else:
            location = " UNKNOWN "

        x = find(lines, 'Company Name')
        if x is not None:
            companyName = lines[x + 1]
            del lines[x + 1]
            del lines[x]
        else:
            companyName = " UNKNOWN "
        try:
            z = lines[find(lines, '…')]
            if "see more" in lines[z + 1]:
                del lines[z + 1]
                del lines[z]
        except:
            pass

        desc = '\n'.join(lines)
        if "\n\u2026\nsee more" in desc[len(desc) - 18:]:
            desc = desc[:len(desc) - 11]
        desc = remove_unicode(desc)
        data = {
            "Company Name": companyName,
            "Current Post": currentPost,
            "Dates Employed": (dates.encode()).decode(),
            "Duration": process_date(duration),
            "Location": location,
            "Description": (desc.encode()).decode()
        }
        return data
    else:
        data = {
            "Company Name": "",
            "Current Post": "",
            "Dates Employed": "",
            "Duration": "",
            "Location": "",
            "Description": ""
        }
        return data


def process_date(date):
    try:
        words = date.split(" ")
        x = find(words, 'yrs')
        yrs = 0
        mons = 0
        if x is not None:
            yrs = int(words[x - 1])
        x = find(words, 'mos')
        if x is not None:
            mons = int(words[x - 1])
        exp_dur = round(yrs + (mons / 12), 1)
        return exp_dur
    except:
        return 0


# TEXT TO STRUCTURED DATA FOR MULTI POST EXPERIENCE
def processMulitPostExp(exp):
    temp = []
    for x in exp:
        text = x.text.strip()
        lines = text.split('\n')
        title = "UNKNOWN"
        pos = find(lines, 'Title')
        try:
            if pos != None:
                title = lines[pos + 1]
                del lines[pos + 1]
                del lines[pos]
        except:
            pass

        date = "UNKNOWN"
        pos = find(lines, 'Dates Employed')
        try:
            if pos != None:
                date = lines[pos + 1]
                del lines[pos + 1]
                del lines[pos]
        except:
            pass

        duration = "UNKNOWN"
        pos = find(lines, 'Employment Duration')
        try:
            if pos != None:
                duration = lines[pos + 1]
                del lines[pos + 1]
                del lines[pos]
        except:
            pass

        location = "UNKNOWN"
        pos = find(lines, 'Location')
        try:
            if pos != None:
                location = lines[pos + 1]
                del lines[pos + 1]
                del lines[pos]
        except:
            pass
        try:
            del lines[find(lines, "Full-time")]
        except:
            pass
        try:
            z = lines[find(lines, '…')]
            if "see more" in lines[z + 1]:
                del lines[z + 1]
                del lines[z]
        except:
            pass

        desc = '\n'.join(lines)
        if "\n\u2026\nsee more" in desc[len(desc) - 18:]:
            desc = desc[:len(desc) - 11]

        desc = remove_unicode(desc)

        data = {
            "Post": title,
            "Dates Employed": date,
            "Duration": process_date(duration),
            "Location": location,
            "Description": desc
        }
        temp.append(data)

    return temp


# TEXT STRUCTURING METHODS ENDS HERE <--------------

# FINAL STRUCTURED DATA PROVIDER METHODS STARTS HERE------------>

def process_intro(intro):
    lines = (intro.text).split('\n')
    name = lines[0]
    post = ""
    if "premium" in lines[3] or "Premium" in lines[4]:
        post=lines[5]
    else:
        post=lines[4]

    data = {
        "Name": name,
        "Post": post
    }
    return data


# GET INTRODUCTION
def getIntro(driver):
    try:
        profile = findElement(XtopIntro, driver, driver)
    except Exception as e:
        profile = None
    return process_intro(profile)


# GET ABOUT
def getAbout(driver):
    try:
        findexpansions(Xabout, XexpandAbout, driver, False)
        about = findElement(Xabout, driver, driver)
    except Exception as e:
        about = None
    if about is not None:
        lines = (about.text).split("\n")
        if lines[0] == "About":
            return '\n'.join(lines[1:])
        else:
            formatted_about = u''
            return remove_unicode(about.text)
    else:
        return None


# GET EXPERIENCE
def getExp(driver):
    try:
        findexpansions(Xexper_Sec, XexpandExp, driver, False)
    except Exception as e:
        pass

    try:
        exps = getElements(driver, Xexperience)
    except Exception as e:
        exps = None

    eles = []
    for x in exps:
        multipost = x.find_elements_by_xpath(XexperienceMulti)
        if len(multipost) > 0:
            temp = processMulitPostExp(multipost)
            ##############################################
            data1 = ListToDic("post", temp)
            ###############################################
            final_data = {
                f"{getCompanyExp(x.text)}": data1
            }
            eles.append(final_data)
        else:
            eles.append(processExp(x.text))
    data = ListToDic("exp", eles)
    return data


# GET RECOMMENDATION
def getRec(driver):
    try:
        rec_sec = findElement(Xrec_Sec, driver, driver)
        loc1 = (rec_sec.location)['y']
        size1 = (rec_sec.size)['height']
        scroll = loc1
        driver.execute_script(f"scroll(0,{scroll - 400})")
        temp = rec_sec.find_element_by_xpath(
            './/button[text()[contains(.,"Received")]]')
        temp.click()
        findexpansions(Xrec_Sec, XexpandExp, driver, False)

    except Exception as e:
        pass

    try:
        recs = getElements(driver, Xrecommendation)
        full_recs = []
        for rec in recs:
            id = rec.get_attribute("id")
            loc = (rec.location)['y']
            size = (rec.size)['height']
            scroll = loc
            inc = 50
            while scroll < (loc + size):
                driver.execute_script(f"scroll(0,{scroll - 100})")
                try:
                    expand = getElement(rec, Xrecsee_more)
                    expand.click()
                    break
                except NoSuchElementException as e:
                    pass
                except ElementClickInterceptedException as e:
                    inc = inc + 25
                scroll = scroll + inc
            new_rec = driver.find_element_by_xpath(f'//li[@id="{id}"]')
            full_recs.append(new_rec)
        recs = full_recs
    except Exception as e:
        pass
        recs = None
    i = 0
    eles = []
    for x in recs:
        text = x.text.strip()
        if text != "":
            eles.append(processRec(x.text))
            i += 1
    data = ListToDic("rec", eles)
    return data


def addDict(dict1, dict2):
    for key in dict1.keys():
        dict2[key] = dict1[key]
    return dict2


def wait(a, b):
    secs = random.randint(a, b)
    pass
    time.sleep(secs)


def remove_unicode(txt):
    utf8string = txt.encode("utf-8")
    return utf8string.decode()

# FINAL STRUCTURED DATA PROVIDER METHODS ENDS HERE------------>

# SUMMERAIZER METHODS ENDS HERE------------>


# options.add_argument('--headless')
