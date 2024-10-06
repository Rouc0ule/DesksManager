class UniqueTagGenerator:
    def __init__(self):
        self.counter = 0

    def next_tag(self):
        self.counter += 1
        print(self.counter)
        return f"node-{self.counter}"