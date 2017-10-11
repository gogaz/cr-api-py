"""
Unified module to call api for data.
In the beginning managers were used but this became problematic
when multiple classes need to access these endpoints.
"""
import aiohttp
import async_timeout
import yaml
import asyncio
from box import Box

from .models import SCTag

config = None


def init(yaml_config=None):
    global config
    with open(yaml_config, "r") as f:
        config = Box(yaml.load(f))


async def fetch(session, url):
    """Fetch URL.

    :param session: aiohttp.ClientSession
    :param url: URL
    :return: Response in JSON
    """
    try:
        with async_timeout.timeout(config.app.async_timeout):
            async with session.get(url) as response:
                return await response.json()
    except asyncio.TimeoutError:
        return None
    except aiohttp.client_exceptions.ClientResponseError:
        return None

async def fetch_clan(clan_tag, include_members=True):
    """Fetch a single clan."""
    url = '{api_url}/{members}'.format(
        api_url=config.api.clan.clan_fmt.format(clan_tag),
        members='' if include_members else '?members=0'
    )
    print(url)
    async with aiohttp.ClientSession() as session:
        # url = self.clan_api_url(clan_tag)
        data = await fetch(session, url)
        if isinstance(data, list):
            data = data[0]
        return data


async def fetch_multi_clans(clan_tags, include_members=True):
    """Fetch multiple clans.

    :param clan_tags: List of clan tags
    :param include_members: Include members or not.

    URL Format: http://api.cr-api.com/clan/28VVQPV9,Y8GYCGV/?members=0
    """
    url = '{api_url}{tag_list}/{members}'.format(
        api_url=config.api.clan.clan_fmt.format(''),
        tag_list=','.join(clan_tags),
        members='' if include_members else '?members=0'
    )
    print(url)
    async with aiohttp.ClientSession() as session:
        data = await fetch(session, url)
        return data

async def fetch_top_clans():
    """Fetch top clans."""
    async with aiohttp.ClientSession() as session:
        # TODO: Move top clans API URL to config
        url = config.api.top_clans.url
        data = await fetch(session, url)
        return data


async def fetch_player(tag):
    """Fetch player from profile API."""
    ptag = SCTag(tag).tag
    url = '{}{}'.format(config.api.profile.url, ptag)

    try:
        async with aiohttp.ClientSession() as session:
            data = await fetch(session, url)
            return data
    # connection refused
    except aiohttp.ClientConnectorError:
        return None
    # timeout
    except asyncio.TimeoutError:
        return None

async def fetch_players(tags):
    """Fetch multiple players= from profile API."""
    ptags = [SCTag(tag).tag for tag in tags]
    url = '{}{}'.format(config.api.profile.url, ','.join(ptags))

    print(url)

    try:
        async with aiohttp.ClientSession() as session:
            data = await fetch(session, url)
            return data
    # connection refused
    except aiohttp.ClientConnectorError:
        return None
    # timeout
    except asyncio.TimeoutError:
        return None

