from cr_api.models import CRPlayerModel
import json
import os

# api.init()

def test_profile():
    with open(os.path.abspath('./data/profile/C0G20PR2.json')) as f:
        data = json.load(f)

    player = CRPlayerModel(json=data)
    assert player.name == 'SML'
    assert player.tag == 'C0G20PR2'
    assert player.clan_name == 'Reddit Delta'
    assert player.clan_role == 'Leader'