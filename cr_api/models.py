# -*- coding: utf-8 -*-

"""
Clash Royale models.
"""

from json import dumps, loads
from logging import getLogger

__timeformat__ = '%Y-%m-%dT%H:%M:%SZ'
__logs__ = getLogger(__package__)


class Tag:
    """SuperCell tags."""

    TAG_CHARACTERS = "0289PYLQGRJCUV"

    def __init__(self, tag: str):
        """Init.

        Remove # if found.
        Convert to uppercase.
        Convert Os to 0s if found.
        """
        if tag.startswith('#'):
            tag = tag[1:]
        tag = tag.replace('O', '0')
        tag = tag.upper()
        self._tag = tag

    @property
    def tag(self):
        """Return tag as str."""
        return self._tag

    @property
    def valid(self):
        """Return true if tag is valid."""
        for c in self.tag:
            if c not in self.TAG_CHARACTERS:
                return False
        return True

    @property
    def invalid_chars(self):
        """Return list of invalid characters."""
        invalids = []
        for c in self.tag:
            if c not in self.TAG_CHARACTERS:
                invalids.append(c)
        return invalids

    @property
    def invalid_error_msg(self):
        """Error message to show if invalid."""
        return (
            'The tag you have entered is not valid. \n'
            'List of invalid characters in your tag: {}\n'
            'List of valid characters for tags: {}'.format(
                ', '.join(self.invalid_chars),
                ', '.join(self.TAG_CHARACTERS)
            ))


class BaseModel(object):
    """Clash Royale base model."""

    def __init__(self, data=None, url=None):
        if url is not None:
            self._uniq = url
        self._data = data
        self._update_attributes(data)

    def _update_attributes(self, data):
        pass

    def __getattr__(self, attribute):
        """Proxy acess to stored JSON."""
        if attribute not in self._data:
            raise AttributeError(attribute)
        value = self._data.get(attribute)
        setattr(self, attribute, value)
        return value

    def as_dict(self):
        """Return the attributes for this object as a dictionary.

        This is equivalent to calling:

            json.loads(obj.as_json())

        :returns: this object’s attributes seriaized as a dictionary
        :rtype: dict
        """
        return self._data

    def as_json(self):
        """Return the json data for this object.

        This is equivalent to calling:

            json.dumps(obj.as_dict())

        :returns: this object’s attributes as a JSON string
        :rtype: str
        """
        return dumps(self._data)

    @classmethod
    def _get_attribute(cls, data, attribute, fallback=None):
        """Return the attribute from the JSON data.

        :param dict data: dictionary used to put together the model
        :param str attribute: key of the attribute
        :param any fallback: return value if original return value is falsy
        :returns: value paried with key in dict, fallback
        """
        if data is None or not isinstance(data, dict):
            return None
        result = data.get(attribute)
        if result is None:
            return fallback
        return result

    @classmethod
    def __class_attribute(cls, data, attribute, cl, *args, **kwargs):
        """Return the attribute from the JSON data and instantiate the class.

        "param dict data: dictionary used to put together the model or None
        "param str attribute: key of the attribute
        :param class cl: class that will be instantiated
        :returns: instantiated class or None
        :rtype: object or None
        """
        value = cls._get_attribute(data, attribute)
        if value:
            return cl(
                value,
                *args,
                **kwargs
            )
        return value

    def __repr__(self):
        repr_string = self._repr()
        return repr_string

    @classmethod
    def from_dict(cls, json_dict):
        """Return an instanc of this class formed from ``json_dict``."""
        return cls(json_dict)

    @classmethod
    def from_json(cls, json):
        """Return an instane of this class formed from ``json``."""
        return cls(loads(json))

    def __eq__(self, other):
        return self._uniq == other._uniq

    def __ne__(self, other):
        return self._uniq != other._uniq

    def _repr(self):
        return "{}({})".format(self.__class__, self.__dict__)


class ProfileClan(BaseModel):
    """Clan model inside a profile."""

    def _update_attributes(self, data):
        self.tag = self._get_attribute(data, 'tag')
        self.name = self._get_attribute(data, 'name', 'No Clan')
        self.role = self._get_attribute(data, 'role', 'N/A')
        self.badge = Badge(data=self._get_attribute(data, 'badge'))


