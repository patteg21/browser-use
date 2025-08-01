from browser_user.browser.profile import BrowserProfile
from browser_user.browser.session import BrowserSession

Browser = BrowserSession
BrowserConfig = BrowserProfile
BrowserContext = BrowserSession
BrowserContextConfig = BrowserProfile

__all__ = ['Browser', 'BrowserConfig', 'BrowserContext', 'BrowserContextConfig']
