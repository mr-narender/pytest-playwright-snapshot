from playwright.sync_api import Page


def test_open_google_page_and_assert_title(page: Page):
    # Launch the browser

    # Navigate to Google
    page.goto("https://www.google.com")

    # Assert the title
    assert page.title() == "Google1"
