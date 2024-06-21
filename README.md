# pysqlpg_trading_solution
Project with solution of 3 sql/python hometasks that shows my level of coding and project organization
# Trade Data Preparation for ML Model

This project involves preparing trade data from a PostgreSQL database for a machine learning model. The database consists of information about client transactions across different types of trading systems. There are two schemas for two types of trading systems: mt4 and mt5.

## Schemas

### MT4 Schema
The mt4 schema contains the following tables:

- mt4.trades:
  - ticket: Primary key, transaction identifier
  - login: Client login who made the trade
  - opentime**: Trade opening time
  - **closetime: Trade closing time. If not closed, it has a zero timestamp.
  - symbol: Symbol, the instrument traded
  - cmd: 0 for buy, 1 for sell

- mt4.marked_trades:
  - ticket: Primary key, transaction identifier
  - type: Bitmask indicating the reason for marking the trade. Trades with the first bit of the mask set should not be considered.

### MT5 Schema
The mt5 schema contains the following tables:

- mt5.deals:
  - deal: Primary key, unique event identifier
  - positionid: Order number, unique transaction identifier
  - login: Client login who made the trade
  - time: Event time
  - symbol: Symbol, the instrument traded
  - action: 0 for buy, 1 for sell
  - entry: 0 for opening trade, 1 otherwise. Trades may have multiple closing events.

- mt5.marked_trades:
  - positionid: Primary key, transaction identifier
  - type: Bitmask indicating the reason for marking the trade. Trades with the first bit of the mask set should not be considered.

Note: If a trade does not have an opening event, it occurred before 2022-02-01. If a trade does not have a closing event, it occurred after 2022-02-08 00:00:00. If any trade does not clearly meet a condition, assume it does not meet it. Logins in different schemas are not related to each other.

## Objectives

Using Python and SQL, you need to compute:

1. For each user, count the number of trades where the time from opening to complete closing is less than one minute.
2. For each user, find the number of trade pairs that:
   - Were made by the same user
   - Have an opening time difference of no more than 30 seconds
   - Have opposite directions (one buy, one sell)
3. Divide all time into equal intervals of 30 seconds. Identify all pairs of users where:
   - Trades opened within the same time interval
   - Trades are for the same instrument
   - Trades belong to different users (one trade per user in the pair)
   - Trades have opposite directions (one buy, one sell)
   - More than 10 trades meet the above criteria within any interval

The script should generate:

1. A CSV file where each row corresponds to a login, with columns for login, metric from point 1, and metric from point 2.
2. A CSV file listing all pairs from point 3.

## How to use
### Clone repo
```
gh repo clone krds00/pysqlpg_trading_solution
```

### File structure
```
/pysqlpg_trading_solution
    ├── main.py 
    ├── app.py
    ├── queries.py
    ├── db.py
    ├── Dockerfile
    ├── requirements.txt
    ├── LICENSE
    ├── README.md
    ├── .gitignore
    ├── .env (should be added, see structure below)
    └── data/
```
### .env File

Create a .env file with the following format and fill in your database credentials:
```
DB_HOST=host
DB_PORT=port
DB_NAME=name
DB_USER=user
DB_PASSWORD=password
```

### Running App Individually
```
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Running Docker

1. Build the Docker image:

```
docker build -t transactions_processing-app .
```


2. Run the Docker container:

```
docker run -p 8000:8000 --env-file .env -v $(pwd)/data:/usr/src/app/data transactions_processing-app
```


3. Access your FastAPI application:

You can now access your FastAPI application at http://localhost:8000/run-main to execute the main function and check result in data/


