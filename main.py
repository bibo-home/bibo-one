import platform
import time
import os
import json
from webDriverLib import WebDriverLibrary, ConfigReader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

book = 5
WTLOS_amount = "11"   # book 3 - manual input to match $1
TLOS_max = "90"
STLOS_max = "80"   # book 5 - manual input to match $10
WTLOS_max = "50"   # book 5 - manual input to match $10
USDT_max = "10"   # book 5 - manual input to match $10
SLUSH_max = "12"  # book 7 - manual input to match $5
loop_count = 0

# Store all window handles with their IDs
tekika_window = ""
symmetric_window = ""
metamask_window = ""
swapsicle_window = ""



special = False
refresh_now = False

# Verify buttons
book1_symm_quest_btn = "/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[4]/div/div[4]/div/div/div[2]/div[1]/div[3]/div/div/button"
book3_symm_quest_btn = "/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div/button"
book2_swc_quest_btn  = "/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div[1]/div[3]/div/div/button"
book5_symm_quest_btn = '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[7]/div/div/div[2]/div[1]/div[3]/div/div/button'
book7_swc_quest_btn  = '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[4]/div/div/div[2]/div[1]/div[3]/div/div/button'

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
time.sleep(5)

def enter_password(xpath, password):
    element = driver.wait_for_element(By.XPATH, xpath)
    element.send_keys(password)
    element.send_keys(Keys.ENTER)
    print("Password entered")


if (driver.get_number_of_windows() > 1):
    current_window_handle = driver.driver.current_window_handle
    driver.get_title_of_all_windows()
    try:
        driver.switch_to_window(1)
        windowMetamask = driver.driver.current_window_handle
        time.sleep(timeWait)
        print("Switched to MetaMask window")
        
        # Example usage:
        password_xpath = '//input[@aria-invalid="false" and @autocomplete="current-password" and @id="password" and @type="password" and @dir="auto" and @data-testid="unlock-password" and contains(@class, "MuiInputBase-input") and contains(@class, "MuiInput-input")]'
        enter_password(password_xpath, config["passMetamask"])
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


########
# Handle SYMMETRIC SWAP

def SYM_select_source_token(token_text):
    # Find and click the specified element
    src_token_button = driver.wait_for_element(By.XPATH, '//div[@class="token-select-input selected group selectable"]')
    src_token_text = src_token_button.find_element(By.XPATH, './/div[@class="flex items-center -mb-px text-base font-medium leading-none"]').text
    
    if src_token_text != token_text:
        src_token_button.click()
        print("> Source button clicked")
        
        # Find the input element, type the token text to search, and press enter
        search_input = driver.wait_for_element(By.XPATH, '//input[@type="text" and @name="tokenSearchInput" and @placeholder="Search by name, symbol or address"]')
        search_input.send_keys(token_text)
        search_input.send_keys(Keys.ENTER)
        print(f"> > {token_text} entered in search input")
    else:
        print(f"> > Source token is already {token_text}")

def SYM_select_target_token(token_text):
    # Find and click the specified element using the provided XPath
    target_token_button = driver.wait_for_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[3]/div/div[1]/div/div/div')
    target_token_text = target_token_button.find_element(By.XPATH, './/div[@class="flex items-center -mb-px text-base font-medium leading-none"]').text
    
    if target_token_text != token_text:
        target_token_button.click()
        print("> Target button clicked")
        
        # Find the input element, type the token text to search, and press enter
        search_input = driver.wait_for_element(By.XPATH, '//input[@type="text" and @name="tokenSearchInput" and @placeholder="Search by name, symbol or address"]')
        search_input.send_keys(token_text)
        search_input.send_keys(Keys.ENTER)
        print(f"> > {token_text} entered in search input")
    else:
        print(f"> > Target token is already {token_text}")

def SYM_enter_source_amount(amount):
    # Find the input field and enter the amount
    amount_input = driver.wait_for_element(By.XPATH, '//input[@type="number" and @name="tokenIn" and @placeholder="0.0"]')
    amount_input.click()
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.DELETE)
    amount_input.send_keys(str(amount))
    print(f"> Entered source amount: {amount}")

def SYM_enter_target_amount(amount):
    # Find the input field and enter the amount using the provided XPath
    amount_input = driver.wait_for_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[3]/div/div[1]/input')
    amount_input.click()
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.DELETE)
    amount_input.send_keys(str(amount))
    print(f"> Entered target amount: {amount}")

