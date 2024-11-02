
import platform
import time
import os
import json
from webDriverLib import WebDriverLibrary, ConfigReader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


reconQuest = 0
decoyQuest = 1
eyesQuest = 0
surfaceQuest = 0

# Đường dẫn đến ChromeDriver và profile Chrome
target_url = "https://mail.google.com/mail/u/0/#inbox"  # Thay đổi URL này thành trang web bạn muốn điều hướng đến

# Đường dẫn đến file cấu hình JSON
config_path = "config.json"

# Đọc cấu hình từ file JSON
config = ConfigReader.read_config(config_path)

# Get the current user's home directory
home_dir = os.path.expanduser("~")
username = os.path.basename(home_dir)

# Replace the placeholder with the actual username
config['chrome_profile_path'] = config['chrome_profile_path'].replace('{username}', username)

#time to wait for action
timeWait = config["timeWait"]

# Khởi tạo đối tượng WebDriverLibrary
os_name = platform.system()
if (os_name == "Windows"):
    driver = WebDriverLibrary(config['path_Chrome_window'], config['profile_path_windows'])
else:
    driver = WebDriverLibrary(config['path_chrome_driver'], config['chrome_profile_path'])
time.sleep(timeWait)

# Mở trang web
print ("open wwebsite")
driver.open_website(config["target_url"])

# $5 - $9
if reconQuest == 1:
    stlosAmount = "17"
    wUskAmount = "6.25956"
    verifyBtn = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[1]/div[3]/div[2]/div/button[1]"
# $10 - $19
elif decoyQuest == 1:
    stlosAmount = "40"
    wUskAmount = "13.7"
    verifyBtn = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div[1]/div[3]/div[2]/div/button[1]"
# $20 - $49
elif eyesQuest == 1:
    stlosAmount = "70"
    wUskAmount = "23.97"
    verifyBtn = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div/div[3]/div/div[1]/div[3]/div[2]/div/button[1]"
# $50 - $99
elif surfaceQuest == 1:
    stlosAmount = "180"
    wUskAmount = "61.5962"
    verifyBtn = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div/div[4]/div/div[1]/div[3]/div[2]/div/button[1]"


def click_and_wait(xpath, wait_time, description, timeout=10):
    try:
        element = driver.wait_for_element(By.XPATH, xpath, timeout=timeout)
        element.click()
        print(f"{description} clicked")
        time.sleep(wait_time)
    except Exception as e:
        print(f"Error clicking {description}: {e}")


click_and_wait(config["connectWallet"], timeWait, "Connect Wallet button")
click_and_wait(config["metaMask"], timeWait, "MetaMask button")

if (driver.get_number_of_windows() > 1):
    current_window_handle = driver.driver.current_window_handle
    driver.get_title_of_all_windows()
    try:
        driver.switch_to_window(1)
        windowMetamask = driver.driver.current_window_handle
        time.sleep(timeWait)
        print("Switched to MetaMask window")

        password = driver.wait_for_element(By.ID, config["passwordId"])
        password.send_keys(config["passMetamask"])
        print("Password entered")
        time.sleep(timeWait)

        click_and_wait(config["unlockBtn"], timeWait, "Unlock button")

        if driver.get_number_of_windows() > 1:
            click_and_wait(config["nextBtn"], timeWait, "Next button")
            click_and_wait(config["confirmBtn"], timeWait, "Confirm button")
        else:
                print("MetaMask window closed before completing actions")
                
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print ("close metamask window")
        try:
            driver.close_window()
        except Exception as e:
            print ("close metamask window closed before completing actions")
        driver.switch_to_window(1)
        driver.close_window()
        print("close MetaMask Offscreen window ")
        print("Switched back to main window")
        driver.switch_to_window(0)
else:
    print("MetaMask window not found")

