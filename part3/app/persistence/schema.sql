CREATE TABLE "User" (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    CONSTRAINT fk_owner FOREIGN KEY (owner_id) REFERENCES "User"(id) ON DELETE SET NULL
);

CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    reservation_id CHAR(36) NOT NULL,
    CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES "User"(id) ON DELETE CASCADE,
    CONSTRAINT fk_review_place FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    CONSTRAINT fk_review_reservation FOREIGN KEY (reservation_id) REFERENCES Reservation(id) ON DELETE CASCADE, 
    CONSTRAINT unique_user_place_reservation_review UNIQUE (user_id, place_id, reservation_id)
);

CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);


CREATE TABLE Reservation (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    CONSTRAINT fk_reservation_user FOREIGN KEY (user_id) REFERENCES "User"(id) ON DELETE CASCADE,
    CONSTRAINT fk_reservation_place FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    CONSTRAINT chk_dates CHECK (start_date <= end_date)
);

-- Insert admin user
INSERT INTO "User" (id, email, first_name, last_name, password, is_admin) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbc1',
 'admin@hbnb.io',
 'Admin',
 'HBnB',
 '$2b$12$4S2x7aZHL0Hw6Ym6YpA6RO1kk12o2JplOeQ0V4Jq1px5x9o9aVYx6', -- mot de passe "admin1234" hashé
 TRUE
);

-- Insert amenities
INSERT INTO Amenity (id, name) VALUES
('e7a1f2f4-9d5c-4e5b-9918-7d9f3293b06a', 'Wifi'),
('c0b6a1bc-8838-4e7b-b1c7-03d69103f61d', 'Piscine'),
('8a5d4f7b-63a9-42b6-8c2e-02cdbb4b2d9f', 'Climatisation');

