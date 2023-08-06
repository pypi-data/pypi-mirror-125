import json

from elasticsearch import Elasticsearch

from .log import logger


class Index:
    """
    不同系列使用不同索引
    文档id使用头像的id方便
    头像id的构成:
        只考虑组件构成，不考虑组件合成顺序，相同组件组成的头像为同一个头像
        根据组件字母排序，组件名称+组件名字，拼接字符串+hash为唯一id，oss中从meta中读取组件列表
    """

    def __init__(self, url, index_name):
        self.url = url
        self.client = Elasticsearch(self.url)
        self.index_name = index_name

    def index_setting(self):
        return {
            "mappings": {
                "dynamic": False,
                "_source": {
                    "enabled": "true",
                },
                "properties": {
                    "body": {
                        "type": "keyword",
                    },
                    "cloth": {
                        "type": "keyword",
                    },
                    "hair": {
                        "type": "keyword",
                    },
                    "horn": {
                        "type": "keyword",
                    },
                    "eyes": {
                        "type": "keyword",
                    },
                    "mouth": {
                        "type": "keyword",
                    },
                    "background": {
                        "type": "keyword",
                    },
                    "image_path": {
                        "type": "keyword",
                    },
                    "image_name": {
                        "type": "keyword",
                    },
                },
            },
        }

    def create_index(self):
        return self.client.indices.create(
            index=self.index_name,
            body=self.index_setting(),
        )

    def exists_index(self):
        return self.client.indices.exists(
            index=self.index_name,
        )

    def delete_index(self):
        return self.client.indices.delete(
            index=self.index_name,
        )

    def delete_and_create(self):
        if self.exists_index():
            self.delete_index()
        self.create_index()

    def refresh_index(self):
        return self.client.indices.refresh(
            index=self.index_name,
        )

    def add_one_doc(self, doc):
        # id = doc["symbol"] + doc["shortName"]
        return self.client.index(
            index=self.index_name,
            body=json.dumps(doc),
        )

    def query_template(self):
        return {
            "query": {
                "bool": {
                    "must": [
                    ]
                }
            }
        }

    def search_one(self):
        input = {
            "mouth": "mouth5",
            "body": "body-2",
        }
        search_list = []
        for key, value in input.items():
            search_item = dict()
            search_item["match"] = {
                key: value,
            }
            search_list.append(search_item)
        result = self.query_template()
        result["query"]["bool"]["must"] = search_list
        logger.info(f"search_one: {result}")
        return result
