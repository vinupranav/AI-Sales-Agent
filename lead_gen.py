import re
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# HubSpot OAuth Token
hubspot_api_token = ''

# website to scrape
website = ""
# chromedriver path
chrome_driver_path = 

# Function to add contact to HubSpot
def add_contact_to_hubspot(first_name, last_name, job_title, company_name, email, phone_number):
    url = "https://api.hubapi.com/contacts/v1/contact"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hubspot_api_token}"
    }
    data = {
        "properties": [
            {"property": "firstname", "value": first_name},
            {"property": "lastname", "value": last_name},
            {"property": "jobtitle", "value": job_title},
            {"property": "company", "value": company_name},
            {"property": "email", "value": email},
            {"property": "phone", "value": phone_number}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.status_code, response.text


# Set up Chrome driver initialisation
def initialise_driver(chrome_driver_path):
    chrome_options = Options()
    user_data_dir = r'C:\Users\TUFF\AppData\Local\Google\Chrome\User Data\Default'  # mac path
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_driver_path = chrome_driver_path
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Function to find email addresses in the page source
def find_email_address(page_source):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, page_source)


# Function to filter out unwanted email domains
def filter_emails(emails, excluded_domain):
    filtered = [email for email in emails if not email.endswith(excluded_domain)]
    return filtered[:2]


# Function to split name into first and last name
def split_name(name):
    parts = name.split()
    first_name = parts[0] if parts else ''
    last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
    return first_name, last_name


# Function for  scraping contacts and save them to a CSV file
def scrape_contacts():
    driver = initialise_driver(chrome_driver_path)
    driver.get(website)
    csv_file_name = 'RealEstate.csv'

    time.sleep(5)

    contacts = []

    while True:
        try:
            loaded_section_selector = "[data-cy-loaded='true']"
            loaded_section = driver.find_element(By.CSS_SELECTOR, loaded_section_selector)

            tbodies = loaded_section.find_elements(By.TAG_NAME, 'tbody')
            if not tbodies:
                break

            for tbody in tbodies:
                first_anchor = tbody.find_element(By.TAG_NAME, 'a')
                if first_anchor:
                    first_anchor_text = first_anchor.text
                    first_name, last_name = split_name(first_anchor_text)

                    linkedin_url = ''
                    for link in tbody.find_elements(By.TAG_NAME, 'a'):
                        href = link.get_attribute('href')
                        if href and 'linkedin.com' in href:
                            linkedin_url = href
                            break

                    job_title_element = tbody.find_element(By.CLASS_NAME, 'zp_Y6y8d')
                    job_title = job_title_element.text if job_title_element else ''

                    company_name = ''
                    for link in tbody.find_elements(By.TAG_NAME, 'a'):
                        if 'accounts' in link.get_attribute('href'):
                            company_name = link.text
                            break

                    phone_number = tbody.find_elements(By.TAG_NAME, 'a')[-1].text

                    button_classes = ["zp-button", "zp_zUY3r", "zp_hLUWg", "zp_n9QPr", "zp_B5hnZ", "zp_MCSwB",
                                      "zp_IYteB"]

                    try:
                        button = tbody.find_element(By.CSS_SELECTOR, "." + ".".join(button_classes))
                        if button:
                            button.click()
                            email_addresses = find_email_address(driver.page_source)
                            filtered_emails = filter_emails(email_addresses, 'sentry.io')
                            email_1 = filtered_emails[0] if len(filtered_emails) > 0 else ''
                            email_2 = filtered_emails[1] if len(filtered_emails) > 1 else ''

                            contact = {
                                'firstname': first_name,
                                'lastname': last_name,
                                'job_title': job_title,
                                'company_name': company_name,
                                'email': email_1,
                                'email_alternate': email_2,
                                'linkedin': linkedin_url,
                                'phone_number': phone_number
                            }
                            contacts.append(contact)
                            print(f"{first_name} has been poached!")

                            # Write to CSV file
                            with open(csv_file_name, 'a', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                writer.writerow([
                                    first_name,
                                    last_name,
                                    job_title,
                                    company_name,
                                    email_1,
                                    email_2,
                                    linkedin_url,
                                    phone_number
                                ])

                            # Update HubSpot
                            status_code, response_text = add_contact_to_hubspot(first_name, last_name, job_title,
                                                                                company_name, email_1, phone_number)
                            print(f"HubSpot Response: {status_code} - {response_text}")

                            button.click()
                            tbody_height = driver.execute_script("return arguments[0].offsetHeight;", tbody)
                            driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", loaded_section,
                                                  tbody_height)
                    except NoSuchElementException:
                        continue

            # Pagination Logic
            next_button_selector = ".zp-button.zp_zUY3r.zp_MCSwB.zp_xCVC8[aria-label='right-arrow']"
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, next_button_selector)
                next_button.click()
                time.sleep(1)
            except NoSuchElementException:
                print("No more pages to navigate.")
                break

        except Exception as e:
            error_message = str(e)
            if "element click intercepted" in error_message:
                print("Your leads are ready!")
                break
            else:
                print(f"An error occurred: {error_message}")
                break

    driver.quit()
    return contacts


scrape_contacts()
