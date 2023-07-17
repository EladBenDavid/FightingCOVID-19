Home Assignment - Fighting COVID-19

In the attached CSV file ***weathersource\_israel\_feb\_aug\_2020.csv*** you will find daily temperature & humidity stats for different postal codes in Israel.

Using this data, we would like to assist cities to fight COVID-19 by alerting on critical temperature & humidity rises.

1. For each **postal\_code** & **date** in the given data file calculate the following:
1. AVG humidity delta from the day before
1. AVG temperature delta from the day before

Example:

Each 2 leading rows like this:

|date|postal\_code|avg\_temperature|avg\_humidity|
| - | - | - | - |
|2020-01-01|1111|90|40|
|2020-01-02|1111|80|38|

Will become:

|date|postal\_code|delta\_tempreture\_previous \_day|delta\_humidity\_previous\_day|
| - | - | :- | - |
|2020-01-02|1111|-10|-2|

2. Split the results so each **post\_code** data has its own file, the format of the output files shouldn’t be “CSV”, but “NEWLINE DELIMITED JSON”

Example: **CSV:**

Date,postal\_code,delta\_tempreture\_previous\_day,delta\_humidity\_previous\_day 2020-01-02,1111,-10,-2

2020-01-03,1111,-15,-6

…

Should transform to

**NEWLINE DELIMITED JSON:**

{“date”: “2020-01-02”, “postal\_code”: 1111, “delta\_tempreture\_previous\_day”: -10 ,”delta\_humidity\_previous\_day”: -2} {“date”: “2020-01-02”, “postal\_code”: 1111, “delta\_tempreture\_previous\_day”: -15 ,”delta\_humidity\_previous\_day”: -6} …

The output file names should look like this (1 result file per postal\_code): COVID-WEATHER-<postal\_code>-FEB-AUG-2020.json

Example: COVID-WEATHER-11111-FEB-AUG-2020.json COVID-WEATHER-12233-FEB-AUG-2020.json

…

Write the output files to your local PC.

3. Learn how to use this python package - [https://pythonhosted.org/PyDrive/quickstart.html ](https://pythonhosted.org/PyDrive/quickstart.html)(It’s a nice package that will help us upload the output files to Google Drive!)
3. Write a code that uploads the output **.json** files to your own Google Drive
