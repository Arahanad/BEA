import requests
import json
import csv

class MAIN():

    def __init__(self) -> None:
        with open('data.json', 'r') as input:
            self.data = json.load(input)

    def get_data(self):
        for i, item in enumerate(self.data, start=1):
            print(f'{i}. {item["Description"]}')
        
        table_number = int(input("Enter the Table Number of Names: "))
        Frequency = input("Enter the Value OF Frequency: ")
        year = input("Enter the Year :")

        if 1 <= table_number <= len(self.data):
            table = self.data[table_number - 1]
            table_name = table["TableName"]
            url = f"https://apps.bea.gov/api/data/?UserID=A49E0CE2-D86C-4842-9C69-2D590202F4C0&method=GetData&DataSetName=NIUnderlyingDetail&TableName={table_name}&Frequency={Frequency}&Year={year}&ResultFormat=json"
            print(f"URL: {url}")

            response = requests.get(url)
            data = response.json()['BEAAPI']

            if 'Error' in data:
                error_description = data['Error']['ErrorDetail']['Description']
                print(error_description)
            
            else:
                datas =[]
                table_data = data['Results']['Data']
                for li in table_data:
                    datas.append(li)
                print(len(datas))
                filename = f'{table_name}.csv'
                with open(filename, 'w', newline='') as csv_file:
                    fieldnames = datas[0].keys()
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in datas:
                        writer.writerow(row)  
        else:
            print("Invalid table number. Please enter a valid number.")

if __name__ == "__main__":
    MAIN().get_data()