class Card(BaseModel):
    """Card."""

    def _update_attributes(self, data):
        self.name = self._get_attribute(data, 'name')
        self.rarity = self._get_attribute(data, 'rarity')
        self.level = self._get_attribute(data, 'level')
        self.count = self._get_attribute(data, 'count')
        self.required_for_upgrade = self._get_attribute(data, 'requiredForUpgrade')
        self.card_id = self._get_attribute(data, 'card_id')
        self.key = self._get_attribute(data, 'key')
        self.card_key = self._get_attribute(data, 'card_key')
        self.elixir = self._get_attribute(data, 'elixir')
        self.type = self._get_attribute(data, 'type')
        self.arena = self._get_attribute(data, 'arena')
        self.description = self._get_attribute(data, 'description')
        self.decklink = self._get_attribute(data, 'decklink')
        self.left_to_upgrade = self._get_attribute(data, 'leftToUpgrade')


class Deck(BaseModel):
    """Deck with cards."""

    def _update_attributes(self, data):
        self.cards = [Card(data=c) for c in data]

class PlayerExperience(BaseModel):
    """Player experience."""

    def _update_attributes(self, data):
        self.level = self._get_attribute(data, 'level')
        self.xp = self._get_attribute(data, 'xp')
        self.xp_required_for_level_up = self._get_attribute(data, 'xpRequiredForLevelUp')
        self.xp_to_level_up = self._get_attribute(data, 'xpToLevelUp')
        
class PlayerStats(BaseModel):
    """Player stats."""
    def _update_attributes(self, data):
        self.legendary_trophies = self._get_attribute(data, 'legendaryTrophies')
        self.tournament_cards_won = self._get_attribute(data, 'tournamentCardsWon')
        self.max_trophies = self._get_attribute(data, 'maxTrophies')
        self.three_crown_wins = self._get_attribute(data, 'threeCrownWins')
        self.cards_found = self._get_attribute(data, 'cardsFound')
        self.favorite_card = self._get_attribute(data, 'favoriteCard')
        self.total_donatons = self._get_attribute(data, 'totalDonations')
        self.challenge_max_wins = self._get_attribute(data, 'challengeMaxWins')
        self.challenge_cards_won = self._get_attribute(data, 'challengeCardsWon')
        self.level = self._get_attribute(data, 'level')

class PlayerGames(BaseModel):
    """Player game stats."""
    def _update_attributes(self, data):
        self.total = self._get_attribute(data, 'total')
        self.tournament_games = self._get_attribute(data, 'tournamentGames')
        self.wins = self._get_attribute(data, 'wins')
        self.losses = self._get_attribute(data, 'losses')
        self.draws = self._get_attribute(data, 'draws')
        self.current_win_streak = self._get_attribute(data, 'currentWinStreak')
        
class PlayerChestCycle(BaseModel):
    """Player chest cycle"""

    def _update_attributes(self, data):
        self.position = self._get_attribute(data, 'position')
        self.super_magical_pos = self._get_attribute(data, 'superMagicalPos')
        self.legendary_pos = self._get_attribute(data, 'legendaryPos')
        self.epic_pos = self._get_attribute(data, 'epicPos')
        
class PlayerShopOffers(BaseModel):
    """Shop offers."""

    def _update_attributes(self, data):
        self.legendary = self._get_attribute(data, 'legendary')
        self.epic = self._get_attribute(data, 'epic')
        self.arena = self._get_attribute(data, 'arena')
        
class Profile(BaseModel):
    """A player profile in Clash Royale."""

    def _update_attributes(self, data):
        #: Unique player tag.
        self.tag = self._get_attribute(data, 'tag')

        #: In-game name, aka username
        self.name = self._get_attribute(data, 'name')

        #: Current trophies
        self.trophies = self._get_attribute(data, 'trophies')

        #: name change option
        self.name_changed = self._get_attribute(data, 'nameChanged')

        #: global rank
        self.global_rank = self._get_attribute(data, 'globalRank')

        #: ----------
        #: Clan
        # self.clan = self._get_attribute(player, 'clan')
        self.clan = Clan(data=self._get_attribute(data, 'clan'))

        #: Not in clan
        self.not_in_clan = self.clan is None

        #: Clan name
        self.clan_name = 'No Clan'

        #: Clan tag
        self.clan_tag = None

        #: Clan role
        self.clan_role = 'N/A'

        self.clan_name = self.clan.name
        self.clan_tag = self.clan.tag
        self.clan_role = self.clan.role

        self.badge = Badge(data=self._get_attribute(data, 'badge'))

        #: Arena
        self.arena = Arena(data=self._get_attribute(data, 'arena'))

        #: Experience
        self.experience = PlayerExperience(data=self._get_attribute(data, 'experience'))

        #: Stats
        self.stats = PlayerStats(data=self._get_attribute(data, 'stats'))

        #: Games
        self.games = PlayerGames(data=self._get_attribute(data, 'games'))

        #: Chests
        self.chest_cycle = PlayerChestCycle(data=self._get_attribute(data, 'chestCycle'))

        #: Shop offers
        self.shop_offers = PlayerShopOffers(data=self._get_attribute(data, 'shopOffers'))

        #: Deck
        self.deck = Deck(data=self._get_attribute(data, 'currentDeck'))


