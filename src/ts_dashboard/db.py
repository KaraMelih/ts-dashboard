# src/ts_dashboard/db.py

from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Base class for all ORM models
Base = declarative_base()

# 2. The PricePoint model lives here so crud.py can import it directly
## Make a Data Model for the price points
class PricePoint(Base):
    __tablename__ = "price_points"
    id    = Column(Integer, primary_key=True, index=True)
    date  = Column(DateTime(timezone=True), unique=True, nullable=False)
    # date  = Column(Date, unique=True, nullable=False)
    price = Column(Float, nullable=False)

# 3. Engine pointing at your SQLite file
SQLITE_PATH = "data/btc.sqlite"
engine      = create_engine(f"sqlite:///{SQLITE_PATH}",
                            connect_args={"check_same_thread": False})  # for SQLite multithreading safety

# 4. Session factory
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Create tables if they don’t exist
Base.metadata.create_all(engine)
