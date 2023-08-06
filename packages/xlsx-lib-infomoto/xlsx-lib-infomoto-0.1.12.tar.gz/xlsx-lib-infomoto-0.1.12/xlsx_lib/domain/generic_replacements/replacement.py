from typing import List, Optional

from camel_model.camel_model import CamelModel

from xlsx_lib.domain.generic_replacements.replacement_part import ReplacementPart


# TODO: To dataclass with Optional[list[ReplacementPart]]
class Replacement(CamelModel):
    name: str
    reference: Optional[str]
    observations: Optional[str]
    parts: Optional[List[ReplacementPart]]

