# enrollment-tools

Contains tools and scripts to manage daily sales and enrollments.

**Note:** All paths must be updated to reflect local environment

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

Future improvements:

+ Create a module containing re-used functions
+ Eliminate redundancy
+ Hide all paths in keyfiles, load as pickle
