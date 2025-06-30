# Time Series Dashboard

A simple project to practice SQLAlchemy, FastAPI and Dockerization concepts <br>
Also will expand it to include CI/CD practices, and pydantic.

The idea is to create a simple timeseries dashboard where it fetches the latest BTC data and plots a simple chart. <br>
Later some extra complications can be added to explore better visualization and interaction.

## How to run

Upon startup the FastAPI's `asynccontextmanager` uses `lifespan` protocol to populate the database, this calls the `populate_db()` function. The database can also be populated manually by calling the following;
```python
from scripts.fetch_btc_data import populate_db
populate_db() ## internally calls crud.upsert()
```

which fetches the BTC data of the last 5 days with hourly intervals and updates/inserts them into the `sqlite` database. 

The insert, update, delete operations are handled by `src.ts_dashboard.crud` script. <br>
database operations like defining a data model, creating the connection with the sqlite and SQLAlchemy (python library) are defined in `src.ts_dashboard.db` and the main app is defined in `src.ts_dashboard.main` using FastAPI tools. 

To run the app, call `uvicorn ts_dashboard.main:app --host 0.0.0.0 --port 8000` from the terminal. Which than enters in the FastAPI app and hosts this app on your local machine at the `0.0.0.0` and binds the 8000th port. (`0.0.0.0` can be accessed by other apps in the network including docker, for fully local, use host `127.0.0.1`)


## Things to do

- CI/CD pipelines
- test cases
- pydantic models
- more complex data models, metrics