try:
    click_and_wait(config["signinBtn"], timeWait, "Signin button", timeout=1)

    if (driver.get_number_of_windows() > 1):
        driver.switch_to_window(1)
        button = driver.wait_for_element(By.XPATH, '//button[text()="Confirm"]',timeout=1)
        button.click()
        time.sleep(timeWait)
        driver.close_window()
        driver.switch_to_window(0)
    else:
        print("not need confirmed")
except Exception as e:
    print(f"An error occurred: {e}")
    print ("not need sign in")
    
click_and_wait(config["avatarBtn"], timeWait, "Avatar button")
click_and_wait(config["questBtn"], timeWait, "Quest button")
click_and_wait(config["partnerBtn"], timeWait, "Partner button")

x = 100
y = 200
driver.click_at_coordinates(x, y)

# Modified $SELECTION_PLACEHOLDER$ code
click_and_wait(config["kumaBtn"], timeWait, "Kuma button")

tekika_window = driver.driver.current_window_handle

click_and_wait(config["startQuestBtn"], timeWait, "Start Quest button")

print(driver.get_number_of_windows())
driver.get_title_of_all_windows()
driver.switch_to_window(1)
print("Switched to task window")
time.sleep(timeWait)

# Get the task window handle
task_window = driver.driver.current_window_handle

# Click the dropdown and select the option
xpath2 = "/html/body/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[3]/div/div[1]/div/div/div/div[2]"
xpath1 = "/html/body/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div[2]"
element = driver.wait_for_element(By.XPATH, xpath1)
text1 = element.text
print("Element found:", element)
print("Element text:", element.text)

element = driver.wait_for_element(By.XPATH, xpath2)
print("Element found:", element)
print("Element text:", element.text)
text2 = element.text


# Wait for Metamask pop-up window to appear
def wait_for_metamask_popup():
    all_windows = driver.driver.window_handles

    # Wait until the number of windows increases
    while len(all_windows) == 2:
        time.sleep(1)
        all_windows = driver.driver.window_handles

    # Switch to the new window
    for window in all_windows:
        if window != task_window and window != tekika_window:
            print(">> Metamask popup")
            driver.driver.switch_to.window(window)
            time.sleep(timeWait)
            print(">> Switched to Metamask window")
            break

def metamask_proc(driver, config, task_window, timeWait, coin="STLOS", maxAmount="60", inputBox=""):
    try:
        if coin == "STLOS":
            # time.sleep(10000)
            element = driver.wait_for_element(By.XPATH, inputBox)
            element.click()
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(maxAmount + Keys.ENTER)
            print (">> 1. Max entered: " + maxAmount)
            time.sleep(timeWait)
        else:
            element = driver.wait_for_element_to_be_clickable(
                By.XPATH, config["max2Btn"])
            element.click()
            print(">> 1. Max out: done")
            time.sleep(timeWait)

        element = driver.wait_for_element_to_be_clickable(
            By.XPATH, config["nextBtn2"])
        element.click()
        print(">> 2. Next: done")
        time.sleep(timeWait)

        element = driver.wait_for_element_to_be_clickable(
            By.XPATH, config["approveBtnWUSK"])
        element.click()
        print(">> 3. Approve: done")
        time.sleep(timeWait)

        # Ensure to switch back to task window
        driver.driver.switch_to.window(task_window)
        time.sleep(timeWait)

        print("> Back to task window")
        element = driver.wait_for_element_to_be_clickable(
            By.XPATH, config["confirmSwapBtn"])
        element.click()
        print("> Confirm Swap: done")
        time.sleep(timeWait)

        wait_for_metamask_popup()
    except Exception as e:
        print(">> max2Btn not found:", e)

