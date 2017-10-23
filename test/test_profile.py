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


@pytest.mark.asyncio
async def test_profile_equal():
    client = Client()
    player1 = await client.get_profile('C0G20PR2')
    player2 = await client.get_profile('C0G20PR2')
    assert player1 == player2


@pytest.mark.asyncio
async def test_profile_not_equal():
    client = Client()
    player1 = await client.get_profile('C0G20PR2')
    player2 = await client.get_profile('PY9VC98C')
    assert player1 != player2
