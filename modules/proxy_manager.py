from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

def setup_proxy(driver, proxy_settings):
    try:
        my_proxy = f"{proxy_settings['ip']}:{proxy_settings['port']}"
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': my_proxy,
            'sslProxy': my_proxy,
            'ftpProxy': my_proxy,
            'noProxy': ''
        })
        proxy.add_to_capabilities(driver.capabilities)
        
        # WebDriver does not natively support proxy authentication
        # You may need to find a service-specific workaround for this part
        # The following line is just a placeholder:
        # driver.get(f"http://{proxy_settings['username']}:{proxy_settings['password']}@{proxy_settings['ip']}:{proxy_settings['port']}")
        
        return True
    except Exception as e:
        print(f"Error in setting up proxy: {e}")
        return False
