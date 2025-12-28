"""
Utility Functions for SwiftAssess Test Automation
"""

from datetime import datetime
from faker import Faker
import random
import string

fake = Faker()


class TestDataGenerator:
    """Generate test data for signup forms"""
    
    @staticmethod
    def generate_email(prefix="test"):
        """Generate unique email address"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"{prefix}{timestamp}{random_num}@example.com"
    
    @staticmethod
    def generate_account_name(length=10):
        """Generate valid account name (5+ chars, no spaces)"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        return f"test{timestamp}"[:length]
    
    @staticmethod
    def generate_organization_name():
        """Generate organization name"""
        return fake.company()
    
    @staticmethod
    def generate_full_name():
        """Generate full name"""
        return fake.name()
    
    @staticmethod
    def generate_invalid_emails():
        """Generate list of invalid email formats"""
        return [
            "invalid@",
            "invalid.com",
            "@example.com",
            "test@",
            "test..email@example.com",
            "test email@example.com",
            "test@domain",
            "test@@example.com",
            "test@.com",
            ".test@example.com",
            "test@domain..com",
        ]
    
    @staticmethod
    def generate_invalid_account_names():
        """Generate invalid account names with reasons"""
        return [
            ("ab", "Too short - less than 5 characters"),
            ("test", "Too short - only 4 characters"),
            ("test name", "Contains space"),
            ("test-name", "Contains special character"),
            ("test@name", "Contains special character"),
            ("test.name", "Contains period"),
            ("TEST NAME", "Contains space and uppercase"),
        ]
    
    @staticmethod
    def generate_valid_test_data():
        """Generate complete valid test data"""
        return {
            "organization": TestDataGenerator.generate_organization_name(),
            "name": TestDataGenerator.generate_full_name(),
            "email": TestDataGenerator.generate_email(),
            "country": random.choice([
                "United States", "United Kingdom", "Canada", 
                "Australia", "Germany", "France"
            ]),
            "account_type": random.choice(["School", "College", "General"]),
            "account_name": TestDataGenerator.generate_account_name(),
            "captcha": "12345"  # Mock value
        }


class WaitHelpers:
    """Custom wait helper functions"""
    
    @staticmethod
    def wait_for_page_load(driver, timeout=30):
        """Wait for page to fully load"""
        from selenium.webdriver.support.ui import WebDriverWait
        
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    
    @staticmethod
    def wait_for_ajax(driver, timeout=30):
        """Wait for jQuery AJAX calls to complete"""
        from selenium.webdriver.support.ui import WebDriverWait
        
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return jQuery.active == 0")
            )
        except:
            pass  # jQuery might not be present
    
    @staticmethod
    def wait_for_element_to_disappear(driver, locator, timeout=10):
        """Wait for element to disappear"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )


class ScreenshotHelper:
    """Enhanced screenshot functionality"""
    
    @staticmethod
    def take_full_page_screenshot(driver, filename):
        """Take screenshot of entire page (scrolling)"""
        original_size = driver.get_window_size()
        required_width = driver.execute_script(
            "return document.body.parentNode.scrollWidth"
        )
        required_height = driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )
        
        driver.set_window_size(required_width, required_height)
        driver.save_screenshot(filename)
        driver.set_window_size(original_size['width'], original_size['height'])
    
    @staticmethod
    def take_element_screenshot(driver, element, filename):
        """Take screenshot of specific element"""
        element.screenshot(filename)


class ValidationHelper:
    """Validation helper functions"""
    
    @staticmethod
    def is_valid_email(email):
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_account_name(account_name):
        """Validate account name (5+ chars, no spaces)"""
        if len(account_name) < 5:
            return False, "Must be at least 5 characters"
        if ' ' in account_name:
            return False, "No spaces allowed"
        if not account_name.replace('_', '').replace('-', '').isalnum():
            return False, "Only alphanumeric characters allowed"
        return True, "Valid"


class BrowserHelper:
    """Browser-related helper functions"""
    
    @staticmethod
    def clear_browser_data(driver):
        """Clear cookies and storage"""
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
    
    @staticmethod
    def set_mobile_viewport(driver, device="iphone_x"):
        """Set viewport to mobile dimensions"""
        devices = {
            "iphone_x": (375, 812),
            "iphone_12": (390, 844),
            "samsung_s21": (360, 800),
            "ipad": (768, 1024),
        }
        
        width, height = devices.get(device, devices["iphone_x"])
        driver.set_window_size(width, height)
    
    @staticmethod
    def scroll_to_element(driver, element):
        """Scroll element into view"""
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    @staticmethod
    def highlight_element(driver, element, duration=2):
        """Highlight element for debugging"""
        original_style = element.get_attribute("style")
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            "border: 3px solid red; background-color: yellow;"
        )
        import time
        time.sleep(duration)
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            original_style
        )


class ReportHelper:
    """Reporting helper functions"""
    
    @staticmethod
    def log_test_step(step_name, status="INFO"):
        """Log test step"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{status}] {step_name}")
    
    @staticmethod
    def log_test_data(data_dict):
        """Log test data for debugging"""
        print("\n" + "="*50)
        print("Test Data:")
        for key, value in data_dict.items():
            # Mask sensitive data
            if key.lower() in ['password', 'captcha', 'security']:
                value = "*" * len(str(value))
            print(f"  {key}: {value}")
        print("="*50 + "\n")


class RetryHelper:
    """Retry mechanism for flaky operations"""
    
    @staticmethod
    def retry_on_exception(func, max_attempts=3, delay=1, exceptions=(Exception,)):
        """Retry function on specific exceptions"""
        import time
        
        for attempt in range(max_attempts):
            try:
                return func()
            except exceptions as e:
                if attempt == max_attempts - 1:
                    raise
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(delay)


class ConfigHelper:
    """Configuration helper"""
    
    @staticmethod
    def get_base_url():
        """Get base URL from environment or default"""
        import os
        return os.getenv("BASE_URL", "https://app.swiftassess.com")
    
    @staticmethod
    def get_browser():
        """Get browser choice from environment"""
        import os
        return os.getenv("BROWSER", "chrome").lower()
    
    @staticmethod
    def is_headless():
        """Check if tests should run headless"""
        import os
        return os.getenv("HEADLESS", "false").lower() == "true" or os.getenv("CI", "false").lower() == "true"
    
    @staticmethod
    def get_timeout():
        """Get default timeout"""
        import os
        return int(os.getenv("DEFAULT_TIMEOUT", "10"))


# Example usage in tests:
"""
from utils import TestDataGenerator, WaitHelpers, ReportHelper

# Generate test data
test_data = TestDataGenerator.generate_valid_test_data()
ReportHelper.log_test_data(test_data)

# Use in test
signup_page.fill_form(**test_data)

# Wait for page load
WaitHelpers.wait_for_page_load(driver)
"""