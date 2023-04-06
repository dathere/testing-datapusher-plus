import os
import requests
import json
from requests_toolbelt import MultipartEncoder
from time import sleep 
import pandas as pd
import csv
import configparser


srcdir = os.getenv('SRC_DIR')
#Read config.ini file
config_obj = configparser.ConfigParser()
config_obj.read("config.ini")
print(config_obj.sections())
setup = config_obj["setup"]
folder = setup["folder"]
API_URL = setup["API_URL"]
api_key = setup["api_key"]
base_url = setup["base_url"]
csv_url = setup["csv_url"]



# Define the function to find CSV files in a folder
def find_csv_files(folder):
    csv_files = []
    for file_name in os.listdir(folder):
        if file_name.endswith(".csv") or file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            file_path = os.path.join(folder, file_name)
            csv_files.append(file_path)
    return csv_files

def compare(id,name):
    response = requests.get(csv_url+id)
    filename = "data.csv"
    with open(filename, "wb") as f:
        f.write(response.content)

    # Load both CSV files into dataframes
    new_data = pd.read_csv(filename)
    old_data = pd.read_csv('/csvs/expected_output/'+id+'.csv')

    # Compare the two dataframes
    if new_data.equals(old_data):
        print(name + "Test case passed")
    else:
        print(name + "Test case failed")




def status(id):
    sleep(10)
    response = requests.get(base_url+id)
    result = json.loads(response.content.decode())["result"]

    if  result["datastore_active"]:
        print(f"Resource  is active")
        return True
    else:
        print(f"Resource is not active")
        return False

def expected_output(name):
    with open('data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Name'] == name:
                expected_op= row['Expected output']
                break 
    return expected_op

# Define the function to send a CSV file to the API


def action(api_url,file_path):
    file_name = os.path.basename(file_path)
    extention = os.path.splitext(file_name)[1][1:]
    print(extention)
    data_dict = {
                'package_id': setup["package_id"],
                'name': file_name,
                'description': "test",
                'format': extention,
                'url': '',
                'id': ''
            }

    file_dict = {
                'file_name': file_name,
                'path': file_path
            }
    fields = data_dict
    
    if file_dict:
        data_dict['upload'] = (
            file_dict.get('file_name'),
            open(os.path.abspath(file_dict.get('path')), 'rb'),
            'application/octet-stream'
        )
        fields = dict(data_dict)

    m = MultipartEncoder(fields=fields)
    r = requests.post(
        api_url + '/api/action/resource_create',
        data=m,
        headers={
            'content-type': m.content_type,
            'X-CKAN-API-Key': api_key
        }
    )
    json_data = r.json()
    if  json_data["success"] == True:
        print("success is True")
        id_value = json_data["result"]["id"]
        name = json_data["result"]["name"]
        print("ID value is:", id_value)
        expected_op = expected_output(name) 
        datastore=status(id_value)
        if datastore:
            compare(id_value,name)
        else :
            if expected_op == "invalid file":
                print(name + "Test case passed")
            else:
                print(name + "Test case Failed")

    else:
        print(" success is False")
    print("\n")


    return r

# Define the main function
def main():
    sleep(20)
    # Parse command-line arguments
    # Find CSV files in the folder
    csv_files = find_csv_files(folder)

    # Send each CSV file to the API
    for file_path in csv_files:
        response = action(API_URL, file_path)
        print(response)


if __name__ == "__main__":
    main()
