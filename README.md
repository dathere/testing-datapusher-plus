# Tests for datapusher-plus



A Tool used to test datapusher plus

Clone the repo and edit the API key and URL endpoints

## Installation


To run this you need to have a dataset named "test_dataset" in your ckan instance
```bash
git clone https://github.com/dathere/testing-datapusher-plus.git
cd testing-datapusher-plus
nano test.py
pip install -r requirements.txt
python test.py
```
## Add Custom values
Change the values in config.ini
    
    
    
## Add files

To add custom test files to the test
```bash
 1) Add the files in the csvs folder 
 2) Add the processed files in the csvs/expected folder 
 3) Add the file name and expected output in the data.csv
 ```
