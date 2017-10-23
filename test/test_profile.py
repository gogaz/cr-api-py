import pytest

from cr_api import Client


@pytest.mark.asyncio
async def test_profile():
    client = Client()
    player = await client.get_profile('C0G20PR2')
    assert player.name == 'SML'
    assert player.tag == 'C0G20PR2'
    assert player.clan_name == 'Reddit Delta'
    assert player.clan_role == 'Leader'
