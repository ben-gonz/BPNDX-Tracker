# pip install webdriver_manager selenium python-dotenv

import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText

# Load .env file for local testing (ignored in Lambda; specify your custom file name)
load_dotenv(dotenv_path='bpndx_scrape_and_email.env')

def lambda_handler(event=None, context=None):
    url = 'https://stockcharts.com/freecharts/symbolsummary.html?sym=%24bpndx'
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Suppress GPU-related warnings
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    # Anti-detection for headless
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Suppress ChromeDriver logs
    service = Service(ChromeDriverManager().install(), log_output=os.devnull)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        
        wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds
        
        def get_element_safe(d):
            try:
                return d.find_element(By.ID, 'latestPrice')
            except NoSuchElementException:
                return None
        
        price_elem = wait.until(lambda d: (elem if (elem := get_element_safe(d)) and elem.text.strip() != '-' else False))
        
        price_str = price_elem.text.strip()
        
        try:
            price = float(price_str)
            print(f"Current BPNDX: {price}")
            
            if price <= 20.00:
                # Load from environment variables
                sender_email = os.environ.get('SENDER_EMAIL')
                receiver_email = os.environ.get('RECEIVER_EMAIL')
                app_password = os.environ.get('APP_PASSWORD')
                
                if not all([sender_email, receiver_email, app_password]):
                    raise RuntimeError("Missing environment variables: SENDER_EMAIL, RECEIVER_EMAIL, or APP_PASSWORD")
                
                msg = MIMEText(f"BPNDX has dropped to {price}, which is at or below 20.00. Time to consider buying low!")
                msg['Subject'] = 'BPNDX Buy Signal Alert'
                msg['From'] = sender_email
                msg['To'] = receiver_email
                
                try:
                    with smtplib.SMTP('smtp.zoho.com', 587) as server:
                        server.starttls()
                        server.login(sender_email, app_password)
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                    print("Email sent successfully")
                except Exception as e:
                    print(f"Email failed: {str(e)}")
        except ValueError:
            print(f"Invalid price format: {price_str}")
    except TimeoutException:
        print("Timeout: latestPrice element did not update from '-' within 30 seconds.")
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
    finally:
        driver.quit()

# For local testing
if __name__ == "__main__":
    lambda_handler()