CREATE SCHEMA coguild;

CREATE TABLE coguild.Users (
    discordId VARCHAR(255) NOT NULL PRIMARY KEY,
    apiKey VARCHAR(255) NOT NULL,
    createdDate timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE coguild.Kills (
    discordId VARCHAR(255) REFERENCES coguild.Users (discordId) NOT NULL,
    raidDay DATE DEFAULT CURRENT_DATE NOT NULL,
    kills INTEGER NOT NULL,
    PRIMARY KEY (discordId, raidDay)
);