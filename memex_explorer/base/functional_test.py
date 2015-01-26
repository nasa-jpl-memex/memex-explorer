from robobrowser import RoboBrowser

# Andy opens his browser window.
browser = RoboBrowser(history=True)

# Andy decides to test out our application, so he heads over to the index.
APP_HOME_PAGE = "http://localhost:8000"
browser.open(APP_HOME_PAGE)

# Andy checks that he clicked on the right link.

# Andy creates a new project.
