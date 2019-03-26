
class TemplateNotFound(IOError, LookupError):
    def __init__(self, name):
        IOError.__init__(self)
        self.name = name
