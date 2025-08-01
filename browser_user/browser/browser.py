from browser_user.browser.profile import BrowserProfile
from browser_user.browser.session import BrowserSession

BrowserConfig = BrowserProfile
BrowserContextConfig = BrowserProfile
Browser = BrowserSession

__all__ = ['BrowserConfig', 'BrowserContextConfig', 'Browser']
