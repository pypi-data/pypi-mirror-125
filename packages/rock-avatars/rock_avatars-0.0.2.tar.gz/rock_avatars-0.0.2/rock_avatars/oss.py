import oss2


class OssBucket:
    def __init__(
            self,
            bucket_name,
            access_key_id=None,
            access_key_secret=None,
            endpoint_url=None,
    ):
        self._bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint_url, bucket_name)

    @property
    def bucket(self):
        return self._bucket

    def exist(self, key):
        return self.bucket.object_exists(key)

    def put(self, key, body):
        return self.bucket.put_object(key, body)

    def get(self, key):
        return self.bucket.get_object(key).read()
