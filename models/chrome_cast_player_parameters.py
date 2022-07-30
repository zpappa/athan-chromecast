from dataclasses import dataclass, field
from typing import List

from models.base_player_parameters import BasePlayerParameters


@dataclass
class ChromeCastPlayerParameters(BasePlayerParameters):
    google_home_group_name: str = None
    chrome_cast_names: List[str] = field(default_factory=list)
