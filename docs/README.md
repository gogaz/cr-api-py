# crapipy

This is a Python wrapper (synchronous and asynchronous) for [cr-api](http://github.com/cr-api/cr-api). See http://docs.cr-api.com for documentation on the expected fields.

## Installation

Install via pip:

```sh
pip install crapipy
```

## Developer key

You will need a developer key from http://cr-api.com to work with this client. See [cr-api docs: Authentication](http://docs.cr-api.com/#/authentication) for details on how to obtain one.

You can authenticate by either setting an environment variable called TOKEN or pass your token to the client.

## How to use

You can access data using blocking or async code. Internally, the wrapper uses the [requests](docs.python-requests.org) library for blocking code and the [aiohttp](aiohttp.readthedocs.io) library for async code.

To initiate a client for connection:

### Blocking

```python
from crapipy import Client
client = Client(token='a1234b2345')
```

### Async

```python
from crapipy import AsyncClient
client = AsyncClient(token='a1234b2345')
```

## Methods

Both the blocking and async client uses the same method names. 

```python
player = client.get_player('C0G20PR2')
```

The object returned allow you to access the JSON returned as dict or dot notation.

- dict: `player['arena']['arenaID']`
- attribute as CamelCaseKeys: `player.arena.arenaID`
- attribute as snake_case_attributes: `player.arena.arena_id`

Additionally, you can use:

- `to_dict()`: to read as dictionary
- `to_json()`: to convert back into JSON
- `to_yaml()`: to convert into YAML

### get_clan(tag)

### get_clans(tags)

### get_player(tag)

### get_players(tags)

### get_constants()


## Examples

### Non-Async

```python
from crapipy import Client

def main():
    client = Client()

    # get player profile
    player = client.get_player('C0G20PR2')
    assert player.name == 'SML'
    assert player.tag == 'C0G20PR2'
    assert player.clan.name == 'Reddit Delta'
    assert player.clan.role.lower() == 'leader'
    assert player.clan_name == player.clan.name
    assert player.clan_role == player.clan.role
    assert player.current_deck is not None
    assert player.arena.arena_id == player.arena.arenaID
    assert player.arena.arena_id is not None

    # profile equality
    player1 = client.get_player('C0G20PR2')
    player2 = client.get_player('C0G20PR2')
    assert player1 == player2

    # profile inequaity
    player1 = client.get_player('C0G20PR2')
    player2 = client.get_player('PY9VC98C')
    assert player1 != player2

    # get clan
    clan = client.get_clan('2CCCP')
    assert clan.name == 'Reddit Alpha'
    assert clan.badge.name == 'A_Char_Rocket_02'

    # multiple clans
    clans = client.get_clans(['2CCCP', '2U2GGQJ'])
    assert clans[0].name == 'Reddit Alpha'
    assert clans[0].badge.name == 'A_Char_Rocket_02'
    assert clans[1].name == 'Reddit Bravo'
    assert clans[1].badge.name == 'A_Char_Rocket_02'

main()
```

### Async

```python
import asyncio
from crapipy import AsyncClient

async def main():
    client = AsyncClient()

    # get player profile
    player = await client.get_player('C0G20PR2')
    assert player.name == 'SML'
    assert player.tag == 'C0G20PR2'
    assert player.clan.name == 'Reddit Delta'
    assert player.clan.role.lower() == 'leader'
    assert player.clan_name == player.clan.name
    assert player.clan_role == player.clan.role
    assert player.current_deck is not None
    assert player.arena.arena_id == player.arena.arenaID
    assert player.arena.arena_id is not None

    # profile equality
    player1 = await client.get_player('C0G20PR2')
    player2 = await client.get_player('C0G20PR2')
    assert player1 == player2

    # profile inequaity
    player1 = await client.get_player('C0G20PR2')
    player2 = await client.get_player('PY9VC98C')
    assert player1 != player2

    # get clan
    clan = await client.get_clan('2CCCP')
    assert clan.name == 'Reddit Alpha'
    assert clan.badge.name == 'A_Char_Rocket_02'

    # multiple clans
    clans = await client.get_clans(['2CCCP', '2U2GGQJ'])
    assert clans[0].name == 'Reddit Alpha'
    assert clans[0].badge.name == 'A_Char_Rocket_02'
    assert clans[1].name == 'Reddit Bravo'
    assert clans[1].badge.name == 'A_Char_Rocket_02'


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

```


## Tests

This package uses [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) for tests.

Run all tests:

```sh
pytest
```



