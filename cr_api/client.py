"""
Unified module to call api for data.
In the beginning managers were used but this became problematic
when multiple classes need to access these endpoints.
"""
import asyncio

import aiohttp
import async_timeout

from .models import Profile, Tag, Clan


class APIError(Exception):
    pass


class APITimeoutError(APIError):
    pass


class APIClientResponseError(APIError):
    pass

class APIURL:
    """
    API URL
    """
    clan = 'http://api.cr-api.com/clan/{}'
    top_clans = 'http://api.cr-api.com/top/clans'
    profile = 'http://api.cr-api.com/profile/{}'

class Client:
    """
    API Client.
    """

    def __init__(self):
        pass

    async def fetch(self, url):
        """Fetch URL.

        :param url: URL
        :return: Response in JSON
        """
        data = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        raise APIError
                    data = await resp.json()
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

    async def get_clans(self, clan_tags, include_members=True):
        """Fetch multiple clans.

        :param clan_tags: List of clan tags
        :param include_members: Include members or not.

        URL Format: http://api.cr-api.com/clan/28VVQPV9,Y8GYCGV/?members=0
        """
        url = '{api_url}/{tag_list}/{members}'.format(
            api_url=APIURL.clan,
            tag_list=','.join(clan_tags),
            members='' if include_members else '?members=0'
        )
        data = await self.fetch(url)
        return data

    async def get_top_clans(self):
        """Fetch top clans."""
        data = await self.fetch(APIURL.top_clans)
        return data

    async def get_profile(self, tag: str) -> Profile:
        """Get player profile by tag.
        :param tag: 
        :return: 
        """
        ptag = Tag(tag).tag
        url = APIURL.profile.format(ptag)
        data = await self.fetch(url)
        return Profile(data=data, url=url)

    async def get_profiles(self, tags):
        """Fetch multiple players from profile API."""
        ptags = [Tag(tag).tag for tag in tags]
        url = APIURL.profile.format(','.join(ptags))
        data = await self.fetch(url)
        return [Profile(data=d, url=url) for d in data]
