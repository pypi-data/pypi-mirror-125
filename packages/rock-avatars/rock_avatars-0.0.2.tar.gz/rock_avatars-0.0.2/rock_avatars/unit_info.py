class UnitInfo:
    def __init__(self, type=None, name=None, color=None, score=0, file_name=None):
        self._type = type
        self._name = name
        self._color = color
        self._score = score
        self._file_name = file_name
        if len(file_name) > 0:
            field_list = file_name.split(',')
            if len(field_list) > 0:
                self._name = field_list[0]
            if len(field_list) > 1:
                self._color = field_list[1]
            if len(field_list) > 2:
                self._score = int(field_list[2])

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def score(self):
        return self._score

    @property
    def file_name(self):
        return self.file_name
