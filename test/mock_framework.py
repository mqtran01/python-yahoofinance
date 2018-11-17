class MockResponse:
    def __init__(self, text):
        self.text = text

    def json(self):
        return self.json_data

    @property
    def cookies(self):
        return {'B': '1234'}