def SYM_click_preview_button():
    # Find and click the Preview button using the correct button element
    preview_button = driver.wait_for_element_to_be_clickable(By.XPATH, '//button[@class="bal-btn px-4 h-12 text-base  bg-gradient-to-tr from-blue-600 to-pink-600 hover:from-blue-700 hover:to-pink-700 transition-colors text-white border-none block w-full rounded-lg shadow hover:shadow-none cursor-pointer"]')
    preview_button.click()
    print("> Preview button clicked")


########
# Handle Metamask pop-up window
def SYM_click_confirm_swap_button():
    print("> Wait for confirm swap button to appear")
    global refresh_now
    try:
        confirm_swap_button = driver.wait_for_element_to_be_clickable(By.XPATH, '/html/body/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div/div/button', timeout = 30)
        confirm_swap_button.click()
        print("> Confirm Swap button clicked")
        refresh_now = False
    except:
        print("> Confirm Swap button did not appear, need to refresh")
        refresh_now = True

    

def metamask_confirm(maxAmount, task_window):
    global special
    # Wait for the MetaMask window to pop up, rechecking every 2 seconds, up to 3 times
    for _ in range(3):
        all_windows = driver.driver.window_handles
        
        if len(all_windows) > 2:
            for window in all_windows:
                if window != tekika_window and window != task_window:
                    driver.driver.switch_to.window(window)
                    print("> Switched to MetaMask window")
                    
                    time.sleep(2)
                    
                    # Find whether the MetaMask window is asking for allowance or confirmation
                    allowance_field = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div/div/div[7]/div/div[2]/input', timeout=2)
                    if allowance_field:
                        print("> > Allowance request")
                        allowance_field.click()
                        allowance_field.send_keys(Keys.CONTROL + "a")
                        allowance_field.send_keys(Keys.DELETE)
                        allowance_field.send_keys(maxAmount + Keys.ENTER)
                        print ("> > Max allowance entered: " + maxAmount)
                        
                        nxt_btn = driver.wait_for_element_to_be_clickable( 
                            By.XPATH, '/html/body/div[1]/div/div/div/div[10]/footer/button[2]')
                        nxt_btn.click()
                        print("> > Next: clicked")
                        time.sleep(1)

                        approved_btn = driver.wait_for_element_to_be_clickable(
                            By.XPATH, '/html/body/div[1]/div/div/div/div[11]/footer/button[2]')
                        approved_btn.click()
                        print("> > Approve: clicked")
                        time.sleep(1)
                        
                        special = True
                        
                        # Ensure to switch back to task window
                        driver.driver.switch_to.window(task_window)
                        time.sleep(timeWait)
                        
                        return
                    else:
                        print("> > Confirmation request")
                        # Wait for the confirm button to appear
                        for _ in range(10):
                            try:
                                confirm_button = driver.wait_for_element(
                                    By.XPATH, '/html/body/div[1]/div/div/div/div/div[3]/button[2]', timeout=2)
                                confirm_button.click()
                                print("> > Confirm button clicked")
                                special = False
                                
                                # Ensure to switch back to task window
                                driver.driver.switch_to.window(task_window)
                                time.sleep(timeWait)
                                
                                return
                            except:
                                time.sleep(2)
                        raise TimeoutError("> > Confirm button did not appear in MetaMask window")
        time.sleep(2)
    raise TimeoutError("> MetaMask window did not appear")

def SYM_swap_tokens(source, target, amount, fill_to = "source"):
    # Select the source token
    SYM_select_source_token(source)
    
    # Select the target token
    SYM_select_target_token(target)
    
    # Enter the source amount
    if fill_to == "target":
        SYM_enter_target_amount(amount)
    else:
        SYM_enter_source_amount(amount)
        
    time.sleep(1)
    
    global symmetric_window
    symmetric_window = driver.driver.current_window_handle
    
    # Click the Preview button
    SYM_click_preview_button()
    
    time.sleep(1)
    
    global refresh_now
    # Click the Confirm Swap button
    SYM_click_confirm_swap_button()
    
    # Special case STLOS - somehow it shows incorrect rate
    while (source == "STLOS" and refresh_now):
        print("> Refreshing the page")
        # Refresh the page and re-select the tokens and amounts
        driver.driver.refresh()
        SYM_select_source_token(source)
        SYM_select_target_token(target)
        SYM_enter_target_amount(amount)
        time.sleep(2)
        SYM_click_preview_button()
        time.sleep(1)
        SYM_click_confirm_swap_button()
    
    
    # Max allowance for tokens
    maxAmount = WTLOS_amount
    
    if source == "STLOS":
        maxAmount = STLOS_max
    elif source == "USDT":
        maxAmount = USDT_max
    elif source == "WTLOS":
        maxAmount = WTLOS_max
    elif source == "TLOS":
        maxAmount = TLOS_max
    else:
        print("> Special case: no allowance needed")
    
    # Confirm the MetaMask transaction
    metamask_confirm(maxAmount, symmetric_window)
    
    if special:
        # Then another confirm swap appears to click
        SYM_click_confirm_swap_button()
        metamask_confirm(maxAmount, symmetric_window)
        
    time.sleep(1)




