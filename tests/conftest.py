import os

import pytest
import pytest_html


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    extras = getattr(rep, "extras", [])

    if rep.when == "call" and rep.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_path = capture_screenshot(page, item.nodeid)
            if screenshot_path:
                rep.extras.append(pytest_html.extras.image(screenshot_path))
            rep.extras = extras


def capture_screenshot(page, test_name):
    screenshot_dir = "screenshots"
    test_name = test_name.replace("::", "_").replace("/", "_").replace(".", "_")
    screenshot_filename = f"{test_name}_screenshot.png"
    screenshot_path = f"{screenshot_dir}/{screenshot_filename}"

    if not page.is_closed():
        page.screenshot(path=screenshot_path)
    return screenshot_path


def get_screenshot_path(item):
    screenshot_dir = "screenshots"
    item_node_id = item.nodeid.replace("::", "_").replace("/", "_").replace(".", "_")
    screenshot_filename = f"{item_node_id}_screenshot.png"
    screenshot_path = os.path.join(screenshot_dir, screenshot_filename)

    return screenshot_path if os.path.exists(screenshot_path) else None
