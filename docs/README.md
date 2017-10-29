# cr-api-py

This is an async Python wrapper for [cr-api](http://github.com/cr-api/cr-api). See http://docs.cr-api.com for documentation on the expected fields.

## Installation

Install via pip:

```sh
pip install cr-api
```

## How to use

The models allow you to read fields from the API JSON using dot syntax. Camel case properties are converted into name_with_underscore.


### Non-Async

```python
from cr_api import Client

client = Client()

# get clan
clan = client.get_clan('2CCCP')
print(clan.name)
print(clan.badge.key)

# get player profile
player = client.get_profile('C0G20PR2')
print(player.name)
print(player.tag)
```

### Async

```python
import asyncio
from cr_api import AsyncClient

async def main():
    client = AsyncClient()
    # get clan
    clan = await client.get_clan('2CCCP')
    print(clan.name)
    print(clan.badge.key)

    # get player profile
    player = await client.get_profile('C0G20PR2')
    print(player.name)
    print(player.tag)

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



