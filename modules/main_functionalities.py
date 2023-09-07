import time
import json
from selenium.webdriver.common.by import By
from modules.selenium_manager import SeleniumManager
from modules.helpers import setup_logger, read_json_file
import emoji

CONFIG = read_json_file("./config/settings.json")
logger = setup_logger()

class MainApp:
    def __init__(self):
        self.selenium_manager = SeleniumManager(logger, CONFIG["web_driver"])
        self.driver = self.selenium_manager.open_link("https://www.google.com/")
        time.sleep(CONFIG["load_wait_time"])

    def change_ip(self):
        self.selenium_manager.open_link("chrome-extension://hnmpcagpplmpfojmgmnngilcnanddlhb/popup.html")
        try:
            self.selenium_manager.click_element("//button[@aria-label='Locations']")
            self.selenium_manager.click_element(f"//*[text()='{CONFIG['instagram']['country_name']}']")
            self.selenium_manager.click_element("//a/following-sibling::div[1]")
            time.sleep(CONFIG["load_wait_time"])
            self.selenium_manager.click_element("//button[@aria-label='Locations']")
            self.selenium_manager.click_element(f"//*[text()='{CONFIG['instagram']['country_name']}']")
        except Exception as e:
            logger.error(f"Error changing IP: {e}")
            self.selenium_manager.quit()
            exit()
        
    def check_ip(self, recursive=False):
        self.selenium_manager.open_link("https://ipinfo.io/json")
        try:
            body_text = self.selenium_manager.get_element("//body").text
        except Exception as e:
            logger.error(f"Error getting IP: {e}")
            self.selenium_manager.quit()
            exit()
        json_response = json.loads(body_text)
        if json_response['country'] != CONFIG["instagram"]["country_code"]:
            logger.info(f"Country is: {json_response['country']} - Trying Changing IP to {CONFIG['instagram']['country_name']}")
            if not recursive:
                self.change_ip()
                time.sleep(10)
                self.check_ip(recursive=True)
            else:
                logger.error("IP is still not correct, idk why, exiting...")
            self.selenium_manager.quit()
            exit()
        logger.info("IP is correct")
        
    def instagram_login(self):
        time.sleep(CONFIG["load_wait_time"])
        self.allow_cookies()
        try:
            self.selenium_manager.fill_field("//input[@name='username']", CONFIG["instagram"]["username"])
            self.selenium_manager.fill_field("//input[@name='password']", CONFIG["instagram"]["password"])
        except Exception as e:
            logger.error(f"Error logging in: {e}")
            self.selenium_manager.quit()
            exit()

        logger.info("Logged in successfully!")

    def allow_cookies(self):
        try:
            self.selenium_manager.click_element("//button[text()='Allow all cookies']")
        except:
            pass

    def navigate_to_messages(self):
        try:
            self.selenium_manager.click_element("//*[text()='Messages']")
            time.sleep(CONFIG["load_wait_time"]) # Wait for messages to load
        except Exception as e:
            logger.error(f"Error navigating to messages: {e}")
            self.selenium_manager.quit()
            exit()
        logger.info("Navigated to messages successfully!")

    def skip_not_now(self):
        try:
            self.selenium_manager.click_element("//button[text()='Not Now']")
        except:
            pass

    def navigate_to_requests(self):
        try:
            self.selenium_manager.click_element("//*[contains(text(), 'Request')]")
            logger.info("Navigated to requests successfully!")
            time.sleep(CONFIG["load_wait_time"]) # Wait for messages to load
            return True
        except Exception as e:
            logger.error(f"Error navigating to requests: {e}")
            self.selenium_manager.quit()
            exit()

    def manage_requests(self):
        counter = 0
        logger.info("Managing requests...")
        while True:
            try:
                message = self.selenium_manager.get_element("//div[@role='listitem']")
            except Exception as get_element_error:
                logger.error(f"Error getting list item: {get_element_error}")

            is_hidden_text = None
            try:
                is_hidden_text = message.find_element(By.XPATH, ".//span").text
            except Exception as find_element_error:
                logger.warning("No span element found in the list item.")

            if is_hidden_text and 'Hidden Requests' in is_hidden_text:
                logger.info("Skipping hidden requests")
                break

            try:
                message.click()
                time.sleep(CONFIG["load_wait_time"])
            except Exception as click_error:
                logger.error(f"Error clicking the list item: {click_error}")
                continue

            self.message_actions(CONFIG["instagram"], True)
            counter += 1
        logger.info(f"Managed {counter} requests successfully!")    

    def manage_messages(self, if_requests):        
        if if_requests:
            self.manage_requests()
        else:
            try:
                list_items = self.selenium_manager.get_elements("//*[@role='listitem']")
            except Exception as get_elements_error:
                logger.error(f"Error getting messages: {get_elements_error}")
                self.selenium_manager.quit()
                exit()
            for list_item in list_items:
                try:
                    list_item.click()
                    time.sleep(CONFIG["load_wait_time"])
                except Exception as click_error:
                    logger.error(f"Error clicking the list item: {click_error}")
                    continue

                self.message_actions(CONFIG["instagram"], if_requests)

    def message_actions(self, data, if_requests):
        time.sleep(CONFIG["load_wait_time"])
        if if_requests:
            try:
                self.selenium_manager.click_element("//*[text()='Accept']")
            except Exception as e: 
                logger.error(f"Failed to click 'Accept': {e}")
            
            try:
                self.selenium_manager.click_element("//*[text()='Primary']")
            except Exception as e:  
                logger.error(f"Failed to click 'Primary': {e}")

        time.sleep(CONFIG["load_wait_time"])
        for message in data.get("messages", []):  
            self.send_text_message(message)

        for file_path in data.get("photos", []):  
            self.upload_file(file_path)

        time.sleep(CONFIG["load_wait_time"])

    def send_text_message(self, message):
        try:
            self.selenium_manager.fill_field("//div[@role='textbox']",  emoji.emojize("😉"))
            time.sleep(CONFIG["load_wait_time"])
        except Exception as e:
            logger.error(f"Error sending message: {e}")

    def upload_file(self, file_path):
        try:
            self.selenium_manager.upload_file("//input[@type='file']", file_path)
            time.sleep(CONFIG["load_wait_time"])
            self.send_text_message(" ")
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            print(e)

    def logout(self):
        try:
            self.selenium_manager.click_element("//*[@aria-label='Settings']")
            self.selenium_manager.click_element("//*[text()='Log out']")
            logger.info("Logged out successfully!")
        except Exception as e:
            logger.error(f"Error logging out, probably already logged out tho :D")