import requests
import os
import bs4
import logging
import hashlib
import argparse
import tkinter as tk
from tkinter import filedialog
logging.basicConfig(level=logging.INFO)

IP = "http://10.130.12.101"
CSRF_PAGE = f"{IP}/properties/authentication/login.php?redir=/properties/decide.php"
AUTH_PAGE = f"{IP}/userpost/xerox.set"
MD5_INDEX = "b78fa191b452f486e040ec613109b826"
parser = argparse.ArgumentParser(description='Print free from the St. Robert CHS library printer')
parser.add_argument('--file', help='Print a specific PDF file. If this is not added, a prompt will be launched.')
parser.add_argument('--simplex', action='store_true', help='Print single sided. Default double sided.')
parser.add_argument('--no-hack', action='store_true', help='Use this flag to disable hacking and print as Web User (instead of Admin).')
args = parser.parse_args()

if args.no_hack:
    logging.info('--no-hack enabled. Accounting will not be disabled.')
if args.file:
    file_name = args.file
else:
    root = tk.Tk()
    root.withdraw()
    file_name = filedialog.askopenfilename(filetypes=[("PDFs ONLY", "*.pdf")])
if os.path.isfile(file_name):
    logging.info(f"Using file: {file_name}")
else:
    raise Exception("File not found!")

if args.simplex:
    plex = "simplex"
else:
    plex = "duplex"
logging.info(f"Print mode: {plex} (Use --simplex for 1-sided printing)")

if hashlib.md5(requests.get("http://10.130.12.101").content).hexdigest() == MD5_INDEX:
    logging.info("Successfully found printer")
else:
    raise Exception("Printer not found!")

response = requests.get(CSRF_PAGE)
phpsessid = response.cookies["PHPSESSID"]
csrf_token = bs4.BeautifulSoup(response.text, 'html.parser').find('input', {'name': 'CSRFToken'})['value']
if csrf_token is not None:
    logging.info(f'Successfully found CSRF token: {csrf_token}')
    logging.info(f'Successfully found PHPSESSID: {phpsessid}')
else:
    raise Exception('No CSRF token found!')

########################################## Begin login

if not args.no_hack:
    cookies = {
        'PageToShow': '',
        'statusSelected': 'n1',
        'statusNumNodes': '8',
        'PHPSESSID': phpsessid,
        'WebTimerPopupID': '-1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://10.130.12.101/properties/authentication/login.php?redir=/properties/decide.php',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    data = {
        '_fun_function': 'HTTP_Authenticate_fn',
        'NextPage': '/properties/authentication/luidLogin.php',
        'webUsername': 'admin',
        'webPassword': '1111',
        'frmaltDomain': 'default',
        'CSRFToken': csrf_token
    }

    response = requests.post('http://10.130.12.101/userpost/xerox.set', headers=headers, cookies=cookies, data=data)
    logging.info("Logged in")

########################################## End login

########################################## Begin disable accounting

if not args.no_hack:
    cookies = {
        'PageToShow': '',
        'statusSelected': 'n1',
        'statusNumNodes': '8',
        'PHPSESSID': phpsessid,
        'WebTimerPopupID': '9',
        'propSelected': 'n29',
        'propNumNodes': '112',
        'propHierarchy': '0001000000000000000000000',
        'LastPage': '/aaa/acct/serviceAccessAndAccounting.php',
        'acctChoice': '-1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://10.130.12.101/aaa/acct/serviceAccessAndAccounting.php?from=Acct_Home',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    data = [
    ('_fun_function', 'HTTP_Set_FDI_Service_Enablement_fn'),
    ('scanTracked', 'TRUE'),
    ('faxTracked', 'TRUE'),
    ('NextPage', '/aaa/acct/serviceAccessAndAccounting.php'),
    ('CSRFToken', csrf_token),
    ('svcreg_id', '1'),
    ('svcreg_id', '2'),
    ('copyTracked', 'TRUE'),
    ('printTracked', 'FALSE'),
    ]

    response = requests.post('http://10.130.12.101/dummypost/xerox.set', headers=headers, cookies=cookies, data=data)

    logging.info("Disabled accounting")

########################################## End disable accounting

########################################## Begin job

cookies = {
    "PageToShow": "",
    "PHPSESSID": phpsessid,
    "propHierarchy": "1001000000000000000000000",
    "propNumNodes": "112",
	"propSelected":	"n29",
    "statusNumNodes": "8",
    "statusSelected": "n1",
    "WebTimerPopupID": "10"
}
files = {
    "_adm_SJ": (file_name, open(file_name, 'rb'), "application/pdf")
}

data = [
    ("NextPage", "/print/print.php?submitted=true"),
    ("job_type", "print"),
    ("plex", plex),
    ("default_medium", "unspecified"),
    ("CSRFToken", csrf_token)
]

requests.post("http://10.130.12.101/upload/xerox.set", cookies=cookies, data=data, files=files)
logging.info("Added job")

########################################## End job

########################################## Enable accounting

if not args.no_hack:
    cookies = {
        'PageToShow': '',
        'statusSelected': 'n1',
        'statusNumNodes': '8',
        'PHPSESSID': phpsessid,
        'WebTimerPopupID': '14',
        'propSelected': 'n29',
        'propNumNodes': '112',
        'propHierarchy': '0001000000000000000000000',
        'LastPage': '/aaa/acct/serviceAccessAndAccounting.php',
        'acctChoice': '-1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://10.130.12.101/aaa/acct/serviceAccessAndAccounting.php?from=Acct_Home',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    data = [
    ('_fun_function', 'HTTP_Set_FDI_Service_Enablement_fn'),
    ('scanTracked', 'TRUE'),
    ('faxTracked', 'TRUE'),
    ('NextPage', '/aaa/acct/serviceAccessAndAccounting.php'),
    ('CSRFToken', csrf_token),
    ('svcreg_id', '1'),
    ('svcreg_id', '2'),
    ('svcreg_id', '7'),
    ('copyTracked', 'TRUE'),
    ('printTracked', 'TRUE'),
    ]

    response = requests.post('http://10.130.12.101/dummypost/xerox.set', headers=headers, cookies=cookies, data=data)

    logging.info("Accounting enabled")

########################################## End enable accounting