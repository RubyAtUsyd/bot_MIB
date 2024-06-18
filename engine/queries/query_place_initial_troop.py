from typing import Iterable, Literal
from pydantic import BaseModel

from engine.models.player.player_public_model import PlayerPublicModel
from engine.models.territory_model import TerritoryModel


class QueryPlaceInitialTroop(BaseModel):
    query: Literal["place_initial_troop"] = "place_initial_troop"
    territories: Iterable[TerritoryModel]
    players: Iterable[PlayerPublicModel]