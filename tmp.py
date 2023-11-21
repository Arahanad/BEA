import time
import requests
import pandas as pd

def pce_data_scraper(year_start,search_description):
    UserID = "A49E0CE2-D86C-4842-9C69-2D590202F4C0"
    size_in_mb = 0
    def add_field_to_dicts(lst, field_name, field_value):
        for d in lst:
            d[field_name] = field_value
            
    def move_dict_to_first(lst, key, value):
        index_to_move = next(
            (index for index, d in enumerate(lst) if d.get(key) == value), None
        )
        if index_to_move is not None:
            lst.insert(0, lst.pop(index_to_move))
    def convert_date(date_str):
        if "Q" in date_str:
            year, quarter = date_str.split("Q")
            end_of_quarter = pd.to_datetime(
                f"{year}-{int(quarter) * 3:02}-01"
            ) + pd.offsets.MonthEnd(0)
            return end_of_quarter.strftime("%Y-%m-%d")
        elif "M" in date_str:
            year, month = date_str.split("M")
            date = pd.to_datetime(f"{year}-{month}", format="%Y-%m")
            end_of_month = date + pd.offsets.MonthEnd(0)
            return end_of_month.strftime("%Y-%m-%d")
        else:
            end_of_year = pd.to_datetime(date_str + "-12-31")
            return end_of_year.strftime("%Y-%m-%d")
    def convert_freq(date_str):
        if "Q" in date_str:
            return "Q"
        elif "M" in date_str:
            return "M"
        else:
            return "A"
    
    master = pd.DataFrame()
    results = []
    response = requests.post(
        f"https://apps.bea.gov/api/data?UserID={UserID}&method=GetParameterValues&datasetname=NIUnderlyingDetail&ParameterName=TableName"
    )
    tableData1 = response.json()["BEAAPI"]["Results"]["ParamValue"]
    add_field_to_dicts(tableData1, "dataset", "NIUnderlyingDetail")
    response = requests.post(
        f"https://apps.bea.gov/api/data?UserID={UserID}&method=GetParameterValues&datasetname=NIPA&ParameterName=TableName"
    )
    tableData2 = response.json()["BEAAPI"]["Results"]["ParamValue"]
    add_field_to_dicts(tableData2, "dataset", "NIPA")
    # tableData1 = []
    tableData = tableData1 + tableData2
    move_dict_to_first(tableData, "TableName", "U20405")
    response = requests.post(
        f"https://apps.bea.gov/api/data?UserID={UserID}&method=GetParameterValues&datasetname=NIUnderlyingDetail&ParameterName=year"
    )
    frequencyData = response.json()["BEAAPI"]["Results"]["ParamValue"]
    response = requests.post(
        f"https://apps.bea.gov/api/data?UserID={UserID}&method=GetParameterValues&datasetname=NIPA&ParameterName=year"
    )
    frequencyData += response.json()["BEAAPI"]["Results"]["ParamValue"]
    result = None
    for item in tableData:
        if item["Description"] == search_description:
            result = item
            break

    if result:
        table_name = result["TableName"]
        print(table_name)
        dataset = result["dataset"]
    else:
        print("Table not found for the given description:", search_description)
        return pd.DataFrame()
    frequencies = list(
        filter(
            lambda frequency: frequency["TableName"] == table_name, frequencyData
        )
    )[0]
    collection = []
    if (
        frequencies["FirstAnnualYear"] != "0"
        and int(frequencies["LastAnnualYear"]) >= year_start
    ):
        l = [
            str(x)
            for x in (
                range(
                    year_start,
                    int(frequencies["LastAnnualYear"]) + 1,
                )
            )
        ]
        collection.extend(l)
    if (
        frequencies["FirstQuarterlyYear"] != "0"
        and int(frequencies["LastQuarterlyYear"]) >= year_start
    ):
        l = [
            str(x)
            for x in (
                range(
                    year_start,
                    int(frequencies["LastQuarterlyYear"]) + 1,
                )
            )
        ]
        collection.extend(l)
    if (
        frequencies["FirstMonthlyYear"] != "0"
        and int(frequencies["LastMonthlyYear"]) >= year_start
    ):
        l = [
            str(x)
            for x in (
                range(
                    year_start,
                    int(frequencies["LastMonthlyYear"]) + 1,
                )
            )
        ]
        collection.extend(l)
    collection = list(set(collection))
    if collection == []:
        return "No data found."
    
    try:
        f = "AQM"
        y = ",".join(collection)
        url = f"https://apps.bea.gov/api/data/?UserID={UserID}&method=GetData&DataSetName={dataset}&TableName={table_name}&Frequency={f}&Year={y}&ResultFormat=json"
        response = requests.get(url)
        size_in_bytes = len(response.content)
        size = size_in_bytes / (1024 * 1024)
        size_in_mb += size
        if size > 100:
            time.sleep(60)
        data = response.json()["BEAAPI"]
        if "Error" not in data:
            res = data["Results"]["Data"]
            add_field_to_dicts(res, "Table Name", result["Description"])
            results += res
        else:
            # print("Error",data)
            # break
            pass
    except Exception as e:
        # print(e)
        pass
    df = pd.DataFrame(results)
    df.insert(loc=1, column="Frequency", value="")
    df["Frequency"] = df["TimePeriod"].apply(convert_freq)
    df["TimePeriod"] = df["TimePeriod"].apply(convert_date)
    df.to_csv("data.csv", index=False)


    return df

if __name__ == "__main__":
    # print(pce_data_scraper(year_start))
    # result_df = pce_data_scraper(1998, "Table 2.3.6U. Real Personal Consumption Expenditures by Major Type of Product and by Major Function (A) (Q) (M)")
    # result_df = pce_data_scraper(1998, "Table 2.3.6U. Real Personal Consu")
    result_df = pce_data_scraper(2555, "Table 2.4.3U. Real Personal Consumption Expenditures by Type of Product, Quantity Indexes (A) (Q) (M)")

    if not result_df.empty:
        print(result_df.head())
    else:
        print("No data found.")