# Setup

## For Local Testing
There are a few prerequisites to take care of before this code will work locally.
- Drivers for mssql must be installed
    - Assuming the operating system is Linux, drivers can be found [here](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=azuresqldb-current)
- The sql.h headers must be present
    - In ubuntu these can be instaled via `sudo apt-get install -y unixodbc-dev`
    - The Microsoft docs consider this an optional installation, but the development headers will be necessary for pyodbc
- The local IP must be whitelisted in the database firewall settings