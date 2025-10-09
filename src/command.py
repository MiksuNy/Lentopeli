from enum import Enum
from state import *

class Command(Enum):
    BUY_AIRPLANE = "buy airplane"
    BUY_AIRPORT = "buy airport"
    MAINTAIN_AIRPLANE = "maintain airplane"
    SELL_AIRPORT = "sell airport"
    INFO = "info"
    NEXT = "next"
    HELP = "help"
    QUIT = "quit"


    def run(self, game_state): #Passataan game_state eteenpäin niille komennoille, jotka sitä tarvii
        match self:
            case Command.BUY_AIRPLANE:
                return self.buy_airplane(game_state)
            case Command.BUY_AIRPORT:
                return self.buy_airport(game_state)
            case Command.MAINTAIN_AIRPLANE:
                return self.maintain_airplane()
            case Command.SELL_AIRPORT:
                return self.sell_airport()
            case Command.INFO:
                return self.info(game_state)
            case Command.NEXT:
                return self.next(game_state)
            case Command.HELP:
                return self.help()
            case Command.QUIT:
                return self.quit()

    def buy_airplane(self, game_state):
        game_state.airplane_manager.buy(input("Enter airplane type (passenger, cargo): "), game_state)

    def buy_airport(self, game_state):
        game_state.airport_manager.buy(input("Enter airport ICAO code: "), game_state)

    def maintain_airplane(self):
        return "Executing: Maintain Airplane"

    def sell_airport(self):
        return "Executing: Sell Airport"

    def info(self, game_state: GameState):
        print("Info:")
        print(f"Name: {game_state.name}")
        print(f"Money: {game_state.wallet.get_balance()}")
        print(f"Quota: {game_state.quota}")
        print(f"\nYou currently own the following airports:")
        owned_airports = game_state.airport_manager.get_owned(game_state)
        for i in range(len(owned_airports)):
                print(f"{owned_airports[i].country}: {owned_airports[i].name} [{owned_airports[i].ident}] @ €{owned_airports[i].cost}")
        print(f"\nYou currently own the following airplanes:")
        owned_airplanes = game_state.airplane_manager.get_owned()
        for i in range(len(owned_airplanes)):
                print(f"{owned_airplanes[i].airplane_type}")

    def next(self, game_state):
        game_state.airplane_manager.move_all()
        game_state.event_manager.roll()

    def help(self):
        print(f"Possible commands: \n")
        commands = [i.value for i in Command]
        for i in range(len(commands)):
            print(commands[i])
        

    def quit(self):
        print("Bye!")
        quit()