class Badge(BaseModel):
    def _update_attributes(self, data):
        # - url
        self.url = self._get_attribute(data, 'url', 'http://smlbiobot.github.io/img/emblems/NoClan.png')

        # - filename
        self.filename = self._get_attribute(data, 'filename')

        # - key
        self.key = self._get_attribute(data, 'key')


class Region(BaseModel):
    def _update_attributes(self, data):
        # - region is a country
        self.is_country = self._get_attribute(data, 'isCountry')

        # - name
        self.name = self._get_attribute(data, 'name')


class ClanChest(BaseModel):
    def _update_attributes(self, data):
        # crowns
        self.crowns = self._get_attribute(data, 'clanChestCrowns')

        # crown percent
        self.crowns_percent = self._get_attribute(data, 'clanChestCrownsPercent')

        # crowns required
        self.crowns_required = self._get_attribute(data, 'clanChestCrownsRequired')


class Arena(BaseModel):
    def _update_attributes(self, data):
        self.image_url = self._get_attribute(data, 'imageURL')
        self.arena = self._get_attribute(data, 'arena')
        self.arena_id = self._get_attribute(data, 'arenaID')
        self.name = self._get_attribute(data, 'name')
        self.trophy_limit = self._get_attribute(data, 'trophyLimit')


class ClanMember(BaseModel):
    """Member model in clan."""

    def _update_attributes(self, data):
        # - name
        self.name = self._get_attribute(data, 'name')

        # - arena
        self.arena = Arena(data=self._get_attribute(data, 'arena'))

        # - experience level
        self.experience_level = self._get_attribute(data, 'expLevel')

        # - trophies
        self.trophies = self._get_attribute(data, 'trophies')

        # - score: alias to trophies
        self.score = self._get_attribute(data, 'score')

        # - donations for the week
        self.donations = self._get_attribute(data, 'donations')

        # - current rank
        self.current_rank = self._get_attribute(data, 'currentRank')

        # - previous rank
        self.previous_rank = self._get_attribute(data, 'previousRank')

        # - clan chest crowns
        self.clan_chestcrowns = self._get_attribute(data, 'clanChestCrowns')

        # - player tag
        self.tag = self._get_attribute(data, 'tag')

        # - role: enum
        self.role = self._get_attribute(data, 'role')

        # - role name
        self.role_name = self._get_attribute(data, 'role_name')

        # - clan name
        self.clan_name = self._get_attribute(data, 'clan_name')

        # - clan name
        self.clan_tag = self._get_attribute(data, 'clan_tag')

    @property
    def rank_delta(self):
        """Difference in rank.

        Return None if previous rank is 0
        """
        if self.previous_rank == 0:
            return None
        else:
            return self.current_rank - self.previous_rank

    @property
    def league(self):
        """League ID from Arena ID."""
        return max(0, self.arena.arean_id - 11)

    @property
    def league_icon_url(self):
        """League Icon URL."""
        return (
            'http://smlbiobot.github.io/img/leagues/'
            'league{}.png'
        ).format(self.league)


class Clan(BaseModel):
    """Clash Royale Clan data."""

    def _update_attributes(self, data):
        # - Name of clan
        self.name = self._get_attribute(data, 'name')

        # - badge
        self.badge = Badge(data=self._get_attribute(data, 'badge'))

        # - type of the clan: enum
        self.type = self._get_attribute(data, 'type')

        # - type name
        self.type_name = self._get_attribute(data, 'typeName')

        # - number of memebers in clan
        self.member_count = self._get_attribute(data, 'memberCount')

        # - required trophies to join
        self.required_score = self._get_attribute(data, 'requiredScore')

        # - total donations for the week
        self.donations = self._get_attribute(data, 'donations')

        # - current rank
        # TODO: not sure what this is
        self.current_rank = self._get_attribute(data, 'currentRank')

        # - clan description
        self.description = self._get_attribute(data, 'description')

        # - clan tag
        self.tag = self._get_attribute(data, 'tag')

        # - region
        self.region = Region(data=self._get_attribute(data, 'region'))

        # - members
        members = self._get_attribute(data, 'members')
        clan_dict = {
            "clan_name": self.name,
            "clan_tag": self.tag
        }
        self.members = []
        if members is not None:
            for m in members:
                m.update(clan_dict)
                self.members.append(ClanMember(data=m))

    @property
    def member_tags(self):
        """List of member tags."""
        return [m.tag for m in self.members]
