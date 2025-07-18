from dataclasses import dataclass


@dataclass(frozen=True)
class GiftDTO:
    id: str
    gift_id: int
    emoji: str
    star_count: int
    remaining_count: int
    total_count: int
    is_new: bool = True
