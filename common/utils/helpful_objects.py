class AmazonItem:
    def __init__(self, title, description, catagories, details):
        self.title = title
        self.description = description
        self.catagories = catagories
        self.details = details
        self.full_text = None


class AlibabaItem:
    def __init__(self, title):
        self.title = title
