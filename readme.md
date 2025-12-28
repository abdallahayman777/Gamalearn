# SwiftAssess Signup Automation Test Suite

Comprehensive automated test suite for the SwiftAssess signup page using Selenium WebDriver, Pytest, and Azure DevOps CI/CD pipeline.

## 📋 Table of Contents

- [Overview](#overview)
- [Test Cases](#test-cases)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Reports](#reports)
- [Best Practices](#best-practices)

## 🎯 Overview

This automation framework tests the SwiftAssess signup functionality (https://app.swiftassess.com/Signup) with comprehensive coverage including:

- ✅ Valid signup scenarios
- ✅ Field validation (email, name, account name)
- ✅ Security code verification
- ✅ Mobile device responsiveness
- ✅ Screenshot capture on failures
- ✅ Retry mechanism for flaky tests

## 🧪 Test Cases

### Test Case 1: Valid Signup with All Fields Correct
**Description:** Verify successful form submission with valid data  
**Priority:** Critical  
**Tags:** `smoke`

### Test Case 2: Signup with Invalid Email
**Description:** Test form validation for invalid email formats  
**Priority:** Critical  
**Tags:** `regression`  
**Variations:** Tests 6 different invalid email formats

### Test Case 3: Signup with Empty Full Name
**Description:** Test required field validation for name  
**Priority:** High  
**Tags:** `regression`

### Test Case 4: Signup with Incorrect Security Code
**Description:** Test CAPTCHA/security code validation  
**Priority:** High  
**Tags:** `security`

### Test Case 5: Signup with Invalid Account Type Selection
**Description:** Test account type dropdown validation  
**Priority:** Medium  
**Tags:** `regression`

### Test Case 6: Signup on Mobile Device (Emulation)
**Description:** Verify form functionality on mobile viewport  
**Priority:** High  
**Tags:** `mobile`  
**Device:** iPhone X emulation (375x812)



## 📦 Prerequisites

- **Python:** 3.9 or higher
- **Chrome Browser:** Latest stable version
- **ChromeDriver:** Compatible with Chrome version
- **Azure DevOps Account:** For CI/CD pipeline
- **Operating System:** Windows, macOS, or Linux

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd swiftassess-automation
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install ChromeDriver

**Option A: Manual Installation**
- Download from: https://chromedriver.chromium.org/
- Add to system PATH

**Option B: Using webdriver-manager (Alternative)**
```bash
pip install webdriver-manager
```

Then modify driver initialization in test code:
```python
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
```

## 🏃 Running Tests

### Run All Tests

```bash
pytest tests/test_signup.py -v
```

### Run Specific Test Categories

```bash
# Smoke tests only
pytest tests/test_signup.py -m smoke -v

# Regression tests
pytest tests/test_signup.py -m regression -v

# Mobile tests
pytest tests/test_signup.py -m mobile -v

# Security tests
pytest tests/test_signup.py -m security -v
```

### Run with HTML Report

```bash
pytest tests/test_signup.py --html=report.html --self-contained-html -v
```

### Run with Allure Report

```bash
# Generate results
pytest tests/test_signup.py --alluredir=allure-results

# Serve report
allure serve allure-results
```

### Run Specific Test

```bash
pytest tests/test_signup.py::TestValidSignup::test_valid_signup_all_fields -v
```

### Run with Coverage

```bash
pytest tests/test_signup.py --cov=tests --cov-report=html
```

## 📊 Reports

### 1. JUnit XML Reports
- Location: `test-results/*.xml`
- Used by Azure DevOps for test tracking

### 2. HTML Reports
- Location: `test-results/*.html`
- Standalone HTML with test details

### 3. Allure Reports
- Location: `allure-report/`
- Rich, interactive test reports
- View with: `allure serve allure-results`

### 4. Failure Screenshots
- Location: `test_screenshots/`
- Automatically captured on test failures
- Timestamped for easy identification

### 5. Coverage Reports
- Location: `coverage/`
- HTML coverage report with line-by-line analysis

## 🎨 Best Practices Implemented

### 1. Page Object Model (POM)
- Separation of test logic and page interactions
- Reusable page methods
- Easy maintenance

### 2. Test Organization
- Grouped by functionality using classes
- Clear test names and descriptions
- Proper markers for categorization

### 3. Fixtures
- Driver setup/teardown
- Screenshot capture on failure
- Test data generation

### 4. Retry Mechanism
```python
@pytest.mark.flaky(reruns=2, reruns_delay=2)
```
- Handles flaky tests automatically
- Configurable retry count and delay

### 5. Screenshot on Failure
- Automatic capture when test fails
- Saved with timestamp and test name
- Attached to Allure reports

### 6. Explicit Waits
```python
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(locator)
)
```
- No hardcoded sleeps
- Waits for elements dynamically

### 7. Parameterized Tests
```python
@pytest.mark.parametrize("invalid_email", [...])
```
- Tests multiple scenarios efficiently
- Reduces code duplication

### 8. Allure Reporting
```python
@allure.feature("Signup")
@allure.story("Email Validation")
```
- Rich test documentation
- Step-by-step execution details

## 🔧 Troubleshooting

### ChromeDriver Version Mismatch
```bash
# Check Chrome version
google-chrome --version

# Download matching ChromeDriver
# https://chromedriver.chromium.org/downloads
```

### Tests Failing in Headless Mode
Add to Chrome options:
```python
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
```

### CAPTCHA Issues
The CAPTCHA field requires manual solving or integration with CAPTCHA solving service. Current tests assume CAPTCHA value for demonstration.

### Element Not Found
- Increase wait time
- Check if page loaded completely
- Verify locator strategy

## 📝 Notes

### CAPTCHA Handling
The security code (CAPTCHA) is a visual challenge that changes on each page load. For full automation, consider:

1. **Manual Testing:** Keep CAPTCHA tests for manual execution
2. **CAPTCHA Service:** Integrate with services like 2Captcha, Anti-Captcha
3. **Test Environment:** Request a test environment with disabled CAPTCHA
4. **Mocking:** Mock the CAPTCHA validation in test environment

### Current Implementation
Tests include CAPTCHA field interaction but assume a known value for demonstration purposes.

## 🤝 Contributing

1. Create feature branch
2. Write tests following POM pattern
3. Ensure all tests pass locally
4. Submit pull request
5. Pipeline will validate changes



---

**Happy Testing! 🎉**
