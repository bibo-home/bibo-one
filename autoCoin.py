
import platform
import time
import os
import json
from webDriverLib import WebDriverLibrary, ConfigReader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


book1Quest = 1
book2Quest = 0

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

verify_basic_training_btn = config.get("verifyBasicTrainingBtn", "")
verify_unite_quest_btn = config.get("verifyUniteQuestBtn", "")
verify_enemy_quest_btn = config.get("verifyEnemyQuestBtn", "")
verify_victory_quest_btn = config.get("verifyVictoryQuestBtn", "")

if book1Quest == 1:
    tlosAmount = "100"
    slushAmount = "32"
    listVerifyBtns = [verify_basic_training_btn, verify_unite_quest_btn, verify_enemy_quest_btn]
elif book2Quest == 1:
    tlosAmount = "230"
    slushAmount = "56"
    listVerifyBtns = [verify_victory_quest_btn]
else:
    tlosAmount = "10"
    slushAmount = "5"
    listVerifyBtns = []



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


# connect wallet
button = connect_wallet_button = driver.wait_for_element(By.XPATH, config["connectWallet"])
print("Connect Wallet button found:", connect_wallet_button)

button.click()
print("Connect Wallet button clicked")
time.sleep(timeWait)

#click on metamask
button = driver.wait_for_element(By.XPATH, config["metaMask"])
print("MetaMask button found:", button)
button.click()
print("MetaMask button clicked")
time.sleep(timeWait)

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

        
        button = driver.wait_for_element(By.XPATH, config["unlockBtn"])
        button.click()
        print("Unlock button clicked")
        time.sleep(timeWait)

        if driver.get_number_of_windows() > 1:
            button = driver.wait_for_element(By.XPATH, config["nextBtn"])
            button.click()
            print("Next button clicked")
            time.sleep(timeWait)

            button = driver.wait_for_element(By.XPATH, config["confirmBtn"])
            button.click()
            print("Confirm button clicked")
            time.sleep(timeWait)
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
    print("linh")
    button = driver.wait_for_element(By.XPATH, config["signinBtn"],timeout=1)
    button.click()
    print("Signin button clicked")
    time.sleep(timeWait)

    tekika_window = driver.driver.current_window_handle
    
    all_windows = driver.driver.window_handles

    # Wait until the number of windows increases
    count = 0
    while len(all_windows) == 1 and count < 10:
        time.sleep(1)
        all_windows = driver.driver.window_handles
        count = count + 1

    # Switch to the new window
    for window in all_windows:
        if (window != tekika_window):
            print(">> Metamask popup")
            driver.driver.switch_to.window(window)
            time.sleep(timeWait)
            print(">> Switched to Metamask window")
            break
    
    
    signBtn_extra = "/html/body/div[1]/div/div/div/div/div[3]/button[2]"

    # button = driver.wait_for_element(By.XPATH, '//button[text()="Confirm"]',timeout=1)
    button = driver.wait_for_element(By.XPATH, signBtn_extra, timeout=1)
    button.click()
    time.sleep(timeWait)
    driver.switch_to_window(tekika_window)
    
except Exception as e:
    print(f"An error occurred: {e}")
    print ("not need sign in")

button = driver.wait_for_element(By.XPATH, config["avatarBtn"])
button.click()
print("Avatar button clicked")
time.sleep(timeWait)

button = driver.wait_for_element(By.XPATH, config["questBtn"])
button.click()
print("Quest button clicked")
time.sleep(timeWait)

button = driver.wait_for_element(By.XPATH, config["partnerBtn"])
button.click()
print("Partner button clicked")
time.sleep(timeWait)

x = 100
y = 200
driver.click_at_coordinates(x, y)


button = driver.wait_for_element(By.XPATH, config["swapCircleBtn"])
button.click()
print("Swapcircle button clicked")
time.sleep(timeWait)

tekika_window = driver.driver.current_window_handle

button = driver.wait_for_element(By.XPATH, config["startVictoryQuestBtn"])
button.click()
print("Start Quest button clicked")
time.sleep(timeWait)

print(driver.get_number_of_windows())
driver.get_title_of_all_windows()
driver.switch_to_window(1)
print("Switched to task window")
time.sleep(timeWait)

# Get the task window handle
task_window = driver.driver.current_window_handle
 
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

def metamask_proc(driver, config, task_window, timeWait, coin="TLOS", maxAmount="250", inputBox=""):
    try:
        if coin == "TLOS":
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
            By.XPATH, config["approveBtnSLUSH"])
        element.click()
        print(">> 3. Approve: done")
        time.sleep(timeWait)

        # Ensure to switch back to task window
        driver.driver.switch_to.window(task_window)
        time.sleep(timeWait)

        print("> Back to task window")
        element = driver.wait_for_element_to_be_clickable(
            By.XPATH, config["swapTokenToTokenBtn"])
        element.click()
        print("> Confirm Swap: done")
        time.sleep(timeWait)

        wait_for_metamask_popup()
    except Exception as e:
        print(">> max2Btn not found:", e)

