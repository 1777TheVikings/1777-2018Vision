from abc import ABC
from numpy import ndarray  # used for type checking
from typing import Tuple, List


class ProcessorBase(ABC):
    """ Defines a vision processing pipeline to run on every frame. All
        subclasses must define process(). The internal implementation of
        the pipeline, as well as the keyword arguments supported, are
        left up to the subclass.
    """

    def __init__(self):
        super().__init__()

    def process(self, frame: ndarray, **kwargs) -> Tuple[List, ndarray]:
        pass
