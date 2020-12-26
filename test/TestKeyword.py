from robot.api.deco import keyword


class TestKeyword:
    data = {}

    def __init__(self):
        self.data = {}

    @keyword
    def enrollment_veeahub(self):
        return 1
