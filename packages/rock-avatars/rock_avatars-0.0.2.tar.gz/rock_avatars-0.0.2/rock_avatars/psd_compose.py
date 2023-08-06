import os
from io import BytesIO
from pathlib import Path

from psd_tools import PSDImage


class PSDCompose:
    def __init__(self, psd_file, output_base, oss_bucket=None) -> None:
        self._series = Path(psd_file).stem
        self._oss_bucket = oss_bucket
        if self.oss_bucket:
            stream = BytesIO(self.oss_bucket.get(psd_file))
            self._psd = PSDImage.open(stream)[0]
        else:
            # 跳过第一层ArtBoard
            self._psd = PSDImage.open(psd_file)[0]
        self._view_box = self._psd.bbox
        self._output_base = output_base
        self._component_depth = 2

    @property
    def series(self):
        return self._series

    @property
    def psd(self):
        return self._psd

    @property
    def view_box(self):
        return self._view_box

    @property
    def output_base(self):
        return self._output_base

    @property
    def component_depth(self):
        return self._component_depth

    @property
    def oss_bucket(self):
        return self._oss_bucket

    def unit_list(self):
        unit_list = []
        for child in self.psd:
            if child.kind == 'group':
                unit_list.append(child.name)
        return unit_list

    def compose(self):
        self.recur(
            0,
            "",
            self.psd,
        )
        if self.oss_bucket:
            path_base = ""
        else:
            path_base = self.output_base
        return [
            self.series,
            PSDCompose.path_join(path_base, self.psd),
            self.unit_list(),
        ]

    @staticmethod
    def path_join(path, layer):
        return os.path.join(path, layer.name)

    @staticmethod
    def png_file(path, layer):
        return '%s.png' % PSDCompose.path_join(path, layer)

    def save_to_oss(self, layer, relative_path):
        image_path = PSDCompose.png_file(relative_path, layer)
        with BytesIO() as output:
            layer.composite(viewport=self.view_box).save(output, format="PNG")
            self.oss_bucket.put(image_path, output.getvalue())

    def save_to_local(self, layer, relative_path):
        absolute_path = os.path.join(self.output_base, relative_path)
        if not os.path.isdir(absolute_path):
            os.makedirs(absolute_path)
        layer.composite(viewport=self.view_box).save(PSDCompose.png_file(absolute_path, layer), format="PNG")

    def save(self, layer, relative_path):
        if self.oss_bucket:
            return self.save_to_oss(layer, relative_path)
        else:
            return self.save_to_local(layer, relative_path)

    def recur(self, depth, relative_path, layer):
        if not layer.is_visible():
            return
        if layer.is_group() and depth == self.component_depth:
            self.save(layer, relative_path)
        elif layer.is_group():
            for child in layer:
                self.recur(
                    depth + 1,
                    PSDCompose.path_join(relative_path, layer),
                    child,
                )
        else:
            self.save(layer, relative_path)
