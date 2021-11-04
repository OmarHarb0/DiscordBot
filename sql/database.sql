CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    steamid32 BIGINT,
    steamid64 BIGINT,
    url TEXT
);

CREATE TABLE heroes (
    id SMALLINT PRIMARY KEY,
    name TEXT
);


SELECT * FROM users;

DELETE FROM users WHERE id=144456358996082688;
