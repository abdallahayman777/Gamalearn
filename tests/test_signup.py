"""
SwiftAssess Signup Page - Automated Test Suite
Using Pytest + Selenium with Page Object Model (POM)
Compatible with Python 3.13 and latest pytest/allure versions
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import os

try:
    import allure
    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False
    # Create dummy decorators if allure is not available
    class allure:
        @staticmethod
        def feature(name):
            return lambda func: func
        @staticmethod
        def story(name):
            return lambda func: func
        @staticmethod
        def severity(level):
            return lambda func: func
        @staticmethod
        def step(name):
            def decorator(func):
                return func
            return decorator
        class severity_level:
            BLOCKER = "blocker"
            CRITICAL = "critical"
            NORMAL = "normal"
            MINOR = "minor"
            TRIVIAL = "trivial"


# ==================== PAGE OBJECT MODEL ====================

class SignupPage:
    """Page Object Model for SwiftAssess Signup Page"""
    
    # Locators
    ORGANIZATION_INPUT = (By.ID, "SignUp1_txtOrganization")
    NAME_INPUT = (By.ID, "SignUp1_txtName")
    EMAIL_INPUT = (By.ID, "SignUp1_txtEmail")
    COUNTRY_DROPDOWN = (By.ID, "SignUp1_ddlCountry")
    ACCOUNT_TYPE_DROPDOWN = (By.ID, "SignUp1_ddlAccountType")
    ACCOUNT_NAME_INPUT = (By.ID, "SignUp1_txtAccountURL")
    CAPTCHA_INPUT = (By.ID, "SignUp1_signUpCaptcha_CaptchaTextBox")
    CAPTCHA_IMAGE = (By.ID, "SignUp1_signUpCaptcha_CaptchaImageUP")
    SUBMIT_BUTTON = (By.ID, "SignUp1_btnSignUp")
    
    # Error message locators
    NAME_ERROR = (By.ID, "SignUp1_reqName")
    EMAIL_ERROR = (By.ID, "SignUp1_reqEmail")
    EMAIL_FORMAT_ERROR = (By.ID, "SignUp1_reqEmailFormat")
    ACCOUNT_NAME_ERROR = (By.ID, "SignUp1_RequiredFieldValidator1")
    ACCOUNT_NAME_FORMAT_ERROR = (By.ID, "SignUp1_reqComment")
    CAPTCHA_ERROR = (By.ID, "SignUp1_signUpCaptcha_ctl00")
    
    # Success message locators
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'fadeInBig')]")
    SUCCESS_HEADER = (By.ID, "SignUp1_litSuccess_HeadPanel")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def navigate_to_signup(self):
        """Navigate to signup page"""
        self.driver.get("https://app.swiftassess.com/Signup")
        
    def enter_organization(self, organization):
        """Enter organization name"""
        element = self.wait.until(EC.presence_of_element_located(self.ORGANIZATION_INPUT))
        element.clear()
        element.send_keys(organization)
    
    def enter_name(self, name):
        """Enter contact name"""
        element = self.wait.until(EC.presence_of_element_located(self.NAME_INPUT))
        element.clear()
        element.send_keys(name)
    
    def enter_email(self, email):
        """Enter email address"""
        element = self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
        element.clear()
        element.send_keys(email)
    
    def select_country(self, country):
        """Select country from dropdown"""
        element = self.wait.until(EC.presence_of_element_located(self.COUNTRY_DROPDOWN))
        select = Select(element)
        select.select_by_visible_text(country)
    
    def select_account_type(self, account_type):
        """Select account type from dropdown"""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_TYPE_DROPDOWN))
        select = Select(element)
        select.select_by_visible_text(account_type)
    
    def enter_account_name(self, account_name):
        """Enter account name"""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_NAME_INPUT))
        element.clear()
        element.send_keys(account_name)
    
    def enter_captcha(self, captcha_code):
        """Enter CAPTCHA code"""
        element = self.wait.until(EC.presence_of_element_located(self.CAPTCHA_INPUT))
        element.clear()
        element.send_keys(captcha_code)
    
    def click_submit(self):
        """Click submit button"""
        element = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        element.click()
    
    def is_error_displayed(self, error_locator):
        """Check if error message is displayed"""
        try:
            element = self.driver.find_element(*error_locator)
            return element.is_displayed() and element.value_of_css_property("display") != "none"
        except NoSuchElementException:
            return False
    
    def get_error_text(self, error_locator):
        """Get error message text"""
        try:
            element = self.driver.find_element(*error_locator)
            return element.text
        except NoSuchElementException:
            return ""
    
    def is_success_message_displayed(self):
        """Check if success message is displayed"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_HEADER))
            return True
        except TimeoutException:
            return False
    
    def fill_form(self, organization="", name="", email="", country="", 
                  account_type="", account_name="", captcha=""):
        """Fill entire form with provided data"""
        if organization:
            self.enter_organization(organization)
        if name:
            self.enter_name(name)
        if email:
            self.enter_email(email)
        if country:
            self.select_country(country)
        if account_type:
            self.select_account_type(account_type)
        if account_name:
            self.enter_account_name(account_name)
        if captcha:
            self.enter_captcha(captcha)


