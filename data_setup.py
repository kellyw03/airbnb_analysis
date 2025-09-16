from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

## Sets up and imports in data from csvs into sql tables

#psql -h airbnb.cb8ei06oo8wd.us-east-2.rds.amazonaws.com -U postgres -d airbnb
db_host = "airbnb.cb8ei06oo8wd.us-east-2.rds.amazonaws.com"
db_port = "5432"
db_name = "airbnb"
db_user = "postgres"
db_pass = "N0thoughts!"


# creates a connection and returns a SQLAlchemy engine
def create_connection():
    return create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")  

# creates tables from sql make file
def create_tables(engine):
    try:
        with engine.connect() as conn:
            with open("airbnb-table.sql", "r") as f:
                conn.execute(text(f.read()))
            print("Tables created successfully")
    except SQLAlchemyError as e:
        print("Error creating tables", e)
        
# map neighborhood groups and neighborhoods to ids
def map_neighborhoods(neigh_df):
    # assign group_id to each unique neighbourhood_group
    groups = neigh_df['neighbourhood_group'].unique()
    group_map = {name: idx+1 for idx, name in enumerate(groups)}

    #match schema of NeighborhoodGroups 
    neigh_group_df = pd.DataFrame({
        "group_id": list(group_map.values()),
        "group_name": list(group_map.keys())
    })

    #assign neighborhood_id to each neighborhood
    neigh_df['group_id'] = neigh_df['neighbourhood_group'].map(group_map)
    neigh_df['neighborhood_id'] = range(1, len(neigh_df)+1)

    # match schema of Neighborhoods table
    neighbourhoods_final = neigh_df[['neighborhood_id', 'neighbourhood','group_id']]
    
    return neigh_group_df, neighbourhoods_final
    
# map and replace neighbourhood_group and neighbourhood column with ids
def map_listings(listings_df,group_df,neighbourhood_df):
    listings_df = listings_df.copy()
    #create mappings of neighbourhood and group
    group_mapping = dict(zip(group_df['group_name'], group_df['group_id']))
    neighborhood_mapping = dict(zip(neighbourhood_df['neighbourhood'], neighbourhood_df['neighborhood_id']))

    #map columns in listings to id
    listings_df['neighbourhood_group_id'] = listings_df['neighbourhood_group'].map(group_mapping)
    listings_df['neighbourhood_id'] = listings_df['neighbourhood'].map(neighborhood_mapping)

    listings_df = listings_df.drop(columns=['neighbourhood_group', 'neighbourhood'])
    return listings_df

def main():
    engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")    
    create_tables(engine)

    # load csv
    listings_df = pd.read_csv("listings.csv")
    neigh_df = pd.read_csv("neighbourhoods.csv")
    review_df = pd.read_csv("reviews.csv")

    #transform neighborhoods to ids
    group_df, neighbourhood_df = map_neighborhoods(neigh_df)
    listings_df = map_listings(listings_df, group_df, neighbourhood_df)
    #print(neighbourhood_df)
    #print(group_df)

    with engine.connect() as conn:
        #insert into db
        if conn.execute(text("SELECT COUNT(*) FROM neighborhoodgroups")).scalar() == 0:
            group_df.to_sql("neighborhoodgroups", engine, if_exists="append", index=False)
            neighbourhood_df.to_sql("neighborhoods", engine, if_exists="append", index=False)
            listings_df.to_sql("listings", engine, if_exists="append", index=False)
            review_df.to_sql("reviews", engine, if_exists="append", index=False)

if __name__ == "__main__":
    main()