###########
# Swapsicle

def SWC_select_source_token(token_text):
    if token_text == "WTLOS":
        token_id = '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/button[1]'
    else:
        token_id = '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/button[7]'  
         
    # Find and click the specified element
    src_token_button = driver.wait_for_element(By.XPATH, '/html/body/div/main/div/main/div[3]/div/div/div[2]/div[1]/div[2]/div/div[1]/button')
    src_token_text = src_token_button.find_element(By.XPATH, './/h3').text
    
    if src_token_text != token_text:
        src_token_button.click()
        print("> Source button clicked")
        
        # Find the input element, type the token text to search, and press enter
        selected_token = driver.wait_for_element(By.XPATH, token_id)
        selected_token.click()
        print(f"> > {token_text} selected")
    else:
        print(f"> > Source token is already {token_text}")
        
def SWC_select_target_token(token_text):
    if token_text == "WTLOS":
        token_id = '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/button[1]'
    else:
        token_id = '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/button[7]' 
        
    # Find and click the specified element using the provided XPath
    target_token_button = driver.wait_for_element(By.XPATH, '/html/body/div/main/div/main/div[3]/div/div/div[2]/div[1]/div[3]/div/div[1]/button')
    target_token_text = target_token_button.find_element(By.XPATH, './/h3').text
    
    if target_token_text != token_text:
        target_token_button.click()
        print("> Target button clicked")
        
        # Find the input element, type the token text to search, and press enter
        selected_token = driver.wait_for_element(By.XPATH, token_id)
        selected_token.click()
        print(f"> > {token_text} selected")
    else:
        print(f"> > Target token is already {token_text}")

def SWC_enter_source_amount(amount):
    # Find the input field and enter the amount
    amount_input = driver.wait_for_element(By.XPATH, '/html/body/div/main/div/main/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/input')
    amount_input.click()
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.DELETE)
    amount_input.send_keys(str(amount))
    print(f"> Entered source amount: {amount}")

def SWC_enter_target_amount(amount):
    # Find the input field and enter the amount using the provided XPath
    amount_input = driver.wait_for_element(By.XPATH, '/html/body/div/main/div/main/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/input')
    amount_input.click()
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.DELETE)
    amount_input.send_keys(str(amount))
    print(f"> Entered target amount: {amount}")
    
def SWC_click_swap_button():
    # Find and click the Preview button using the correct button element
    swap_now_button = driver.wait_for_element_to_be_clickable(By.XPATH, '/html/body/div/main/div/main/div[3]/div/div/div[2]/button', timeout=30)
    swap_now_button.click()
    print("> SWAP button clicked")

def SWC_swap_tokens(source, target, amount, fill_to = "source"):
    # Select the source token
    SWC_select_source_token(source)
    
    # Select the target token
    SWC_select_target_token(target)
    
    time.sleep(1)
    
    # Enter the source amount
    if fill_to == "target":
        SWC_enter_target_amount(amount)
    else:
        SWC_enter_source_amount(amount)
        
    time.sleep(1)
    
    global swapsicle_window
    swapsicle_window = driver.driver.current_window_handle
    
    
    try:
        print("> Try to approve the transaction")
        approve_button = driver.wait_for_element_to_be_clickable(By.XPATH, '/html/body/div/main/div/main/div[3]/div/div/div[2]/div[3]/button[1]', timeout=5)
        approve_button.click()
        print("> Approve button clicked")
        time.sleep(1)
        
        # Max allowance for tokens
        maxAmount = '10'
        if source == "WTLOS":
            maxAmount = WTLOS_max
        elif source == "SLUSH":
            maxAmount = SLUSH_max
        else:
            print("> Special case: no allowance needed")
        
        # Confirm the MetaMask transaction
        metamask_confirm(maxAmount, swapsicle_window)
        SWC_click_swap_button()
        metamask_confirm(maxAmount, swapsicle_window)
        time.sleep(1)
    except:
        print("> Approve button not found! Let's try swapping directly")
        SWC_click_swap_button()
        maxAmount = '10'
        metamask_confirm(maxAmount, swapsicle_window)
        time.sleep(1)
    
    
    

