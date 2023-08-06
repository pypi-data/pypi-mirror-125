import itertools
import multiprocessing

from .avatar_instance import AvatarInstance
from .consumer import Consumer
# from .index import Index
from .unit_group import UnitGroup


class BlendTask:
    def __init__(self, instance):
        self.instance = instance

    def __call__(self):
        return self.instance.save()

    def __str__(self):
        return self.instance.avatar_name


class Avatar:
    def __init__(self, series, root, unit_list, oss_bucket=None):
        self._series = series
        self._root = root
        self._unit_list = unit_list  # 顺序加载 代表涂层顺序
        self._oss_bucket = oss_bucket

        self._unit_group_list = []
        self._load()

        self.tasks = multiprocessing.JoinableQueue()
        self.num_consumers = multiprocessing.cpu_count() * 2

        # self.index = Index(
        #     url="127.0.0.1:9200",
        #     index_name="test_search_avatars",
        # )
        # self.index.delete_and_create()

    @property
    def series(self):
        return self._series

    @property
    def root(self):
        return self._root

    @property
    def unit_list(self):
        return self._unit_list

    @property
    def unit_group_list(self):
        return self._unit_group_list

    @property
    def oss_bucket(self):
        return self._oss_bucket

    def _start(self):
        for _ in range(self.num_consumers):
            Consumer(self.tasks).start()

    def _join(self):
        for _ in range(self.num_consumers):
            self.tasks.put(None)
        self.tasks.join()

    def _load(self):
        for unit_name in self.unit_list:
            self.unit_group_list.append(
                UnitGroup(self.series, self.root, unit_name, oss_bucket=self.oss_bucket).unit_list)

    def generate(self):
        for i in itertools.product(*self.unit_group_list):
            instance = AvatarInstance(self.series, i, oss_bucket=self.oss_bucket)
            if not instance.valid:
                continue
            instance.save()

    def generate_parallel(self):
        self._start()
        for i in itertools.product(*self.unit_group_list):
            instance = AvatarInstance(self.series, i, oss_bucket=self.oss_bucket)
            if not instance.valid:
                continue
            self.tasks.put(BlendTask(instance))
        self._join()
    #
    # def search(self):
    #     count = 0
    #     for i in itertools.product(*self.unit_group_list):
    #         instance = AvatarInstance(i, oss_bucket=self.oss_bucket)
    #         self.index.add_one_doc(instance.result_info)
    #         count += 1
    #         logger.info(f"count: {count}")
