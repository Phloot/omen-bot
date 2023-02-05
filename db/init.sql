CREATE SCHEMA coguild;

CREATE TABLE coguild.users (
    discord_id VARCHAR(255) NOT NULL PRIMARY KEY,
    api_key VARCHAR(255) NOT NULL,
    created_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE coguild.kills (
    discord_id VARCHAR(255) REFERENCES coguild.users (discord_id) NOT NULL,
    raid_day DATE DEFAULT CURRENT_DATE NOT NULL,
    kills INTEGER NOT NULL,
    PRIMARY KEY (discord_id, raid_day)
);