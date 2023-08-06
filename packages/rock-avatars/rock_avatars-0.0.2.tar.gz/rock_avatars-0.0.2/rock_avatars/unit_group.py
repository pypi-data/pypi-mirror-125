import os

import oss2

from .unit import Unit


class UnitGroup:
    def __init__(self, series, root, unit_type, oss_bucket=None):
        self._series = series
        self._root = root
        self._unit_type = unit_type
        self._oss_bucket = oss_bucket

        self._unit_list = []
        self.init_unit_list()

    def init_unit_list(self):
        if self.oss_bucket:
            self.init_unit_list_by_oss()
        else:
            self.init_unit_list_by_local()

    def init_unit_list_by_oss(self):
        for obj in oss2.ObjectIteratorV2(
                self.oss_bucket.bucket,
                prefix=f"{self.unit_type_path}/",
                delimiter='/',
        ):
            self._unit_list.append(
                Unit(self.series, self.root, self.unit_type, obj.key, oss_bucket=self.oss_bucket))

    def init_unit_list_by_local(self):
        for _, _, files in os.walk(self.unit_type_path):
            for unit_file_with_extension in files:
                self._unit_list.append(
                    Unit(self.series, self.root, self.unit_type, unit_file_with_extension, oss_bucket=self.oss_bucket))

    @property
    def series(self):
        return self._series

    @property
    def root(self):
        return self._root

    @property
    def unit_type(self):
        return self._unit_type

    @property
    def oss_bucket(self):
        return self._oss_bucket

    @property
    def unit_type_path(self):
        return os.path.join(self.root, self.unit_type)

    @property
    def unit_list(self):
        return self._unit_list
