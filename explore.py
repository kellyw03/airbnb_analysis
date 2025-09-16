from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine
from data_setup import create_connection
from typing import List, Tuple, Dict, Optional
import pandas as pd
import seaborn

# select count
# summarize

# Loads data from database
def load_data(engine: Engine) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Loads data from tables as pd dataframes
    """
    with engine.connect() as conn:
        listings_df = pd.read_sql("SELECT * from listings", conn)
        neighborhood_df = pd.read_sql("SELECT * from neighborhoods", conn)
        groups_df = pd.read_sql("SELECT * from neighborhoodgroups", conn)
        review_df = pd.read_sql("SELECT * from reviews", conn)
    return listings_df, neighborhood_df, groups_df, review_df



def main():
    engine = create_connection()
    listings_df, neighborhood_df, groups_df, review_df = load_data(engine)


if __name__ == "__main__":
    main()