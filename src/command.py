from enum import Enum
from state import GameState
from airport import AirportManager

class Command(Enum):
    BUY_FLEET = "buy fleet"
    BUY_AIRPORT = "buy airport"
    MAINTAIN_FLEET = "maintain fleet"
    SELL_AIRPORT = "sell airport"
    INFO = "info"
    NEXT = "next"
    HELP = "help"
    QUIT = "quit"


    def run(self, game_state): #Passataan game_state eteenpäin niille komennoille, jotka sitä tarvii
        match self:
            case Command.BUY_FLEET:
                return self.buy_fleet()
            case Command.BUY_AIRPORT:
                return self.buy_airport(game_state)
            case Command.MAINTAIN_FLEET:
                return self.maintain_fleet()
            case Command.SELL_AIRPORT:
                return self.sell_airport()
            case Command.INFO:
                return self.info(game_state)
            case Command.NEXT:
                return self.next()
            case Command.HELP:
                return self.help()
            case Command.QUIT:
                return self.quit()

    def buy_fleet(self):
        return "Executing: Buy Fleet"

    def buy_airport(self, game_state):
        manager = AirportManager()
        manager.buy(input("Enter airport ICAO code: "), game_state.id)

    def maintain_fleet(self):
        return "Executing: Maintain Fleet"

    def sell_airport(self):
        return "Executing: Sell Airport"

    def info(self, game_state: GameState):
        print("Info:")
        print(f"Name: {game_state.name}")
        print(f"Money: {game_state.balance}")
        print(f"Quota: {game_state.quota}")
        print(f"\nYou currently own the following airports:")
        game_state.owned_airports = AirportManager().get_owned(game_state.id)
        for i in range(len(game_state.owned_airports)):
                print(f"{game_state.owned_airports[i].country}: {game_state.owned_airports[i].name} [{game_state.owned_airports[i].ident}]")

    def next(self):
        return "Executing: Next"

    def help(self):
        print(f"Possible commands: \n")
        commands = [i.value for i in Command]
        for i in range(len(commands)):
            print(commands[i])
        

    def quit(self):
        print("Bye!")
        quit()