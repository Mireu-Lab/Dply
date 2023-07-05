class Search:
    def __init__(self, projectName: str = None) -> None:
        self.projectName = projectName

    def __call__(self):
        print(self.projectName)


test = Search("mireu")
print(test())
