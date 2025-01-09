import json
from threading import RLock

from .page import Page
from .quiz import Questions, Answers, Tables, Timer
from .leaderboard import Result

class Status:
    def __init__(self):
        self.lock = RLock()

        self.version = 1
        self.page = Page.WELCOME

        self.questions = Questions()
        self.answers = Answers()
        self.tables = Tables()
        self.timer = Timer()

        self.results = Result()

    def as_json(self):
        with self.lock:
            data = {
                'version': self.version,
                'page': self.page.to_page(),
            }

            match self.page:
                case Page.WELCOME:
                    pass

                case Page.QUIZ:
                    question_data = {
                        'question': self.questions.__json__(),
                        'answers': self.answers.__json__(),
                        'tables': self.tables.__json__(),
                        'timer': self.timer.__json__()
                    }
                    data['question_data'] = question_data

                case Page.LEADERBOARD:
                    data['leaderboard_data'] = self.results.__json__()

            return json.dumps(data)
