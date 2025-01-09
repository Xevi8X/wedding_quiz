class Questions:
    def __init__(self):
        self.all = 0
        self.current = 0
        self.value = 0
        self.content = ''

    def __json__(self):
        return {
            'all': self.all,
            'current': self.current,
            'value': self.value,
            'content': self.content
        }
    
class Answers:
    def __init__(self):
        self.correct = 0
        self.content =['', '', '', '']

    def __json__(self):
        return {
            'correct': self.correct,
            'content': self.content
        }
    
class Tables:
    def __init__(self):
        self.all = []
        self.answered = []

    def __json__(self):
        return {
            'all': self.all,
            'answered': self.answered
        }

class Timer:
    def __init__(self):
        self.answer_time = 10
        self.left = 0

    def __json__(self):
        return {
            'answer_time': self.answer_time,
            'left': self.left
        }