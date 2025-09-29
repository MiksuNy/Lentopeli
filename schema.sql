ALTER TABLE game ADD quota INT;
ALTER TABLE game ADD balance INT;

CREATE TABLE owns_airport (
    airport_ident VARCHAR(40) NOT NULL,
    game_id VARCHAR(40) NOT NULL,
    PRIMARY KEY (airport_ident, game_id),
    FOREIGN KEY (airport_ident) REFERENCES airport(ident),
    FOREIGN KEY (game_id) REFERENCES game(id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

ALTER TABLE airport ADD cost INT;