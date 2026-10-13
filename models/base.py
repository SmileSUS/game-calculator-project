from abc import ABC, abstractmethod


class BaseEntity(ABC):

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def to_file_string(self):
        pass