def verify_swap_quest(quest_window, button):
    # Switch back to the Tekika window
    driver.driver.switch_to.window(tekika_window)
    
    # Find and click the button with the specified class and SVG content
    svg_button = driver.wait_for_element(By.XPATH, button)
    svg_button.click()
    print("> Swaps Verified!")
    
    driver.driver.switch_to.window(quest_window)
    print("> Switched back to Quest window")

def update_swap_count():
    global swapped_num
    swapped_num = swapped_num + 2
    print(f"Swapped {swapped_num} times")
    report_field = driver.wait_for_element(By.CSS_SELECTOR, 'canvas[width="60"][height="60"][style*="border-radius: 100%"]')
    

def access_to_book(book):
    # Store initial windows
    global tekika_window
    tekika_window = driver.driver.current_window_handle
    
    button = driver.wait_for_element(By.CSS_SELECTOR, 'canvas[width="60"][height="60"][style*="border-radius: 100%"]')
    button.click()
    print("Avatar button with canvas clicked")
    
    # Find and click the "Quests" element
    quests_button = driver.wait_for_element(By.XPATH, '//p[@class="chakra-text css-22m1hb" and text()="Quests"]')
    quests_button.click()
    print("Quests button clicked")

    global loop_count

    if book == 1:
        # Find and click the "Book 1" element using full XPath
        book1_button = driver.wait_for_element(By.XPATH, '//p[text()="The Augmented"]')
        book1_button.click()
        print("Book 1: accessed")
        
        # Update swapped number
        report_field = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[4]/div/div[4]/div/div/div[2]/div[1]/div[2]/div/p')
        swapped_number = int(report_field.text.strip())
        print(f"Swapped number extracted: {swapped_number}")
        remaining_swaps = 1000 - swapped_number
        
        # Calculate the number of swaps to perform
        # loop_count = ceiling(remaining_swaps/2)
        if remaining_swaps % 2 == 0:
            loop_count = remaining_swaps//2
        else:
            loop_count = remaining_swaps//2 + 1
        
        # Find and click the "Start Quest" button
        start_quest_button = driver.wait_for_element(By.XPATH, '//p[text()="Start Quest"]')
        start_quest_button.click()
        print("Start Quest button clicked")
        
        # Switch to the new tab
        driver.switch_to_window(1)
        print("Switched to new tab")
        
    elif book == 2:
        # Find and click the "Book 2" element using full XPath
        book2_button = driver.wait_for_element(By.XPATH, '//p[text()="Do Your Homework"]')
        book2_button.click()
        print("Book 2: accessed")
        
        # Update swapped number
        report_field = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div[1]/div[2]/div/p')
        swapped_number = int(report_field.text.strip())
        print(f"Swapped number extracted: {swapped_number}")
        remaining_swaps = 1000 - swapped_number
        
        # Calculate the number of swaps to perform
        # loop_count = ceiling(remaining_swaps/2)
        if remaining_swaps % 2 == 0:
            loop_count = remaining_swaps//2
        else:
            loop_count = remaining_swaps//2 + 1
        
         # Find and click the "Start Quest" button
        start_quest_button = driver.wait_for_element(By.XPATH, '//p[text()="Start Quest"]')
        start_quest_button.click()
        print("Start Quest button clicked")
        
        # Switch to the new tab
        driver.switch_to_window(1)
        print("Switched to new tab")
    elif book == 3:
        # Find and click the "Book 3" element using full XPath
        book3_button = driver.wait_for_element(By.XPATH, '//p[text()="Across the planes"]')
        book3_button.click()
        print("Book 3: accessed")
        
        # Update swapped number
        report_field = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/div[2]/div[1]/div[2]/div/p')
        swapped_number = int(report_field.text.strip())
        print(f"Swapped number extracted: {swapped_number}")
        remaining_swaps = 1000 - swapped_number

        # Calculate the number of swaps to perform
        # loop_count = ceiling(remaining_swaps/2)
        if remaining_swaps % 2 == 0:
            loop_count = remaining_swaps//2
        else:
            loop_count = remaining_swaps//2 + 1
    
         # Find and click the "Start Quest" button
        start_quest_button = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div/div')
        start_quest_button.click()
        print("Start Quest button clicked")
        
        # Switch to the new tab
        driver.switch_to_window(1)
        print("Switched to new tab")
    elif book == 4:
        # Add code for accessing Book 4
        pass

    elif book == 5:
        # Find and click the "Book 3" element using full XPath
        book_button = driver.wait_for_element(By.XPATH, '//p[text()="The Belly Of The Beast"]')
        book_button.click()
        print("Book 5: accessed")
        
        # Update swapped number
        report_field = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[7]/div/div/div[2]/div[1]/div[2]/div/p')
        swapped_number = int(report_field.text.strip())
        print(f"Swapped number extracted: {swapped_number}")
        remaining_swaps = 1000 - swapped_number

        # Calculate the number of swaps to perform
        # loop_count = ceiling(remaining_swaps/2)
        if remaining_swaps % 2 == 0:
            loop_count = remaining_swaps//2
        else:
            loop_count = remaining_swaps//2 + 1
        
        
        start_quest_button = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[7]/div/div/div[2]/div[1]/div[3]/div/div/div')
        start_quest_button.click()
        print("Start Quest button clicked")
        
        # Switch to the new tab
        driver.switch_to_window(1)
        print("Switched to new tab") 
    elif book == 7:
        # Find and click the "Book 7" element using full XPath
        book_button = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[1]/div/div/div[7]/span/span/span[1]/div/div/div[2]/div')
        book_button.click()
        print("Book 7: accessed")
        
        # Update swapped number
        report_field = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[4]/div/div/div[2]/div[1]/div[2]/div/p')
        swapped_number = int(report_field.text.strip())
        print(f"Swapped number extracted: {swapped_number}")
        remaining_swaps = 1000 - swapped_number

        # Calculate the number of swaps to perform
        # loop_count = ceiling(remaining_swaps/2)
        if remaining_swaps % 2 == 0:
            loop_count = remaining_swaps//2
        else:
            loop_count = remaining_swaps//2 + 1
        
        
        start_quest_button = driver.wait_for_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div/div[3]/div/div[4]/div/div/div[2]/div[1]/div[3]/div/div/div')
        start_quest_button.click()
        print("Start Quest button clicked")
        
        # Switch to the new tab
        driver.switch_to_window(1)
        print("Switched to new tab") 
    else:
        print("Invalid book number")