# clic`k dropdown and select option
def swap_token(coin1, coin2, numberCoin=25, nCount=2):
    xpath2 = "/html/body/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[3]/div/div[1]/div/div/div/div[2]"
    xpath1 = "/html/body/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div[2]"
    
    swapBTN = "/html/body/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div[1]"
    
    element = driver.wait_for_element(By.XPATH, xpath1)
    text1 = element.text
    # print("Element found:", element)
    print("Element text:", element.text)

    element = driver.wait_for_element(By.XPATH, xpath2)
    # print("Element found:", element)
    print("Element text:", element.text)
    text2 = element.text
    
    if (nCount == 1):
        if (text1 !=  coin1):    
            driver.click_dropdown_and_select_option_by_XPATH(config["dropDownAboveBtn"], coin1)
            time.sleep(timeWait)


        # Let update text2 after select coin1
        element = driver.wait_for_element(By.XPATH, xpath2)
        print("Update text2 after select coin 1:", element.text)
        text2 = element.text

        if (text2 != coin2):
            driver.click_dropdown_and_select_option_by_XPATH(config["dropDownBelowBtn"], coin2)
            time.sleep(timeWait)
            
         
    else:
        click_and_wait(swapBTN, timeWait, "Swap button")
        text1 = coin1
        text2 = coin2

    print("Pair: ", text1 + " " + text2)

    # enter input for token
    inputElement = "/html/body/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div[1]/input"
    inputBox = "/html/body/div[1]/div/div/div/div[7]/div/div[2]/input"
    
    for i in range(0,5,1):
        if (text1 == coin1 and text2 == coin2):
            if(coin1 == "STLOS"):
                element = driver.wait_for_element(By.XPATH, inputElement)
                # print ("Element found:", element)
                element.send_keys(numberCoin + Keys.ENTER)
                print ("> Source entered: " + numberCoin)
                time.sleep(timeWait)
            else:
                element = driver.wait_for_element_to_be_clickable(By.XPATH, config["maxBtn"])
                element.click()
                print("> Max button clicked")
                time.sleep(timeWait)
                
            element = driver.wait_for_element_to_be_clickable(By.XPATH, config["previewBtn"])
            
            if (element):
                element.click()
                print("> Preview button clicked")
                time.sleep(timeWait)
                break
            else:
                driver.reload_page()
                print("> Preview button not found, reload page, try again time: %d", i)
                
    if (coin1 == "STLOS"):
        element = driver.wait_for_element_to_be_clickable(By.XPATH, config["confirmSwapBtn"])
        element.click()
        print("> Confirm Swap: done")
        time.sleep(timeWait)
        
        wait_for_metamask_popup()
        metamask_proc(driver, config, task_window, timeWait, "STLOS", numberCoin, inputBox)
        
        element = driver.wait_for_element_to_be_clickable(By.XPATH, config["confirmAgainBtn"])
        element.click()
        print(">> Confirm Again button clicked")
        time.sleep(timeWait)
    else:
        element = driver.wait_for_element_to_be_clickable(By.XPATH, config["approveBtn"])
        element.click()
        print("Approve button clicked")

        wait_for_metamask_popup()
        metamask_proc(driver, config, task_window, timeWait, "wUSK")
        
        element = driver.wait_for_element_to_be_clickable(By.XPATH, config["confirmAgainBtn"])
        element.click()
        print("Confirm Again button clicked")
        time.sleep(timeWait)
        
def verify_task(btn):
    button = driver.wait_for_element(By.XPATH, btn)
    button.click()
    print("Verify clicked")
    time.sleep(timeWait)

nCount = 1

for iii in range(89):
    swap_token("STLOS", "wUSK", stlosAmount, nCount)
    time.sleep(20)
    nCount = 2
    driver.driver.switch_to.window(task_window)
    swap_token("wUSK", "STLOS", wUskAmount, nCount)
    time.sleep(15)
    driver.driver.switch_to.window(tekika_window)
    verify_task(verifyBtn)
    driver.driver.switch_to.window(task_window)
    time.sleep(3)


time.sleep(10000)
# Ví dụ sử dụng hàm wait_for_element để chờ đợi một phần tử xuất hiện
#element = driver.wait_for_element(By.XPATH, '//*[@id="example-element-id"]')
# print("Element found:", element)

# Đóng trình duyệt sau khi hoàn thành
# driver.quit_driver()
