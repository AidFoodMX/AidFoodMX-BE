from dataclasses import dataclass
from datetime import datetime

# Schema to represent a Beneficiary.
# This dataclass stores the details of a person receiving aid, including their name, satisfaction score,
# the date they were registered as a beneficiary, and the region where they are located.
@dataclass
class Beneficiary:
    id: int  # Unique identifier for the beneficiary.
    name: str  # Name of the beneficiary.
    satisfaction: int  # Satisfaction rating of the beneficiary (e.g., 1 to 5).
    date_registered: datetime  # Date when the beneficiary was registered.
    region: str  # Region where the beneficiary is located.

# Schema to represent a Food Package.
# This dataclass stores information about food packages provided, including a list of satisfaction scores,
# the information about the package, and the date it was rated by beneficiaries.
@dataclass
class FoodPackage:
    id: int  # Unique identifier for the food package.
    info: str  # Description or information about the food package contents.
    satisfaction_scores: list[int]  # A list to store satisfaction scores from beneficiaries.
    date_rated: datetime  # Date when the food package was rated.

# Schema to represent the Inventory.
# This dataclass tracks the amount of different food categories available in the inventory (e.g., non-perishables, cereals),
# and records the last time the inventory was updated.
@dataclass
class Inventory:
    non_perishables: int  # Quantity of non-perishable food items in the inventory.
    cereals: int  # Quantity of cereals in the inventory.
    fruits_vegetables: int  # Quantity of fruits and vegetables in the inventory.
    dairy: int  # Quantity of dairy products in the inventory.
    meat: int  # Quantity of meat in the inventory.
    last_updated: datetime  # Timestamp indicating when the inventory was last updated.