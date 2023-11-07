import json
import requests

class BEA():

    def __init__(self) -> None:
        self.url = 'https://apps.bea.gov/api/data?UserID=A49E0CE2-D86C-4842-9C69-2D590202F4C0&method=GetParameterValues&datasetname=NIUnderlyingDetail&ParameterName=TableName'

    def get_table_name(self):
        tablename = []
        response = requests.post(self.url)
        print(response)
        data = response.json()['BEAAPI']['Results']['ParamValue']
        with open ('data.json' ,'w' ,encoding='utf-8') as input:
            json.dump(data,input,indent=4)


if __name__ == "__main__":
    BEA().get_table_name()