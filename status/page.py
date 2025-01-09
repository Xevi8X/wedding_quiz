from enum import Enum

class Page(Enum):
    WELCOME = 1
    QUIZ = 2
    LEADERBOARD = 3

    def to_page(self):
        match self:
            case Page.WELCOME:
                return 'welcome_page'
            case Page.QUIZ:
                return 'question_page'
            case Page.LEADERBOARD:
                return 'leaderboard_page'
            case _:
                return ''