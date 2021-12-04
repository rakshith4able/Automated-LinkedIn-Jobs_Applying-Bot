from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from os import environ
import time


service = Service("C:\Development\chromedriver.exe");
driver = webdriver.Chrome(service=service)

driver.maximize_window()

driver.get(
    "https://www.linkedin.com/jobs/search/?f_AL=true&geoId=102713980&keywords=python%20intern&location=India")

time.sleep(2)
login_button = driver.find_element(By.CSS_SELECTOR, ".nav__button-secondary")

login_button.click()

time.sleep(2)
username_field = driver.find_element(By.NAME, "session_key")
password_field = driver.find_element(By.NAME, "session_password")

username_field.send_keys(environ["LM"])
password_field.send_keys(environ["LP"])

sign_in_btn = driver.find_element(By.CSS_SELECTOR, ".login__form_action_container  button")
sign_in_btn.click()

time.sleep(2)

hide_chat_btn = driver.find_elements(By.CSS_SELECTOR, ".msg-overlay-bubble-header__controls button")[2]
hide_chat_btn.click()

all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

for listing in all_listings:
    print("called")
    listing.click()
    time.sleep(2)

    # Try to locate the apply button, if can't locate then skip the job.
    try:
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button--top-card button")
        apply_button.click()
        time.sleep(2)

        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")

        # If the submit_button is a "Next" button, then this is a multi-step application, so skip.
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()
            time.sleep(2)
            discard_button = driver.find_elements(By.CSS_SELECTOR, ".artdeco-modal__actionbar--confirm-dialog button")[
                1]
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else:
            submit_button.click()

        # Once application completed, close the pop-up window.
        time.sleep(2)
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()


    # If already applied to job or job is no longer accepting applications, then skip.
    except NoSuchElementException:
        print("No application button, skipped.")
        continue
time.sleep(2)
driver.quit()
