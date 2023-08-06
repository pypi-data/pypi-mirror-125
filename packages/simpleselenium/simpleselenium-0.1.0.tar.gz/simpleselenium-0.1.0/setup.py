# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpleselenium']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.9b0,<22.0',
 'pre-commit>=2.15.0,<3.0.0',
 'pytest-env>=0.6.2,<0.7.0',
 'selenium==3.141.0',
 'tox>=3.24.4,<4.0.0']

setup_kwargs = {
    'name': 'simpleselenium',
    'version': '0.1.0',
    'description': 'Python package to easily work with Selenium.',
    'long_description': '### Simple Selenium\n\nThe aim of this package is to quickly get started with working with selenium for simple browser automation tasks.\n\n### Usage\n\nThe best way to getting started with the package is to use the `Browser` object to start a browser and call `open`\nmethod off it which returns a Tab object.\n\n#### Browser\n\n```python\nimport time  # just to slow down stuffs and see things for testing\nfrom simpleselenium import Browser\n\nchrome_driver = r"/path/to/chromedriver"\n\nwith Browser(name="Chrome", driver_path=chrome_driver, implicit_wait=10) as browser:\n    google = browser.open("https://google.com")\n    yahoo = browser.open("https://yahoo.com")\n    bing = browser.open("https://bing.com")\n    duck_duck = browser.open("https://duckduckgo.com/")\n\n    print(yahoo)  # A Tab Object\n    print(yahoo.is_alive)\n    print(yahoo.is_active)\n    print(dir(yahoo))  # All methods and attributes of Tab Objects\n\n    print(browser.get_all_tabs())  # List of tab objects\n\n    print(browser.tabs.all())\n    print(browser.tabs)  # TabManager object\n    print(dir(browser.tabs))  # All methods and attributes of TabManager Objects\n\n    browser.close_tab(bing)  # close a browser tab\n    print(browser.tabs.all())\n\n    print(browser.get_current_tab())  # current tab\n    time.sleep(5)\n\n    yahoo.switch()  # switch/focus/tap to/on `yahoo` tab\n    print(browser.get_current_tab())\n    time.sleep(5)\n\n    google.switch()\n    print(browser.get_current_tab())\n    time.sleep(5)\n\n    browser.close_tab(yahoo)\n    time.sleep(5)\n\n    print(google.driver)  # Usual selenium driver object which can be worked upon\n\n    print(google.driver.title, google.title)\n\n    print(google.scroll_to_bottom())\n    print(google.is_active)\n    print(google.is_alive)\n    print(bing.is_alive)  # False, it has been deleted.\n\n    print(browser.get_all_tabs())\n```\n',
    'author': 'Vishal Kumar Mishra',
    'author_email': 'vishal.k.mishra2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TheConfused/simpleselenium',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
