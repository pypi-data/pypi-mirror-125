import os
import pickle

from via import logger
from via import settings
from via.constants import CACHE_DIR
from via.utils import get_size


class BaseCache():

    def __init__(self, cache_type=None):
        assert cache_type is not None
        self.loaded = False
        self.data = {}
        self.last_save_len = -1
        self.cache_type = cache_type

    def get(self, k):
        if not self.loaded:
            self.load()

        return self.data.get(k, None)

    def set(self, k, v, skip_save=False):
        self.data[k] = v
        if not skip_save:
            self.save()

    def create_dirs(self):
        if not os.path.exists(self.fp):
            logger.debug(f'Creating cache dir: {self.fp}')
            os.makedirs(
                os.path.dirname(self.fp),
                exist_ok=True
            )

    def save(self):
        if len(self.data) <= self.last_save_len:
            return
        logger.debug(f'Saving cache {self.cache_type}')
        self.create_dirs()
        with open(self.fp, 'wb') as f:
            pickle.dump(self.data, f)
        self.last_save_len = len(self.data)

    def load(self):
        logger.debug(f'Loading cache {self.cache_type}')
        if not os.path.exists(self.fp):
            self.create_dirs()
            self.save()

        with open(self.fp, 'rb') as f:
            self.data = pickle.load(f)
        self.loaded = True
        self.last_save_len = len(self.data)
        logger.debug(
            'Size of %s cache: %sMB',
            self.cache_type,
            get_size(self.data) / (1000 ** 2)
        )

    @property
    def dir(self) -> str:
        return os.path.join(CACHE_DIR, self.cache_type, settings.VERSION)

    @property
    def fp(self) -> str:
        return os.path.join(self.dir, 'cache.pickle')
