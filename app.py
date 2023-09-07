from modules.main_functionalities import MainApp
import time

if __name__ == "__main__":
    main_app = MainApp()
    # time.sleep(15)
    # main_app.check_ip()
    main_app.selenium_manager.open_link("https://www.instagram.com/")
    # main_app.logout()
    # main_app.instagram_login()
    # main_app.skip_not_now()
    main_app.navigate_to_messages()
    managing_requests = False
    # managing_requests = main_app.navigate_to_requests() # Ako sakas da go koristis za replies na obicni poraki, samo iskomentiraj ja ova linija
    main_app.manage_messages(managing_requests) 
    # main_app.logout()
    main_app.selenium_manager.quit()
