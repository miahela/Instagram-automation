from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


class SeleniumManager:
    def __init__(self, logger, wait_time=20, headless=False, proxy_settings=None):
        self.logger = logger
        options = Options()
        options.headless = headless
        
        if proxy_settings:
            proxy_str = f"{proxy_settings['ip']}:{proxy_settings['port']}"
            options.add_argument(f"--proxy-server={proxy_str}")

        # Uncomment the line below if the Chrome executable is not in your system's path
        # options.binary_location = "path/to/chrome"
        
        caps = DesiredCapabilities.CHROME

        self.driver = webdriver.Chrome(chrome_options=options, desired_capabilities=caps)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, wait_time)


    def quit(self):
        self.driver.quit()
        self.logger.info("Selenium driver closed successfully!")

    def get_driver(self):
        return self.driver

    def setup_proxy(self, proxy_settings):
        try:
            my_proxy = f"{proxy_settings['ip']}:{proxy_settings['port']}"
            webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy": my_proxy,
                "ftpProxy": my_proxy,
                "sslProxy": my_proxy,
                "noProxy": None,
                "proxyType": "MANUAL",
                "class": "org.openqa.selenium.Proxy",
                "autodetect": False
            }
            
            self.driver = webdriver.Chrome(desired_capabilities=webdriver.DesiredCapabilities.CHROME)
            
            self.logger.info("Proxy successfully set up!")
            return True
        except Exception as e:
            self.logger.error(f"Error in setting up proxy: {e}")
            return False

        
    def click_element(self, xpath):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except Exception as e:
            self.logger.error(f"Error clicking element {xpath}: {e}")

    def fill_field(self, xpath, data):
        try:
            field = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            field.send_keys(data)
            field.send_keys(Keys.ENTER)
        except Exception as e:
            self.logger.error(f"Error filling field: {e}")

    def open_link_new_tab(self, href):
        try:
            initial_tabs = len(self.driver.window_handles)
            self.driver.execute_script("window.open('%s', '_blank')" % href)
            WebDriverWait(self.driver, 10).until(
                lambda driver: len(driver.window_handles) > initial_tabs
            )
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as e:
            self.logger.error(f"Error opening link in new tab: {e}")

    def element_exists(self, xpath):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except Exception as e:
            self.logger.error(f"Error checking if element exists: {e}")
            return False

    def wait_until_url_changes(self, url):
        try:
            self.wait.until(EC.url_changes(url))
        except Exception as e:
            self.logger.error(f"Error waiting until url changes: {e}")

    def open_link(self, href):
        try:
            self.driver.get(href)
        except Exception as e:
            self.logger.error(f"Error opening link: {e}")

    def get_elements(self, xpath):
        try:
            return self.driver.find_elements(By.XPATH, xpath)
        except Exception as e:
            self.logger.error(f"Error getting elements: {e}")
