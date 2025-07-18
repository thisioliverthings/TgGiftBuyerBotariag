from dataclasses import dataclass


@dataclass(frozen=True)
class AutoBuySettingDTO:
    id: int
    user_id: int
    status: bool
    price_limit_from: int
    price_limit_to: int
    supply_limit: int
    cycles: int
