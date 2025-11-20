import enum, json
from enum import Enum
from dataclasses import dataclass, asdict

if __name__ == "inventory_item":
    # import generic
    pass
else:
    from . import generic

class InventoryJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Enum members and dataclasses."""
    def default(self, obj):
        # Handle all Enum members (Condition, Category, etc.)
        if isinstance(obj, Enum):
            return obj.value # Serialize the Enum using its string value

        # Handle nested dataclass objects (like trade_in_device)
        if isinstance(obj, InventoryItem):
            # Recursively convert the dataclass to a dictionary
            # The encoder will then run the dict through this same logic
            return asdict(obj) 
            
        # Let the base class handle other objects (like datetime)
        return json.JSONEncoder.default(self, obj)

class InventoryItemCondition(enum.Enum):
    """
    Class for asserting InventoryItems conditions.

    - "NEW" - Item is brand new, such as from a direct wholesaler or otherwise.
    - "USED" - Item has been through slight damage or visible markings that signify it was owned prior.
    - "REFURBISHED" - Item was considered 'USED' via damage or was inoperable at one point, but was restored with replacement parts or the like.
    - "DAMAGED" - Item is inoperable, extensively damaged, or improperly repaired.
    """

    NEW = "New"
    USED = "Used"
    REFURBISHED = "Refurbished"
    DAMAGED = "Damaged"

    @classmethod
    def get_from_string(cls, input_str: str | None) -> "InventoryItemCondition | None":
        if not input_str:
            return None
        
        # This handles case-insensitivity and ensures the input is valid
        # If the key is not found, ValueError is raised automatically by enum.Enum
        try:
            return cls[input_str.upper().replace(' ', '_')] # Use [] access for case-insensitive lookup of member names
        except KeyError:
            # Handle the specific error message you had
            raise ValueError(f"{input_str} is not a valid condition name!")

class InventoryItemCategory(enum.Enum):
    """
    Class for sorting InventoryItems into categories.

    - "PART" - Item is used for a device repair. See PartItem.
    - "REPAIR" - Item is a device repair element in of itself, such as part replacements and repairs. See RepairItem.
    - "PREPAID" - Item is a prepaid service on a device. See PrepaidItem.
    - "DEVICE" - Item is a device that is sold by the shop. See DeviceItem.
    - "ACCESSORY" - Item is an accessory to a device, such as a charging cable or case. See AccessoryItem.
    - "SERVICE" - Item is an additional service that is not satisfied by the prior groups. See ServiceItem.
    """

    PART = "Part"
    REPAIR = "Repair"
    PREPAID = "Prepaid"
    DEVICE = "Device"
    ACCESSORY = "Accessory"
    SERVICE = "Service"
    TOOL = "Tool"

    @classmethod
    def get_from_string(cls, input_str: str | None) -> "InventoryItemCategory | None":
        if not input_str:
            return None
        
        try:
            return cls[input_str.upper().replace(' ', '_')]
        except KeyError:
            raise ValueError(f"{input_str} is not a valid category name!")

class InventoryItemType:
    class RepairItem(enum.Enum):
        """
        Enum for sorting InventoryItem repairs into types.

        - "PHONE" - Repair is done on a cellphone.
        - "TABLET" - Repair is done on a tablet lacking a built-in keyboard and running a mobile-intentioned OS.
        - "LAPTOP" - Repair is done on a laptop computer.
        - "COMPUTER" - Repair is done on a desktop or handheld computer. If the handheld is running a mobile-intentioned OS, this is classed as a Game instead.
        - "GAME" - Repair is done on a game console or gaming handheld. If console runs a desktop OS, this is classed as a Computer instead.
        - "DRONE" - Repair is done on a drone.
        - "MISCELLANEOUS" - Repair is done on a device that falls outside most classifications, but is still considered a "device", like cameras or accessories.
        - "OTHER" - Repair is done on a device that falls outside of these classifications.
        """

        PHONE = "Repair - Phone"
        TABLET = "Repair - Tablet"
        LAPTOP = "Repair - Laptop"
        COMPUTER = "Repair - Computer"
        GAME = "Repair - Game"
        DRONE = "Repair - Drone"
        MISCELLANEOUS = "Repair - Miscellaneous"
        OTHER = "Repair - Other"

        @classmethod
        def get_from_string(cls, input_str: str | None) -> "InventoryItemType.RepairItem | None":
            if not input_str:
                return None

            try:
                return cls[input_str.upper().replace(' ', '_')]
            except KeyError:
                raise ValueError(f"{input_str} is not a valid repair type!")

    class PartItem(enum.Enum):
        """
        Enum for sorting InventoryItem parts into types.

        PartItem is intended to be fetched from the `get_from_string` function with one of the following:
        - "PHONE" - Part belongs in a cellphone.
        - "TABLET" - Part belongs in a tablet lacking a built-in keyboard and running a mobile-intentioned OS.
        - "LAPTOP" - Part belongs in a laptop computer.
        - "COMPUTER" - Part belongs in a desktop or handheld computer. If the handheld is running a mobile-intentioned OS, this is classed as a Game instead.
        - "GAME" - Part belongs in a game console or gaming handheld. If console runs a desktop OS, this is classed as a Computer instead.
        - "DRONE" - Part belongs in a drone.
        - "SPECIAL ORDER" - Part is difficult to find or is not easily found in each of the prior categories.
        - "OTHER" - Part belongs in a device that falls outside of these classifications.
        """

        PHONE = "Phone"
        TABLET = "Tablet"
        LAPTOP = "Laptop"
        COMPUTER = "Computer"
        GAME = "Game"
        DRONE = "Drone"
        SPECIAL_ORDER = "Special Order"
        OTHER = "Other"

        @classmethod
        def get_from_string(cls, input_str: str | None) -> "InventoryItemType.PartItem | None":
            if not input_str:
                return None

            try:
                return cls[input_str.upper().replace(' ', '_')]
            except KeyError:
                raise ValueError(f"{input_str} isn't a valid device to receive any parts!")

    class ServiceItem(enum.Enum):
        """
        Enum for sorting InventoryItem services into types.

        - "UNLOCK" - Service is done to unlock a device from its carrier.
        - "CLAIM" - Service is done by the order of an insurance claim or warranty repair.
        - "OTHER" - Service falls outside of these classifications.
        """

        UNLOCK = "Unlock"
        CLAIM = "Claim"
        OTHER = "Other"


        @classmethod
        def get_from_string(cls, input_str: str | None) -> "InventoryItemType.ServiceItem | None":
            if not input_str:
                return None

            try:
                return cls[input_str.upper().replace(' ', '_')]
            except KeyError:
                raise ValueError(f"{input_str} isn't a valid service!")

    class AccessoryItem(enum.Enum):
        """
        Enum for sorting InventoryItem accessories into types.

        - "AUDIO" - Accessory is used for audio (headphones/speakers).
        - "CASE" - Accessory protects the exterior of the device from visible damage.
        - "SCREEN PROTECTOR" - Accessory protects the fragile, glass, screen.
        - "POWER" - Accessory keeps the device powered.
        - "OTHER" - Accessory falls outside of these classifications.
        """

        AUDIO = "Audio"
        CASE = "Case"
        SCREEN_PROTECTOR = "Screen Protector"
        POWER = "Power"
        OTHER = "Other"

        @classmethod
        def get_from_string(cls, input_str: str | None) -> "InventoryItemType.AccessoryItem | None":
            if not input_str:
                return None

            try:
                return cls[input_str.upper().replace(' ', '_')]
            except KeyError:
                raise ValueError(f"{input_str} isn't a valid accessory item!")

    class PrepaidItem(enum.Enum):
        """
        Enum for sorting InventoryItem prepaid actions into types.

        - "ACTIVATION" - Prepaid device is activated with a plan.
        - "PLAN" - Prepaid device is provided a plan.
        - "SIM" - Prepaid device is provided with a SIM card and plan.
        - "OTHER" - Prepaid action is outside of these conditions.
        """

        ACTIVATION = "Activation"
        PLAN = "Plan"
        SIM = "SIM"
        OTHER = "Other"

        @classmethod
        def get_from_string(cls, input_str: str | None) -> "InventoryItemType.PrepaidItem | None":
            if not input_str:
                return None

            try:
                return cls[input_str.upper().replace(' ', '_')]
            except KeyError:
                raise ValueError(f"{input_str} isn't a valid prepaid item!")

    class DeviceItem(enum.Enum):
        """
        Enum for sorting InventoryItem devices into types.

        - "PHONE" - Cellphone.
        - "TABLET" - Tablet, or bigger cellphone. Lacks built-in keyboard.
        - "LAPTOP" - Laptop computer.
        - "COMPUTER" - Desktop or handheld computer. If the handheld is running a mobile-intentioned OS, this is classed as a Game instead.
        - "GAME" - Game console or gaming handheld. If console runs a desktop OS, this is classed as a Computer instead.
        - "DRONE" - Drone.
        - "OTHER" - Device that falls outside of these classifications.
        """

        PHONE = "Phone"
        TABLET = "Tablet"
        LAPTOP = "Laptop"
        COMPUTER = "Computer"
        GAME = "Game"
        DRONE = "Drone"
        OTHER = "Other"

        @classmethod
        def get_from_string(cls, input_str: str | None) -> "InventoryItemType.DeviceItem | None":
            if not input_str:
                return None

            try:
                return cls[input_str.upper().replace(' ', '_')]
            except KeyError:
                raise ValueError(f"{input_str} isn't a valid device type!")
            
    class ToolItem(enum.Enum):
        """Urgh."""

        TOOL = "Tool"

        @classmethod
        def get_from_string(cls, input_str: str | None) -> "InventoryItemType.DeviceItem | None":
            return cls["TOOL"]
    
    def get_from_string(input: str | None) -> "InventoryItemType":
        if input is None: return None
        if len(input) == 0: return None

        try:
            item_type, item = [s.strip() for s in input.split("-", 1)]
        except ValueError:
            if input.upper() == "TOOLS": return InventoryItemType.ToolItem.get_from_string(input)
            raise ValueError("Input must be in 'CATEGORY - TYPE' format")
        if item_type.upper() not in ["REPAIR", "DEVICE", "PREPAID", "PART", "ACCESSORY", "SERVICE"]:
            raise ValueError(f"{item_type} is not a valid type!")
        match item_type.upper():
            case "REPAIR":    return InventoryItemType.RepairItem.get_from_string(item)
            case "DEVICE":    return InventoryItemType.DeviceItem.get_from_string(item)
            case "PREPAID":   return InventoryItemType.PrepaidItem.get_from_string(item)
            case "PART":      return InventoryItemType.PartItem.get_from_string(item)
            case "ACCESSORY": return InventoryItemType.AccessoryItem.get_from_string(item)
            case "SERVICE":   return InventoryItemType.ServiceItem.get_from_string(item)

# BEHOLD. THE NIGHTMARES.
@dataclass(repr=True)
class InventoryItem(generic.GenericItem):
    """A MyRepairApp inventory item. This handles organization, inventory counts, price, cost, etcetera."""
    item_id = None; store_id = None; sku = None; manufacturer = None; type = None; name = None; in_stock = None; condition = None; bin = None; supplier_id = None
    price = None; created_at = None; updated_at = None; note = None; inventoried = None; serialized = None; active = None; cost = None; category = None; serial_num = None
    carrier = None; color = None; storage = None; trade_in_condition = None; trade_in_device = None; trade_in_status = None; additional_info = None; is_rebate = None; tax_free = None
    grouping_id = None; repair_provider = None; is_motorola_sku = None; pulled = None; ordered = None; back_ordered = None; sku_pulled = None; sku_instock = None

    def __init__(self, item_id: str = None, store_id: str = None, sku: str = None, manufacturer: str = None, item_type: InventoryItemType = None, name: str = None,
                 in_stock: int = None, condition: InventoryItemCondition = None, bin: str = None, supplier_id: str = None, price: float = None, created_at: str = None,
                 updated_at: str = None, note: str = None, inventoried: bool = None, serialized: bool = None, active: bool = None, cost: float = None,                              
                 category: InventoryItemCategory = None, serial_num: str = None, carrier: str = None, color: str = None, storage: str = None,
                 trade_in_condition: InventoryItemCondition = None, trade_in_device: "InventoryItem" = None, trade_in_status = None, additional_info = None,
                 is_rebate: bool = None, tax_free: bool = None, grouping_id: str = None, repair_provider: str = None,
                 is_motorola_sku: bool = None, # seems irrelevant? applies only to "motorola authorized repair centers", probably 
                 # relevance: int = None, # can likely be ignored, this is a by-query basis
                 pulled: bool = None, ordered: bool = None, back_ordered: bool = None, sku_pulled: bool = None, sku_instock: bool = None):
        
        super().__init__("inventory")
        
        self.item_id = item_id; self.store_id = store_id; self.sku = sku; self.manufacturer = manufacturer; self.type = item_type; self.name = name; self.in_stock = in_stock
        self.condition = condition; self.bin = bin; self.supplier_id = supplier_id; self.price = price
        # - todo: translate the below into datetime instances -
        self.created_at = created_at
        self.updated_at = updated_at
        # -----------------------------------------------------
        self.note = note; self.inventoried = inventoried; self.serialized = serialized; self.active = active; self.cost = cost; self.category = category; self.serial_num = serial_num
        self.carrier = carrier; self.color = color; self.storage = storage; self.trade_in_condition = trade_in_condition; self.trade_in_device = trade_in_device
        self.trade_in_status = trade_in_status; self.additional_info = additional_info; self.is_rebate = is_rebate; self.taxFree = tax_free; self.grouping_id = grouping_id
        self.repair_provider = repair_provider; self.is_motorola_sku = is_motorola_sku; self.pulled = pulled; self.ordered = ordered; self.back_ordered = back_ordered
        self.sku_pulled = sku_pulled; self.sku_instock = sku_instock
    
    def __repr__(self):
        return self.name
    
    def export(self):
        raw_dump = json.loads(json.dumps(self.__dict__, cls=InventoryJSONEncoder)) # awful.
        returned = raw_dump
        del returned["ITEM_TYPE"]
        returned["id"] = returned["item_id"]; del returned["item_id"]
        returned["storeId"] = returned["store_id"]; del returned["store_id"]
        print(returned)
        return returned

    
    # def __dict__(self):
    #     return {
    #         "id": self.item_id,
    #         "storeId": self.store_id,
    #         "sku": self.sku,
    #         "manufacturer": self.manufacturer,
    #         "item_type": self.type,
    #         "name": self.name,
    #         "instock": self.in_stock,
    #         "condition": self.condition,

    #     }

def item_from_json(data: dict) -> InventoryItem:
    # Use .get() for optional keys
    pulled = data.get("pulled")
    ordered = data.get("ordered")
    back_ordered = data.get("backOrdered")
    sku_pulled = data.get("skuPulled")
    sku_instock = data.get("skuInstock")
    
    # Safely get and convert condition, category, and type
    condition = InventoryItemCondition.get_from_string(data.get("condition"))
    category  = InventoryItemCategory.get_from_string(data.get("category"))
    item_type = InventoryItemType.get_from_string(data.get("type"))
    
    # Pass arguments by name, which is clearer than positional arguments
    return InventoryItem(
        item_id = data.get("id"),
        store_id = data.get("storeId"),
        sku = data.get("sku"),
        manufacturer = data.get("manufacturer"),
        item_type = item_type,
        name = data.get("name"),
        in_stock = data.get("instock"),
        condition = condition,
        bin = data.get("bin"),
        supplier_id = data.get("supplierId"),
        price = data.get("price"),
        created_at = data.get("createdAt"),
        updated_at = data.get("updatedAt"),
        note = data.get("note"),
        inventoried = data.get("inventoried"),
        serialized = data.get("serialized"),
        active = data.get("active"),
        cost = data.get("cost"),
        category = category,
        serial_num = data.get("serialNum"),
        carrier = data.get("carrier"),
        color = data.get("color"),
        storage = data.get("storage"),
        trade_in_condition = data.get("tradeInCondition"), # Needs to be parsed like 'condition'... eventually
        trade_in_status = data.get("tradeInStatus"),
        additional_info = data.get("additionalInfo"),
        is_rebate = data.get("isRebate"),
        tax_free = data.get("taxFree"),
        grouping_id = data.get("groupingId"),
        repair_provider = data.get("repairProvider"),
        is_motorola_sku = data.get("isMotorolaSku"),
        pulled = pulled,
        ordered = ordered,
        back_ordered = back_ordered,
        sku_pulled = sku_pulled,
        sku_instock = sku_instock
    )