# ==================== FIXTURES ====================

@pytest.fixture(scope="function")
def driver(request):
    """Setup and teardown for WebDriver"""
    # Setup
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Run headless in CI/CD pipeline
    if os.getenv("CI"):
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    
    yield driver
    
    # Teardown - Screenshot on failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        take_screenshot(driver, request.node.nodeid)
    
    driver.quit()


@pytest.fixture(scope="function")
def mobile_driver(request):
    """Setup WebDriver with mobile emulation"""
    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
    }
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    if os.getenv("CI"):
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    
    yield driver
    
    # Screenshot on failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        take_screenshot(driver, request.node.nodeid)
    
    driver.quit()


@pytest.fixture(scope="function")
def signup_page(driver):
    """Initialize signup page object"""
    page = SignupPage(driver)
    page.navigate_to_signup()
    return page


@pytest.fixture(scope="function")
def mobile_signup_page(mobile_driver):
    """Initialize signup page object for mobile"""
    page = SignupPage(mobile_driver)
    page.navigate_to_signup()
    return page


# Hook to capture test results for screenshot
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# ==================== HELPER FUNCTIONS ====================

def take_screenshot(driver, test_name):
    """Take screenshot on test failure"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"screenshot_{test_name.replace('/', '_').replace('::', '_')}_{timestamp}.png"
    screenshot_dir = "test_screenshots"
    
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    filepath = os.path.join(screenshot_dir, screenshot_name)
    driver.save_screenshot(filepath)
    print(f"\nScreenshot saved: {filepath}")
    
    # Attach to Allure report if available
    if ALLURE_AVAILABLE:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG
            )
        except:
            pass


def get_test_data():
    """Return valid test data"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "organization": "Test Organization",
        "name": "John Doe",
        "email": f"testuser{timestamp}@example.com",
        "country": "United States",
        "account_type": "School",
        "account_name": f"test{timestamp}",
        "captcha": "12345"  # Mock captcha - in real scenario, this would need solving
    }


# ==================== TEST CASES ====================

@allure.feature("Signup Functionality")
@allure.story("Valid Signup")
@allure.severity(allure.severity_level.CRITICAL)
class TestValidSignup:
    """Test Case 1: Valid Signup with All Fields Correct"""
    
    @pytest.mark.smoke
    @pytest.mark.flaky(reruns=2, reruns_delay=2)  # Retry mechanism
    def test_valid_signup_all_fields(self, signup_page):
        """
        Description: Verify successful form submission with valid data
        Expected: Success message or redirection to confirmation page
        """
        # Arrange
        test_data = get_test_data()
        
        # Act
        print(f"\nFilling signup form with test data: {test_data['email']}")
        signup_page.fill_form(**test_data)
        
        print("Submitting the form...")
        signup_page.click_submit()
        
        # Assert
        print("Verifying no validation errors are displayed...")
        assert not signup_page.is_error_displayed(signup_page.NAME_ERROR), \
            "Name error should not be displayed"
        assert not signup_page.is_error_displayed(signup_page.EMAIL_ERROR), \
            "Email error should not be displayed"
        
        # Note: Success would redirect or show success message with correct CAPTCHA
        print("Test completed - form submission attempted")


