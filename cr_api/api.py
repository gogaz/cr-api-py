"""
Unified module to call api for data.
In the beginning managers were used but this became problematic
when multiple classes need to access these endpoints.
"""
import asyncio

import aiohttp
import async_timeout

from .models import ProfileModel, SCTag


class APIError(Exception):
    pass


class APITimeoutError(APIError):
    pass


class APIClientResponseError(APIError):
    pass


class Client:
    """
    API Client.
    """

    def __init__(self, session=None, timeout=30):
        if session is None:
            session = aiohttp.ClientSession()
        self.session = session

        self.timeout = timeout

    async def fetch(self, url):
        """Fetch URL.

        :param session: aiohttp.ClientSession
        :param url: URL
        :return: Response in JSON
        """
        try:
            with async_timeout.timeout(self.timeout):
                async with self.session.get(url) as resp:
                    if resp.status != 200:
                        raise APIError
                    return resp.json()
        except asyncio.TimeoutError:
            raise APITimeoutError
        except aiohttp.client_exceptions.ClientResponseError:
            raise APIClientResponseError

    async def get_clan(self, clan_tag, include_members=True):
        """Fetch a single clan."""
        url = '{api_url}/{members}'.format(
            api_url='http://api.cr-api.com/clan/{}'.format(clan_tag),
            members='' if include_members else '?members=0'
        )
        print(url)
        data = await self.fetch(url)
        if isinstance(data, list):
            data = data[0]
        return data

    async def get_clans(self, clan_tags, include_members=True):
        """Fetch multiple clans.

        :param clan_tags: List of clan tags
        :param include_members: Include members or not.

        URL Format: http://api.cr-api.com/clan/28VVQPV9,Y8GYCGV/?members=0
        """
        url = '{api_url}/{tag_list}/{members}'.format(
            api_url='http://api.cr-api.com/clan',
            tag_list=','.join(clan_tags),
            members='' if include_members else '?members=0'
        )
        print(url)
        data = await self.fetch(url)
        return data

    async def get_top_clans(self):
        """Fetch top clans."""
        data = await self.fetch('http://api.cr-api.com/top/clans')
        return data

    async def get_profile(self, tag):
        """Fetch player from profile API."""
        ptag = SCTag(tag).tag
        url = '{}{}'.format(config.api.profile.url, ptag)
        data = await self.fetch(url)
        return ProfileModel(json=data)

    async def get_profiles(self, tags):
        """Fetch multiple players from profile API."""
        ptags = [SCTag(tag).tag for tag in tags]
        url = '{}{}'.format(config.api.profile.url, ','.join(ptags))
        data = await self.fetch(url)
        return [ProfileModel(json=d) for d in data]
