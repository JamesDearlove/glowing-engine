from pydantic import BaseModel
from typing import List

Color = int
Colors = list[int]

class BaseControlParams(BaseModel):
    pass

class PulseParams(BaseControlParams):
    colors: Colors
    reverse: bool

