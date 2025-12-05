from enum import Enum
from db import *
from state import *

class AirplaneType(Enum):
    PASSENGER = "passenger"
    CARGO = "cargo"

class Airplane:
    def __init__(self, airplane_type, airport_ident = None, owned_by_player = False):
        self.airport_ident = airport_ident
        self.airplane_type = airplane_type
        self.owned_by_player = owned_by_player
