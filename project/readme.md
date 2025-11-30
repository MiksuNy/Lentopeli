`POST /login/<username>`

Kirjaa käyttäjän sisään ja palauttaa pelitilan.

Jos käyttäjää ei ole olemassa, luo uuden käyttäjän ja palauttaa uuden pelitilan.


login(username) return value

Success Response
```{
    "newUser": true/false,
    "gameState": {
    "name": string,
    "id": string,
    "co2Consumed": int,
    "co2Budget": int,
    "startingIcao": string,
    "startingPortMeta": {
        "airportName": null,
        "countryName": null
    },
    "quota": null,
    "balance": int,
    "messages": [
        {
            "type": string,
            "text": string
        }
    ],
    "ownsAirport": []
}
```

Error Response
```
{
    "Error": error
}
```