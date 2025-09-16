CREATE TABLE IF NOT EXISTS NeighborhoodGroups (
    group_id SERIAL PRIMARY KEY,
    group_name TEXT
);

CREATE TABLE IF NOT EXISTS Neighborhoods (
    neighborhood_id SERIAL PRIMARY KEY,
    neighbourhood TEXT,
    group_id int REFERENCES NeighborhoodGroups(group_id)
);

CREATE TABLE IF NOT EXISTS Listings (
    id BIGINT,
    name TEXT,
    host_id int,
    host_name TEXT,
    neighbourhood_group_id int REFERENCES NeighborhoodGroups(group_id),
    neighbourhood_id int REFERENCES Neighborhoods(neighborhood_id),
    latitude NUMERIC,
    longitude NUMERIC,
    room_type TEXT,
    price NUMERIC,
    minimum_nights int,
    number_of_reviews int,
    last_review Date,
    reviews_per_month NUMERIC,
    calculated_host_listings_count int,
    availability_365 int,
    number_of_reviews_ltm int,
    license TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Reviews (
    review_id SERIAL PRIMARY KEY,
    listing_id BIGINT,
    date Date,
    FOREIGN KEY (listing_id) REFERENCES Listings(id)
);
