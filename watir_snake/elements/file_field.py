from errno import ENOENT

import six
from os import path

from .input import Input
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class FileField(Input):
    def set(self, filepath):
        """
        Set the file field to the given path

        :param filepath: path to the file
        :raises: ENOENT
        """
        if not path.exists(filepath):
            raise ENOENT
        self._element_call(lambda _: self.element.send_keys(filepath))

# TODO: container
# TODO: collection