# clic`k dropdown and select option
def swap_token(coin1, coin2, numberCoin="25", nCount=2):
    sourceToken = "/html/body/div/main/div/main/div[3]/div/div/div[2]/div[1]/div[2]/div/div[1]/button"
    destToken = "/html/body/div/main/div/main/div[3]/div/div/div[2]/div[1]/div[3]/div/div[1]/button"
    element = driver.wait_for_element(By.XPATH, sourceToken)
    srcText = element.find_element(By.TAG_NAME, "h3").text

    element = driver.wait_for_element(By.XPATH, destToken)
    destText = element.find_element(By.TAG_NAME, "h3").text
    
    swapBTN = "/html/body/div/main/div/main/div[3]/div/div/div[2]/div[1]/button"
    slushToken = "/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/button[7]"
    
    
    if (nCount == 1):
        if (srcText !=  coin1):    
            driver.click_dropdown_and_select_option_by_XPATH(sourceToken, coin1)
            time.sleep(timeWait)

        if (destText != coin2):
            element = driver.wait_for_element(By.XPATH, destToken)
            element.click()
            print("Destination token clicked")
            time.sleep(timeWait)
            
            element = driver.wait_for_element(By.XPATH, slushToken)
            element.click()
            print("Choose SLUSH token")
            time.sleep(timeWait)
        element = driver.wait_for_element(By.XPATH, sourceToken)
        srcText = element.find_element(By.TAG_NAME, "h3").text

        element = driver.wait_for_element(By.XPATH, destToken)
        destText = element.find_element(By.TAG_NAME, "h3").text
        
    else:
        element = driver.wait_for_element(By.XPATH, swapBTN)
        element.click()
        print("Swap clicked successfully")
        
        element = driver.wait_for_element(By.XPATH, sourceToken)
        srcText = element.find_element(By.TAG_NAME, "h3").text

        element = driver.wait_for_element(By.XPATH, destToken)
        destText = element.find_element(By.TAG_NAME, "h3").text

    print("Pair: ", srcText + " " + destText)

    # enter input for token
    inputElement = "/html/body/div/main/div/main/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/input"
    inputBox = "/html/body/div[1]/div/div/div/div[7]/div/div[2]/input"
    

    if (srcText == coin1 and destText == coin2):
        if(coin1 == "TLOS"):
            element = driver.wait_for_element(By.XPATH, inputElement)
            element.send_keys(numberCoin + Keys.ENTER)
            print ("> Source entered: " + numberCoin)
            time.sleep(timeWait)
        else:
            element = driver.wait_for_element_to_be_clickable(By.XPATH, config["maxBtn"])
            element.click()
            print("> Max button clicked")
            time.sleep(timeWait)
            
        #element = driver.wait_for_element_to_be_clickable(By.XPATH, config["previewBtn"])
                
    if (coin1 == "TLOS"):
        element = driver.wait_for_element_to_be_clickable(By.XPATH, config["swapTokenToTokenBtn"])
        time.sleep(timeWait)
        element.click()
        print("> Confirm Swap: done")
        time.sleep(timeWait)
        
        wait_for_metamask_popup()
        metamask_proc(driver, config, task_window, timeWait, "TLOS", numberCoin, inputBox)
        
        element = driver.wait_for_element_to_be_clickable(By.XPATH, config["confirmAgainBtn"])
        element.click()
        print(">> Confirm Again button clicked")
        time.sleep(timeWait)
    else:
        element = driver.wait_for_element_to_be_clickable(By.XPATH, config["approveSlushBtn"])
        element.click()
        print("Approve SLUSH button clicked")

        wait_for_metamask_popup()
        metamask_proc(driver, config, task_window, timeWait, "SLUSH")
        
        element = driver.wait_for_element_to_be_clickable(By.XPATH, config["confirmAgainBtn"])
        element.click()
        print("Confirm Again button clicked")
        time.sleep(timeWait)
        
def verify_task(listBtns):
    for btn in listBtns:
        button = driver.wait_for_element(By.XPATH, btn)
        button.click()
        print("Verify clicked")
        time.sleep(5)

nCount = 1

for i in range(0, 98, 1):
    swap_token("TLOS", "SLUSH", tlosAmount, nCount)
    time.sleep(10)
    #driver.driver.switch_to.window(tekika_window)
    #verify_task(listVerifyBtns)
    nCount = 2
    #time.sleep(3)
    driver.driver.switch_to.window(task_window)
    swap_token("SLUSH", "TLOS", slushAmount, nCount)
    time.sleep(10)
    driver.driver.switch_to.window(tekika_window)
    verify_task(listVerifyBtns)
    driver.driver.switch_to.window(task_window)
    time.sleep(3)


time.sleep(10000)
# Ví dụ sử dụng hàm wait_for_element để chờ đợi một phần tử xuất hiện
#element = driver.wait_for_element(By.XPATH, '//*[@id="example-element-id"]')
# print("Element found:", element)

# Đóng trình duyệt sau khi hoàn thành
# driver.quit_driver()
