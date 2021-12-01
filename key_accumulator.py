class KeyAccumulator:

    def __init__(self) -> None:
        self.answer_string = ""

    def add_key(self, key) -> None:
        if key in [key.K_0, key.K_1, key.K_2, key.K_3, key.K_4, key.K_5, key.K_6, key.K_7, key.K_8, key.K_9]:
            # accumulate keys
            self.answer_string += str(key)[-1]

        if key == key.BACKSPACE:
            self.answer_string = self.answer_string[:-1] if len(self.answer_string) > 0 else ""