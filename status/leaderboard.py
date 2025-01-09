from typing import List


class Result:
    def __init__(self):
        self.places : List[Place] = [] 
        self.first_visible = 0

    def __json__(self):
        places = [place.__json__() for place in self.places]
        return {
            'first_visible': self.first_visible,
            'places': places
        }

class Place:
    def __init__(self, total, tables):
        self.total = total
        self.tables = tables

    def __json__(self):
        return {
            'total': self.total,
            'tables': self.tables,
        }