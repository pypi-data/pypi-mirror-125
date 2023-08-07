Explanation on youtube: https://www.youtube.com/watch?v=JUMmBmXNDOU


Logging of screenshot and messages to HTML file. Can be used with selenium, but not necessary.
How to use it:

from LoggingSelenium.LogHTML import LogHTML

LogHTML.set_log_path(r"C:\pathToFolderForLogs")

LogHTML.screenshot("Screenshot is taken")
LogHTML.info("Random message")