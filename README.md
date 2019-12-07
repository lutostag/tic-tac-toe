![tic-tac-toe picture](https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Tic_tac_toe.svg/200px-Tic_tac_toe.svg.png)

# Tic-Tac-Toe
A simple but comprehensive REST API for a [tic-tac-toe game](https://en.wikipedia.org/wiki/Tic-tac-toe)

## Quickstart

Get the code first:
```bash
git clone https://github.com/lutostag/tic-tac-toe
cd tic-tac-toe
```

Using docker:
```bash
docker-compose up
```

If you prefer a non-docker workflow, **please be in a virtual environment running Python3.7**:
```bash
make deps dev
```

In your browser, navigate to:
* http://localhost/redoc for documentation
* http://localhost/docs for a swagger ui that you can use to interact with REST-API via your browser.

(note that if you are not using docker, the dev server is typically listening on port :8000)

## Sceenshots
![Redoc Screenshot](https://i.imgur.com/keisUzI.png)
![Swagger Screenshot](https://i.imgur.com/9nV3gOh.png)

## Introduction

This project implements a REST API for playing [tic-tac-toe](https://en.wikipedia.org/wiki/Tic-tac-toe)

All game state is saved and can be viewed/returned to whenever the players want to.

Game state transitions are validated to prevent clients from cheating and operating out of turn.

Players can enter their names, the first player to join is 'x', the second is 'o'.

## Technologies

[Python 3](https://www.python.org/) -- language that has good support for backend servers

Backend:
* [FastAPI](https://fastapi.tiangolo.com/) -- a relatively new framework, taking it for a spin for the first time. I agree with a lot of the [sentiments](https://fastapi.tiangolo.com/alternatives/), and is asyncio friendly in implementation.
* [Pydantic](https://pydantic-docs.helpmanual.io/) -- a full featured data modelling framework, very helpful for validation and data wrangling into and out of ORMs, first time using this one as well.
* [SQLAlchemy](https://www.sqlalchemy.org/) for talking with the database -- in this case using [SQLite](https://sqlite.org/) for local development and [PostgreSQL](https://www.postgresql.org/) or any other SQL backend. The challenge may be better suited to a non-SQL database, but with the validation of progression, using transactions was important, and given there were already lots of new tools to learn, sticking with these tools made it easier to spin up, and introspect for development.

Testing:
* [Requests](https://2.python-requests.org/en/master/) -- a great http client (only missing asyncio for speed), but great for flexible testing
* [Pytest](https://docs.pytest.org/) -- really useful for dealing with test parameterization

Deployment:
* [Docker](https://en.wikipedia.org/wiki/Docker_%28software%29) -- using [docker-compose](https://docs.docker.com/compose/) to ensure that the server can be built/run on different machines without too much hassle

## Data Representation and validation

As there only one type of data (games) exposed by this API, making a good representation of it is important.

The game objects use the following format that is exposed to the clients via the endpoints:
```json
{
  "players": [
    "one",
    "two"
  ],
  "state": [
      [null, null, 0],
      [null, null, null],
      [null, null, 1]
  ]
}
```

On every update of the state of a game validation is performed to ensure that only valid tic-tac-toe moves occur. This ensures that clients cannot "cheat" by sending multiple moves or skip turns.


## API
The server complies with the JSON API specification, in this case exposing an [OpenAPI](https://www.openapis.org/) (formerly know as [swagger](https://swagger.io/) -- it switched names in the v2 -> v3 transition).

- `GET /api/games`: Return a list of the Games known to the server, as JSON.

- `POST /api/games`: Create a new `Game`, assigning it an ID and returning the newly created `Game`.

- `GET /api/games/<id>`: Retrieve a `Game` by its ID, returning a `404` status code if no game with that ID exists.

- `POST /api/games/<id>`: Update the `Game` with the given ID, replacing its data with the newly `POST`ed data.

## Clients

Since the openapi definition is exposed you can create a client by using tooling such as:
* https://github.com/OpenAPITools/openapi-generator
* https://github.com/anttiviljami/openapi-client-axios

## Contributing/Workflows

Most of the common workflows, (development/hot-reloading server, testing, running) are usable via `make`

Setup your workspace:
* python3.7
* be in a virtualenv
* `make deps # to install depenencies`
* `make dev # to start a hot-reloading dev server`

Typical workflow:
* create a new branch on git
* make any desired changes
* add tests to `tests/`
* `make fmt # to reformat your code using black`
* `make test # to test your code is working`
* push and submit the code as a PR -- note the upstream repo where the idea came from is https://github.com/ContinuumIO/tic-tac-toe-challenge

Notes:
* you can point the tests at a different server by setting the `TICTACTOE_SERVER` environment variable, e.g. `TICTACTOE_SERVER=http://localhost make test` this is typically helpful to test against the docker container or other already deployed servers.

## Future Ideas

* Setup CI
* Utilize redis for only holding on to in-progress games with a 5min TTL, then games can optionally be saved to the backend database if desired by clients.
* Alert clients on turns via websockets, so clients do not have to poll.
* A terminal tui client, perhaps using [urwid](http://urwid.org/)
