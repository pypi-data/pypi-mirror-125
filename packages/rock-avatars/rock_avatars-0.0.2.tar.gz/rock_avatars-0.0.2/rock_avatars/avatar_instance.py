import json
import os
from io import BytesIO


class AvatarInstance:
    def __init__(self, series, unit_list, output_path="./output", oss_bucket=None):
        self._series = series
        self._unit_list = unit_list
        self._output_path = output_path

        self._oss_bucket = oss_bucket
        self._result_image = None
        self._result_info = None

    @property
    def series(self):
        return self._series

    @property
    def unit_list(self):
        return self._unit_list

    @property
    def output_path(self):
        return self._output_path

    @property
    def avatar_name(self):
        sum_score = sum([unit.unit_score for unit in self.unit_list])
        new_unit_list = [unit for unit in self.unit_list]
        new_unit_list.sort(key=lambda x: x.unit_type)
        new_unit_list = [unit for unit in new_unit_list if unit.unit_name != "blank"]
        return ",".join([str(sum_score)] + [unit.unit_name for unit in new_unit_list])

    @property
    def valid(self):
        color_list = [unit for unit in self.unit_list if unit.unit_color]
        return not color_list or len(set(color_list)) > 1

    @property
    def avatar_image_name(self):
        return self.avatar_name + ".png"

    @property
    def avatar_info_name(self):
        return self.avatar_name + ".json"

    @property
    def avatar_image_path(self):
        return os.path.join(self.output_path, self.avatar_image_name)

    @property
    def avatar_info_path(self):
        return os.path.join(self.output_path, self.avatar_info_name)

    @property
    def oss_bucket(self):
        return self._oss_bucket

    def blend_info(self):
        info = {
            unit.unit_type: unit.unit_name for unit in self.unit_list
        }
        info["image_name"] = self.avatar_name,
        info["image_url"] = self.avatar_image_name,
        self._result_info = info
        return info

    @staticmethod
    def blend_two(background, overlay):
        _, _, _, alpha = overlay.split()
        background.paste(overlay, (0, 0), mask=alpha)
        return background

    @property
    def result_info(self):
        return self._result_info

    @property
    def result_image(self):
        return self._result_image

    def blend_image(self):
        result = self.unit_list[0].image()
        for i in range(1, len(self.unit_list)):
            result = AvatarInstance.blend_two(result, self.unit_list[i].image())
        self._result_image = result
        return result

    def blend_and_save_info_local(self):
        if os.path.isfile(self.avatar_info_path):
            return
        self.blend_info()
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
        with open(self.avatar_info_path, "w") as f:
            json.dump(self.result_info, f)

    def blend_and_save_image_local(self):
        if os.path.isfile(self.avatar_image_path):
            return
        self.blend_image()
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
        self.result_image.save(self.avatar_image_path, "PNG")

    def blend_and_save_info_oss(self):
        oss_path = os.path.join(self.series, self.avatar_info_name)
        if self.oss_bucket.exist(oss_path):
            return
        self.oss_bucket.put(oss_path, json.dumps(self.blend_info()))

    def blend_and_save_image_oss(self):
        oss_path = os.path.join(self.series, self.avatar_image_name)
        if self.oss_bucket.exist(oss_path):
            return
        self.blend_image()
        with BytesIO() as output:
            self.result_image.save(output, format="PNG")
            self.oss_bucket.put(oss_path, output.getvalue())

    def save(self):
        if self.oss_bucket:
            self.blend_and_save_info_oss()
            self.blend_and_save_image_oss()
        else:
            self.blend_and_save_info_local()
            self.blend_and_save_image_local()
