"""
cr-api async client for Clash Royale.
"""
import asyncio
import logging

import aiohttp

from .exceptions import APIError, APIClientResponseError, APITimeoutError
from .models import Clan, Tag, Player, Constants
from .url import APIURL

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class AsyncClient:
    """
    API AsyncClient.
    """

    def __init__(self):
        pass

    async def fetch(self, url):
        """Fetch URL.

        :param url: URL
        :return: Response in JSON
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
                    if resp.status != 200:
                        logger.error(
                            "API Error | HTTP status {status} | {errmsg} | url: {url}".format(
                                status=resp.status,
                                errmsg=data.get('error'),
                                url=url
                            )
                        )
                        raise APIError

        except asyncio.TimeoutError:
            raise APITimeoutError
        except aiohttp.client_exceptions.ClientResponseError:
            raise APIClientResponseError

        return data

    async def get_clan(self, clan_tag):
        """Fetch a single clan."""
        url = APIURL.clan.format(clan_tag)
        data = await self.fetch(url)
        if isinstance(data, list):
            data = data[0]
        return Clan(data=data, url=url)

    async def get_clans(self, clan_tags):
        """Fetch multiple clans.

        :param clan_tags: List of clan tags
        """
        url = APIURL.clan.format(','.join(clan_tags))
        data = await self.fetch(url)
        return [Clan(data=d, url=url) for d in data]

    async def get_top_clans(self):
        """Fetch top clans."""
        data = await self.fetch(APIURL.top_clans)
        return data

    async def get_profile(self, tag: str) -> Player:
        """Get player profile by tag.
        :param tag: 
        :return: 
        """
        ptag = Tag(tag).tag
        url = APIURL.profile.format(ptag)
        data = await self.fetch(url)
        return Player(data=data, url=url)

    async def get_profiles(self, tags):
        """Fetch multiple players from profile API."""
        ptags = [Tag(tag).tag for tag in tags]
        url = APIURL.profile.format(','.join(ptags))
        data = await self.fetch(url)
        return [Player(data=d, url=url) for d in data]

    async def get_constants(self, key=None):
        """Fetch contants.

        :param key: Optional field.
        """
        url = APIURL.constants
        data = await self.fetch(url)
        return Constants(data=data, url=url)