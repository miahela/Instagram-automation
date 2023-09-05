from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

class SeleniumManager:
    def __init__(self, logger, web_driver_settings):
            self.logger = logger
            self.logger.info("Initializing Selenium driver...")
            
            options = Options()
            options.headless = web_driver_settings["headless"]
            options.add_extension("config/3.4.8_0.crx")
            options.add_argument(f"user-data-dir={web_driver_settings['user_data_path']}")
            options.add_argument('--disable-blink-features=AutomationControlled')

            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()

            self.wait = WebDriverWait(self.driver, web_driver_settings["wait_time"])
            
            self.logger.info("Selenium driver initialized successfully!")

    def quit(self):
        self.driver.quit()
        self.logger.info("Selenium driver closed successfully!")

    def get_driver(self):
        return self.driver
     
    def click_element(self, xpath):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def fill_field(self, xpath, data):
        field = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        field.send_keys(data)
        field.send_keys(Keys.ENTER)
        
    def upload_file(self, xpath, file_path):
        file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        file_input.send_keys(file_path)
        ActionChains(self.driver).key_down(Keys.ENTER).perform()

    def open_link(self, href):
        try:
            self.driver.get(href)
        except Exception as e:
            self.logger.error(f"Error opening link: {e}")

    def get_elements(self, xpath):
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return self.driver.find_elements(By.XPATH, xpath)


    def get_element(self, xpath):
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element(By.XPATH, xpath)
