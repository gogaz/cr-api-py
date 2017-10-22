import pytest
import asyncio

from cr_api import Client


@pytest.mark.asyncio
async def test_profile():
    client = Client()
    player = await client.get_profile('C0G20PR2')
    print(player)
    assert player.name == 'SML'
    assert player.tag == 'C0G20PR2'
    assert player.clan_name == 'Reddit Delta'
    assert player.clan_role == 'Leader'


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(test_profile())
