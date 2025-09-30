from enum import Enum
from command import Command

class EventManager:
    def __init__(self):
        self.event_queue = []

    def append_queue(self, event):
        self.event_queue.append(event)

    def pop_queue(self):
        return self.event_queue.pop(0)