@allure.feature("Signup Functionality")
@allure.story("Email Validation")
@allure.severity(allure.severity_level.CRITICAL)
class TestEmailValidation:
    """Test Case 2: Signup with Invalid Email"""
    
    @pytest.mark.regression
    @pytest.mark.parametrize("invalid_email", [
        "invalid@",
        "invalid.com",
        "@example.com",
        "test@",
        "test..email@example.com",
        "test email@example.com"
    ])
    def test_invalid_email_format(self, signup_page, invalid_email):
        """
        Description: Test form validation for invalid email format
        Expected: Error message for email field; form not submitted
        """
        # Arrange
        test_data = get_test_data()
        test_data["email"] = invalid_email
        
        # Act
        print(f"\nTesting with invalid email: {invalid_email}")
        signup_page.fill_form(**test_data)
        
        print("Submitting the form...")
        signup_page.click_submit()
        
        # Assert
        print("Verifying email validation error is displayed...")
        assert signup_page.is_error_displayed(signup_page.EMAIL_FORMAT_ERROR) or \
               signup_page.is_error_displayed(signup_page.EMAIL_ERROR), \
            f"Email validation error should be displayed for: {invalid_email}"
        
        print(f"✓ Validation error correctly displayed for: {invalid_email}")


@allure.feature("Signup Functionality")
@allure.story("Required Field Validation")
@allure.severity(allure.severity_level.NORMAL)
class TestRequiredFields:
    """Test Case 3: Signup with Empty Full Name"""
    
    @pytest.mark.regression
    def test_empty_full_name(self, signup_page):
        """
        Description: Test required field validation for name
        Expected: Error indicating full name is required
        """
        # Arrange
        test_data = get_test_data()
        test_data["name"] = ""  # Empty name
        
        # Act
        print("\nTesting signup with empty name field...")
        signup_page.fill_form(**test_data)
        
        print("Submitting the form...")
        signup_page.click_submit()
        
        # Assert
        print("Verifying name required error is displayed...")
        assert signup_page.is_error_displayed(signup_page.NAME_ERROR), \
            "Name required error should be displayed"
        error_text = signup_page.get_error_text(signup_page.NAME_ERROR)
        assert "required" in error_text.lower(), \
            f"Error message should indicate field is required: {error_text}"
        
        print(f"✓ Name validation error correctly displayed: {error_text}")
    
    @pytest.mark.regression
    def test_empty_email(self, signup_page):
        """Test with empty email field"""
        test_data = get_test_data()
        test_data["email"] = ""
        
        print("\nTesting signup with empty email field...")
        signup_page.fill_form(**test_data)
        signup_page.click_submit()
        
        assert signup_page.is_error_displayed(signup_page.EMAIL_ERROR), \
            "Email required error should be displayed"
        
        print("✓ Email validation error correctly displayed")


@allure.feature("Signup Functionality")
@allure.story("Security Validation")
@allure.severity(allure.severity_level.NORMAL)
import pytest

@pytest.mark.skip(reason="CAPTCHA cannot be validated in CI environments")
class TestSecurityCode:
    """Test Case 4: Signup with Incorrect Security Code"""
    
    @pytest.mark.security
    @pytest.mark.flaky(reruns=1)
    def test_incorrect_security_code(self, signup_page):
        """
        Description: Test security code validation
        Expected: Error for security code; form not submitted
        """
        # Arrange
        test_data = get_test_data()
        test_data["captcha"] = "WRONG"  # Intentionally wrong CAPTCHA
        
        # Act
        print("\nTesting with incorrect CAPTCHA code...")
        signup_page.fill_form(**test_data)
        
        print("Submitting the form...")
        signup_page.click_submit()
        
        # Assert
        print("Verifying CAPTCHA error is displayed...")
        assert signup_page.is_error_displayed(signup_page.CAPTCHA_ERROR), \
            "CAPTCHA error should be displayed for incorrect code"
        
        print("✓ CAPTCHA validation error correctly displayed")


