# **README - BEA Data Retrieval**

This code is designed to fetch data from the Bureau of Economic Analysis (BEA) API. It consists of two Python scripts: Table_data.py and main.py. The Table_data.py script is responsible for retrieving a list of available table names and storing them in a JSON file. The main.py script allows you to select a table, specify the frequency and year, and retrieve data in CSV format for the chosen table.

**Prerequisites**

Before running the code, ensure you have the following dependencies installed:

Python 3.x
Required Python libraries: 

**requests**
**json** 
**csv** 

**Usage**

Follow these steps to run the code:

1. Clone or download the repository to your local machine.

2. Open a terminal or command prompt.

3. Navigate to the directory where the code is located.

4. Run Table_data.py to retrieve a list of available table names and save them to a JSON file. Execute the following command:

```python Table_data.py```

This step will create a file named data.json containing a list of table names.

5. Run main.py to fetch data for a specific table, frequency, and year and save it as a CSV file. Execute the following command:

```python main.py```

Follow the on-screen instructions to select a table, specify the frequency, and provide the year.

6. The script will generate a CSV file with the data from the chosen table. The file will be named after the selected table and will be saved in the same directory as the code.

