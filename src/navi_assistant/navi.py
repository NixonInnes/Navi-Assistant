# src/navi_assistant/navi.py

import os

from . import GLOBAL_CONFIG_DIR, GLOBAL_CACHE_DIR, GLOBAL_TOOLS_DIR
from .cache import NaviCache, default_cache
from .config import NaviConfig, default_config
from .utils import JsonHandler


class Navi:
    LOCAL_CONFIG_DIR = ".navi"
    LOCAL_CACHE_DIR = ".navi"
    LOCAL_TOOLS_DIR = os.path.join(".navi", "tools")
    config: NaviConfig
    cache: NaviCache

    def __init__(self, is_global: bool = False, load_defaults: bool = False):
        self.__is_global = is_global
        
        self._config_handler = JsonHandler[NaviConfig](self.config_file)
        self._cache_handler = JsonHandler[NaviCache](self.cache_file)

        if load_defaults:
            self.config = default_config()
            self.cache = default_cache()
        else:
            self.config = self._config_handler.load()
            self.cache = self._cache_handler.load()
    
    @property
    def is_global(self) -> bool:
        return self.__is_global

    @property
    def config_dir(self) -> str:
        return GLOBAL_CONFIG_DIR if self.is_global else self.LOCAL_CACHE_DIR

    @property
    def config_file(self) -> str:
        return os.path.join(self.config_dir, "config.json")

    @property
    def cache_dir(self) -> str:
        return GLOBAL_CACHE_DIR if self.is_global else self.LOCAL_CACHE_DIR

    @property
    def cache_file(self) -> str:
        return os.path.join(self.cache_dir, "cache.json")

    @property
    def tools_dir(self) -> str:
        return GLOBAL_TOOLS_DIR if self.is_global else self.LOCAL_TOOLS_DIR

    def load_config(self) -> None:
        self.config = self._config_handler.load()

    def load_cache(self) -> None:
        self.cache = self._cache_handler.load()

    def save_config(self) -> None:
        self._config_handler.save(self.config)
    
    def save_cache(self) -> None:
        self._cache_handler.save(self.cache)


    

