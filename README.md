# enrollment-tools

Contains tools and scripts to clean daily enrollment file and add to postgres
database. To update the database daily, include the following in a script which
runs daily:

Functionality includes

+ Comparing daily sales to leadsheets to get attribution numbers
+ Converting and processing files
+ Extracting names and emails and adding them to specific mailing lists
+ Calculating attributed sales and creating report emails
+ Tools to connect to and update postgres database

Additional scripts needed to make these tools work together are not included
for security. Some features in those scripts include:

+ Pulling lead datasheets from google
+ Connecting to AWS S3 to access files
+ Writing results and backups to AWS S3 buckets

```
python insertEnrollments.py
```
