from dataclasses import dataclass


@dataclass
class Foo:
    bar: str = None

    def test(self):
        self.bar = 123

    def __init__(self):
        self.test()


foo = Foo()
# foo.test()

print(foo.bar)
