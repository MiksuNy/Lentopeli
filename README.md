
# Flight Game

The source tree for the Ohjelmisto 2 Flight Game project.


## Features
Currently implemented features include
- A fully functional Flask backend using MariaDB
- A frontend written in standard JS, rendered client-side
- A topographical world map using Leaflet
- Ratelimiting for the backend
- Server and database health check




## API Reference

### Player

#### Log in

```http
  POST /login/${username}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Your username |

Logs in as a specific user. Returns a `user_id`

#### Get username

```http
  GET /player/getScreenName/${user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user_id`      | `string` | **Required**. User ID |

Gets the username of the user associated with the user ID.

### Game

#### Next turn

```http
  POST /game/nextTurn/${user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user_id`      | `string` | **Required**. User ID |

Complete a turn for the user associated with the user ID.

### Airports

#### Get random set

```http
  GET /airports/getRandomSet
```

Get a random set on 100 airports. Used to populate the in-game store.

#### Get owned

```http
  GET /airports/getOwned/${user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. User ID |

Returns a list of all the owned airports for the user associated with the user ID.


#### Buy airport

```http
  POST /airports/buy/${airport_ident}/${user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|`airport_ident` | `string` | **Required**. Airport ICAO code |
| `id`      | `string` | **Required**. User ID |

Attempts to buy an airport as the user associated with the user ID.
Returns **200** on success, **403** on insufficient funds or an invalid ICAO code.

#### Get airport price

```http
  GET /airports/getPrice/${airport_ident}/${user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
|`airport_ident` | `string` | **Required**. Airport ICAO code |
| `id`      | `string` | **Required**. User ID |

Returns the price for the airport associated with the ICAO code.
Returns **200** on success, **403** for an invalid ICAO code.


### Airplanes

#### Create airplanes

```http
  POST /airplanes/create/${amount}/${user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `amount` | `int` | **Required**. Amount to create |
| `id`      | `string` | **Required**. User ID |

Creates a set amount of airplanes for purchase in the game associated with the user ID.

Called when a new game is registered into the database. Used to populate the in-game store.

#### Buy airplane

```http
  POST /airplanes/buy/${airplane_id}/${user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `airplane_id` | `string` | **Required**. Airplane ID |
| `id`      | `string` | **Required**. User ID |

Attempts to buy an airplane as the specified user.

Returns **200** on success, **403** on insufficient funds or an invalid airplane ID.

### Service status

#### Health check

```http
  GET /health
```

Returns a JSON object about the service health.
Returns **200** if the service is healthy, **503** if it isn't.

**Example response:**
```json
{
    "healthy": true,
    "status":
    {
        "database": true,
        "server": true
    }
}
```
## Deployment

#### Running the backend
The backend can be run by either executing the `run_server.sh` file or by running `python3 src/server.py`

#### Prerequisites

To deploy this project, first apply the new schema on top of the existing database provided by the teachers.

```bash
  mysql --host="mysql_server" --user="user_name" --database="database_name" --password="user_password" < "schema.sql"
```

Next, create a file called `.env` and populate it.

```bash
cat .env.example > .env
```

And change the fields to your host, username and password.

**It is recommended** to run the game behind a reverse proxy to avoid CORS- related errors.

The following is an example NGINX server block for the backend.
```
server {
    listen 80;
    server_name api.flight_game.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```


## Authors

- [@HEPOSHEIKKI](https://www.github.com/HEPOSHEIKKI) (Otto)
- [@MiksuNy](https://www.github.com/MiksuNy) (Mikael)
- [@skode7](https://www.github.com/skode7) (Teemu)

