## CRUD = Create, Read, Update, Delete
# This file contains the Read operations for the PricePoint model.
from .db import Session, PricePoint

def get_price_points():
    """Fetches all price points from the database."""
    session = Session()
    rows = session.query(PricePoint).order_by(PricePoint.date).all()
    session.close()
    return [{"date": r.date.isoformat(), "price": r.price} for r in rows]

def upsert_price_points(price_points):
    """Upserts a list of price points into the database.
    
    Args:
        price_points (list): List of dictionaries with 'date' and 'price' keys.
    """
    session = Session()
    for date, price in price_points.items():
        # Convert date string to datetime object
        exists = session.query(PricePoint).filter_by(date=date).first()
        if exists:
            exists.price = price
        else:
            new_pp = PricePoint(date=date, price=price)
            session.add(new_pp)
    session.commit()
    session.close()

def delete_price_point(date):
    """Deletes a price point by date.
    
    Args:
        date (str): The date of the price point to delete in ISO format.
    """
    session = Session()
    pp = session.query(PricePoint).filter_by(date=date).first()
    if pp:
        session.delete(pp)
        session.commit()
        print(f"Deleted price point for date: {date}")
    session.close()


