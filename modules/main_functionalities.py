import time
import json
from selenium.webdriver.common.by import By
from modules.selenium_manager import SeleniumManager
from modules.helpers import setup_logger, read_json_file

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
                time.sleep(CONFIG["load_wait_time"])
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

        self.skip_not_now()

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

    def manage_messages(self, if_requests):
        try:
            list_items = self.selenium_manager.get_elements("//*[@role='listitem']")
            for list_item in list_items:

                is_hidden_text = list_item.find_element(By.XPATH, ".//span").text
                if 'Hidden Requests' in is_hidden_text:
                    logger.info("Skipping hidden requests")
                    continue

                try:
                    list_item.click()
                    time.sleep(CONFIG["load_wait_time"])
                    self.message_actions(CONFIG["instagram"], if_requests)
                except Exception as e:
                    logger.error(f"Error loading a message: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error opening messages: {e}")
            self.selenium_manager.quit()
            exit()

    def message_actions(self, data, if_requests):
        if if_requests:
            self.selenium_manager.click_element("//*[text()='Accept']")
        for message in data["messages"]:
            self.send_text_message(message)
        for file_path in data["photos"]:
            self.upload_file(file_path)
            self.send_text_message(" ")
        time.sleep(CONFIG["load_wait_time"])

    def send_text_message(self, message):
        time.sleep(CONFIG["load_wait_time"])
        try:
            self.selenium_manager.fill_field("//div[@role='textbox']", message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")

    def upload_file(self, file_path):
        try:
            self.selenium_manager.upload_file("//input[@type='file']", file_path)
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