########
# Main flow

access_to_book(book)

if book == 1:
    for i in range(loop_count):
        print(f"Swap {i + 1} / {loop_count}")
        SYM_swap_tokens("USDT", "WTLOS", 1, "source")
        time.sleep(5)
        SYM_swap_tokens("WTLOS", "USDT", 1, "target")
        time.sleep(5)
        verify_swap_quest(symmetric_window, book1_symm_quest_btn)
        print("")
elif book == 3:
    for i in range(loop_count):
        print(f"Swap {i + 1} / {loop_count}")
        SYM_swap_tokens("WTLOS", "STLOS", WTLOS_amount, "source")
        time.sleep(5)
        SYM_swap_tokens("STLOS", "WTLOS", WTLOS_amount, "target")
        time.sleep(5)
        verify_swap_quest(symmetric_window, book3_symm_quest_btn)
        print("")
elif book == 2:
    for i in range(loop_count):
        print(f"Swap {i + 1} / {loop_count}")
        SWC_swap_tokens("WTLOS", "SLUSH", 2.0, "target")
        time.sleep(5)
        SWC_swap_tokens("SLUSH", "WTLOS", 2.0, "source")
        time.sleep(5)
        verify_swap_quest(swapsicle_window, book2_swc_quest_btn)
        print("")
elif book == 5:
    for i in range(loop_count):
        print(f"Swap {i + 1} / {loop_count}")
        SYM_swap_tokens("TLOS", "USDT", 10, "target")
        time.sleep(5)
        SYM_swap_tokens("USDT", "TLOS", 10, "source")
        time.sleep(5)
        verify_swap_quest(symmetric_window, book5_symm_quest_btn)
        print("")
elif book == 7:
    for i in range(loop_count):
        print(f"Swap {i + 1} / {loop_count}")
        SWC_swap_tokens("WTLOS", "SLUSH", 12, "target")
        time.sleep(5)
        SWC_swap_tokens("SLUSH", "WTLOS", 12, "source")
        time.sleep(5)
        verify_swap_quest(swapsicle_window, book7_swc_quest_btn)
        print("")
time.sleep(100000)

