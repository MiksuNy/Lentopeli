from enum import Enum

class Event(Enum):
    QUIT_GAME = 0
    NEXT_TURN = 1

class EventManager:
    def __init__(self):
        self.event_queue = []

    def append_queue(self, event):
        self.event_queue.append(event)

    def pop_queue(self):
        return self.event_queue.pop(0)

    def queue_event_from_string(self, string):
        match string:
            case "quit":
                self.append_queue(Event.QUIT_GAME)
            case "next":
                self.append_queue(Event.NEXT_TURN)
