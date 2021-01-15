import time
import sys
from selenium import webdriver
import scraper as sc
import json


def getUniqueId(link):
    words = link.split("https://www.linkedin.com/in/")
    word2 = words[1].split("/")
    return word2[0]


def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver


if __name__ == "__main__":
    # print(sys.argv[1])  # URL
    # print(sys.argv[2])  # ID
    # print(sys.argv[3])  # OD
    driver2 = create_driver_session(sys.argv[2], sys.argv[1])
    # print(f"Cr: {driver2.current_url}")
    if "feed" not in driver2.current_url and "https://www.linkedin.com/in/" not in driver2.current_url:
        raise Exception("You must be logged in.")
    od = sys.argv[3]
    prev = driver2.current_url

    # if "https://www.linkedin.com/in/" in driver2.current_url:
    #     # print(sc.getAbout(driver2))
    #     u_id = {
    #         getUniqueId(driver2.current_url): "pending"
    #     }
    #     print(json.dumps(u_id))
    #     sys.stdout.flush()
    #     time.sleep(2)
    #     intro = (sc.getIntro(driver2))
    #     about = (sc.getAbout(driver2))
    #     sys.stdout.flush()
    #     prev = driver2.current_url
    #     experience = (sc.getExp(driver2))
    #     recommendation = (sc.getRec(driver2))
    #     data = {
    #         "Link:": driver2.current_url,
    #         "Introduction": intro,
    #         "About": about,
    #         "Experience": experience,
    #         "Recommendations": recommendation
    #     }
    #     dire = od + '\\' + getUniqueId(driver2.current_url) + ".json"
    #     # print(dire)
    #     with open(dire, 'w') as outfile:
    #         json.dump(data, outfile, indent=4)
    #     u_id[getUniqueId(driver2.current_url)] = "completed"
    #     print(json.dumps(u_id))
    #     sys.stdout.flush()

    tabs = driver2.window_handles
    prev1=len(tabs)
    while True:
        tabs = driver2.window_handles
        #print(f"prev1 before check:{prev1}")
        if prev1!=len(tabs) :
            if prev1<=len(tabs):
                try:
                    driver2.switch_to_window(tabs[len(tabs)-1])
                    #print(f"prev1: {prev1}")
                    if "https://www.linkedin.com/in/" in driver2.current_url:

                     #   print(f"url : {driver2.current_url}")
                        u_id = {
                            getUniqueId(driver2.current_url): "pending"
                        }
                        print(json.dumps(u_id))
                        sys.stdout.flush()
                        time.sleep(2)
                        intro = (sc.getIntro(driver2))
                        about = (sc.getAbout(driver2))
                        sys.stdout.flush()
                        prev = driver2.current_url
                        experience = (sc.getExp(driver2))
                        recommendation = (sc.getRec(driver2))
                        data = {
                            "Link:": driver2.current_url,
                            "Introduction": intro,
                            "About": about,
                            "Experience": experience,
                            "Recommendations": recommendation
                        }
                        dire = od + '\\' + getUniqueId(driver2.current_url) + ".json"
                        # print(dire)
                        with open(dire, 'w') as outfile:
                            json.dump(data, outfile, indent=4)

                        u_id[getUniqueId(driver2.current_url)] = "completed"
                        print(json.dumps(u_id))
                        sys.stdout.flush()
                except:
                    pass

            prev1=len(tabs)

        time.sleep(1)
