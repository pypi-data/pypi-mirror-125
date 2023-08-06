from io import BytesIO
from pathlib import Path

from PIL import Image

from .unit_info import UnitInfo


class Unit:
    def __init__(self, series, root, unit_type, unit_file_with_extension, oss_bucket=None):
        self._series = series
        self._root = root
        self._unit_file_with_extension = unit_file_with_extension
        self._unit_info = UnitInfo(type=unit_type, file_name=Path(self._unit_file_with_extension).stem)
        self._oss_bucket = oss_bucket

    @property
    def series(self):
        return self._series

    @property
    def root(self):
        return self._root

    @property
    def unit_file_with_extension(self):
        return self._unit_file_with_extension

    @property
    def unit_info(self):
        return self._unit_info

    @property
    def oss_bucket(self):
        return self._oss_bucket

    @property
    def unit_type(self):
        return self._unit_info.type

    @property
    def unit_name(self):
        return self._unit_info.name

    @property
    def unit_name_with_type(self):
        return f"{self.unit_type}_{self.unit_name}"

    @property
    def unit_color(self):
        return self._unit_info.color

    @property
    def unit_score(self):
        return self._unit_info.score

    @property
    def unit_file_name(self):
        return self._unit_info.file_name

    def image(self):
        if self.oss_bucket:
            stream = BytesIO(self.oss_bucket.get(self.unit_file_with_extension))
            return Image.open(stream).convert("RGBA")
        return Image.open(self.unit_file_with_extension).convert("RGBA")
