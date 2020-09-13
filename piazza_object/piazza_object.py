class PiazzaObject:
    def __init__(self, id, subject, content, date, link):
        self.id = id
        self.subject = subject
        self.content = content
        self.date = date
        self.link = link
    def to_string(self):
        return f'Subject: {self.subject}\nContent: {self.content}\nDate: {self.date}\nLink: {self.link}'