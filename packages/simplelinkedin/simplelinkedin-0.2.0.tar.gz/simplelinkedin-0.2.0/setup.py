# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplelinkedin']

package_data = \
{'': ['*']}

install_requires = \
['pytest-env>=0.6.2,<0.7.0',
 'python-crontab==2.5.1',
 'python-dotenv==0.18.0',
 'selenium==3.141.0',
 'toml==0.10.2']

setup_kwargs = {
    'name': 'simplelinkedin',
    'version': '0.2.0',
    'description': 'Python package to work with LinkedIn',
    'long_description': '# LinkedIn\n\nPython script to automate some usual tasks performed on social-networking site LinkedIn. The script has been tested on\nmacOS and is expected to work on Linux environment as well. Raise an issue/PR if you encounter any issue while running\nthe scripts.\n\nBefore you proceed:\n\n- Download appropriate chrome driver from https://chromedriver.chromium.org/downloads for the version of the Chrome you\n  have installed in your machine.\n- Allow the script to execute the chrome-driver file downloaded above\n\nThe best way to run and test the package for your needs is to use `sample_script.py` like below:\n\n```python\nfrom simplelinkedin import LinkedIn\n\nsettings = {\n  "LINKEDIN_USER": "<username>",\n  "LINKEDIN_PASSWORD": "<password>",\n  "LINKEDIN_BROWSER": "Chrome",\n  "LINKEDIN_BROWSER_DRIVER": "/path/to/chromedriver",\n  "LINKEDIN_BROWSER_HEADLESS": 0,\n  "LINKEDIN_BROWSER_CRON": 0,\n  "LINKEDIN_CRON_USER": "<root_user>",\n  "LINKEDIN_PREFERRED_USER": "/path/to/preferred/user/text_doc.text",\n  "LINKEDIN_NOT_PREFERRED_USER": "/path/to/not/preferred/user/text_doc.text",\n}\n\nwith LinkedIn(\n        username=settings.get("LINKEDIN_USER"),\n        password=settings.get("LINKEDIN_PASSWORD"),\n        browser=settings.get("LINKEDIN_BROWSER"),\n        driver_path=settings.get("LINKEDIN_BROWSER_DRIVER"),\n        headless=bool(settings.get("LINKEDIN_BROWSER_HEADLESS")),\n) as ln:\n  # do all the steps manually\n  ln.login()\n  ln.remove_sent_invitations(older_than_days=14)\n\n  ln.send_invitations(\n    max_invitation=max(ln.WEEKLY_MAX_INVITATION - ln.invitations_sent_last_week, 0),\n    min_mutual=10,\n    max_mutual=450,\n    preferred_users=["Quant"],  # file_path or list of features\n    not_preferred_users=["Sportsman"],  # file_path or list of features\n    view_profile=True,  # (recommended) view profile of users you sent connection request to\n  )\n\n  ln.accept_invitations()\n\n  # OR\n  # run smart follow-unfollow method (without setting cron jobs) which essentially does the same thing as\n  # all the above steps\n  ln.smart_follow_unfollow(\n    users_preferred=settings.get("LINKEDIN_PREFERRED_USER") or [],\n    users_not_preferred=settings.get("LINKEDIN_NOT_PREFERRED_USER") or [],\n  )\n\n  # setting and un-setting cron\n  # Use sudo in case you are setting/un-setting cron.\n\n  # set cron on your machine\n  ln.set_smart_cron(settings)\n\n  # remove existing cron jobs\n  ln.remove_cron_jobs(settings=settings)\n```\n\nAlternatively, you can go the command line way, like below.\n\n    usage: linkedin.py [-h] [--env ENV] [--email EMAIL] [--password PASSWORD] [--browser BROWSER] [--driver DRIVER] [--headless] [--cron] [--cronuser CRONUSER]\n                       [--preferred PREFERRED] [--notpreferred NOTPREFERRED]\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      --env ENV             Linkedin environment file\n      --email EMAIL         Email of linkedin user\n      --password PASSWORD   Password of linkedin user\n      --browser BROWSER     Browser used for linkedin\n      --driver DRIVER       Path to Chrome/Firefox driver\n      --headless            Whether to run headless\n      --cron                Whether to create a cron job\n      --cronuser CRONUSER   Run cron jobs as this user\n      --rmcron              Whether to remove existing cron\n      --preferred PREFERRED\n                            Path to file containing preferred users characteristics\n      --notpreferred NOTPREFERRED\n                            Path to file containing characteristics of not preferred users\n\nStart with following commands. Use `example.env` file as reference while setting values. Prepend `sudo` if\nsetting/un-setting cron in the commands below.\n\n    python linkedin.py --env .env\n    python linkedin.py --email abc@gmail.com --password $3cRET --browser Chrome --driver /path/to/chromedriver --cronuser john --preferred data/users_preferred.txt --notpreferred data/users_not_preferred.txt\n\nIf the above command works, you can change `.env` file and set `LINKEDIN_BROWSER_CRON=1` or pass `--cron` in the second\ncommand.\n\n`example.env`\n\n    LINKEDIN_USER=\n    LINKEDIN_PASSWORD=\n    LINKEDIN_BROWSER=Chrome\n    LINKEDIN_BROWSER_DRIVER=\n    LINKEDIN_BROWSER_HEADLESS=0\n    LINKEDIN_BROWSER_CRON=0\n    LINKEDIN_CRON_USER=\n    LINKEDIN_PREFERRED_USER=data/users_preferred.txt\n    LINKEDIN_NOT_PREFERRED_USER=data/users_not_preferred.txt\n\nTODOS:\n\n- improve documentation\n- Include Tests\n',
    'author': 'Vishal Kumar Mishra',
    'author_email': 'vishal.k.mishra2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TheConfused/LinkedIn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
