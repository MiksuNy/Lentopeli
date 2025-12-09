ALTER TABLE game ADD quota INT;
ALTER TABLE game ADD balance INT;
ALTER TABLE game ADD turns INT;

CREATE TABLE owns_airport (
    airport_ident VARCHAR(40) NOT NULL,
    game_id VARCHAR(40) NOT NULL,
    PRIMARY KEY (airport_ident, game_id),
    FOREIGN KEY (airport_ident) REFERENCES airport(ident),
    FOREIGN KEY (game_id) REFERENCES game(id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

ALTER TABLE game ADD seed BINARY(64);

CREATE TABLE airplane (
    id VARCHAR(40) NOT NULL,
    game_id VARCHAR(40) NOT NULL,
    airport_ident VARCHAR(40),
    airplane_type VARCHAR(40) NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (game_id) REFERENCES game(id),
    FOREIGN KEY (airport_ident) REFERENCES airport(ident)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

CREATE TABLE owns_airplane (
    airplane_id VARCHAR(40) NOT NULL,
    game_id VARCHAR(40) NOT NULL,
    PRIMARY KEY (airplane_id, game_id),
    FOREIGN KEY (airplane_id) REFERENCES airplane(id),
    FOREIGN KEY (game_id) REFERENCES game(id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;