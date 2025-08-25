import os
import pytest
import allure
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

def pytest_addoption(parser):
    parser.addoption("--headless", action="store", default="true")

@pytest.fixture(scope="session")
def cfg(request):
    return {
        "BASE_URL": os.getenv("BASE_URL", "https://test.example.com"),
        "HEADLESS": request.config.getoption("--headless").lower() == "true",
        "TIMEOUT": int(os.getenv("TIMEOUT", "15")),
    }

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture()
def driver(request, cfg):
    opts = Options()
    if cfg["HEADLESS"]:
        opts.add_argument("--headless=new")
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    drv = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    yield drv

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            allure.attach(drv.get_screenshot_as_png(), "screenshot", allure.attachment_type.PNG)
        except Exception:
            pass
        try:
            allure.attach(drv.page_source, "page_source", allure.attachment_type.HTML)
        except Exception:
            pass
        try:
            allure.attach(str(drv.get_log("browser")), "browser_console", allure.attachment_type.TEXT)
        except Exception:
            pass
    drv.quit()
