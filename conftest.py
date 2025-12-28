"""
Pytest Configuration and Global Fixtures
"""

import pytest
import os
from datetime import datetime


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: Mark test as smoke test (critical functionality)"
    )
    config.addinivalue_line(
        "markers", "regression: Mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "mobile: Mark test as mobile device test"
    )
    config.addinivalue_line(
        "markers", "security: Mark test as security-related test"
    )


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "SwiftAssess Signup Automation Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    """Add custom summary to HTML report"""
    prefix.extend([
        "<h2>SwiftAssess Signup Page Testing</h2>",
        f"<p>Test Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        "<p>Test URL: https://app.swiftassess.com/Signup</p>"
    ])


@pytest.fixture(scope="session", autouse=True)
def test_environment_setup():
    """Setup test environment before all tests"""
    print("\n" + "="*50)
    print("SwiftAssess Test Suite - Starting")
    print("="*50)
    
    # Create directories for reports
    os.makedirs("test_screenshots", exist_ok=True)
    os.makedirs("test-results", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)
    
    yield
    
    print("\n" + "="*50)
    print("SwiftAssess Test Suite - Completed")
    print("="*50)


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application"""
    return "https://app.swiftassess.com"


@pytest.fixture(scope="session")
def signup_url(base_url):
    """Signup page URL"""
    return f"{base_url}/Signup"