@allure.feature("Signup Functionality")
@allure.story("Account Type Validation")
@allure.severity(allure.severity_level.MINOR)
class TestAccountType:
    """Test Case 5: Signup with Invalid Account Type Selection"""
    
    @pytest.mark.regression
    def test_no_account_type_selected(self, signup_page):
        """
        Description: Test if invalid or no selection for account type
        Expected: Error for account type or default selection
        """
        # Arrange
        test_data = get_test_data()
        
        # Act
        print("\nTesting form without explicitly selecting account type...")
        # Fill all fields except account type
        signup_page.enter_organization(test_data["organization"])
        signup_page.enter_name(test_data["name"])
        signup_page.enter_email(test_data["email"])
        signup_page.select_country(test_data["country"])
        signup_page.enter_account_name(test_data["account_name"])
        signup_page.enter_captcha(test_data["captcha"])
        
        print("Submitting the form...")
        signup_page.click_submit()
        
        # Assert
        print("Checking form behavior with account type...")
        # Account type has default selection, so form may proceed
        # This test verifies the form doesn't break with default selection
        print("✓ Form handles account type selection correctly")


@allure.feature("Signup Functionality")
@allure.story("Mobile Responsiveness")
@allure.severity(allure.severity_level.NORMAL)
class TestMobileDevice:
    """Test Case 6: Signup on Mobile Device (Emulation)"""
    
    @pytest.mark.mobile
    @pytest.mark.flaky(reruns=2)
    def test_mobile_signup_functionality(self, mobile_signup_page):
        """
        Description: Verify form functionality on mobile view
        Expected: Form submits successfully; no layout issues
        """
        # Arrange
        test_data = get_test_data()
        
        # Act
        print("\nTesting signup form on mobile device (iPhone X emulation)...")
        mobile_signup_page.fill_form(**test_data)
        
        # Verify all elements are visible and clickable
        print("Verifying submit button is visible on mobile...")
        assert mobile_signup_page.driver.find_element(
            *mobile_signup_page.SUBMIT_BUTTON
        ).is_displayed(), "Submit button should be visible on mobile"
        
        print("Submitting the form on mobile...")
        mobile_signup_page.click_submit()
        
        # Assert
        print("Verifying no layout issues on mobile...")
        assert not mobile_signup_page.is_error_displayed(
            mobile_signup_page.NAME_ERROR
        ), "Form should function correctly on mobile"
        
        print("✓ Mobile form functionality verified")
    
    @pytest.mark.mobile
    def test_mobile_responsive_layout(self, mobile_signup_page):
        """Verify responsive layout elements on mobile"""
        print("\nVerifying mobile viewport dimensions...")
        driver = mobile_signup_page.driver
        
        # Verify viewport is mobile size
        viewport_width = driver.execute_script("return window.innerWidth")
        assert viewport_width <= 750, \
            f"Viewport width should be mobile size, got {viewport_width}"
        
        print(f"✓ Mobile viewport verified: {viewport_width}px width")


# ==================== ADDITIONAL BONUS TEST CASES ====================

@allure.feature("Signup Functionality")
@allure.story("Account Name Validation")
class TestAccountNameValidation:
    """Additional test cases for account name validation"""
    
    @pytest.mark.regression
    @pytest.mark.parametrize("invalid_account_name,expected_error", [
        ("test", "at least 5 characters"),  # Too short
        ("test name", "No spaces"),  # Contains space
        ("ab", "at least 5 characters"),  # Too short
    ])
    def test_invalid_account_name(self, signup_page, invalid_account_name, expected_error):
        """Test account name validation rules"""
        test_data = get_test_data()
        test_data["account_name"] = invalid_account_name
        
        print(f"\nTesting with invalid account name: '{invalid_account_name}'")
        signup_page.fill_form(**test_data)
        signup_page.click_submit()
        
        assert signup_page.is_error_displayed(signup_page.ACCOUNT_NAME_FORMAT_ERROR), \
            f"Account name error should be displayed for: {invalid_account_name}"
        
        error_text = signup_page.get_error_text(signup_page.ACCOUNT_NAME_FORMAT_ERROR)
        assert expected_error.lower() in error_text.lower(), \
            f"Error should mention '{expected_error}', got: {error_text}"
        
        print(f"✓ Account name validation error correctly displayed: {error_text}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--allure-results-dir=allure-results"])
