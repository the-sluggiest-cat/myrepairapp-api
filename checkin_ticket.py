import inventory_item, enum
from inventory_item import InventoryItem

class CheckinTicketActivity:
    jsonID = None; checkinTicketID = None; userID = None; activity_type = None; metadata = None; createdAt = None

    class CheckinActivityType(enum.Enum):

        CREATION = "CREATION"
        ITEMS_CHANGED = "ITEMS_CHANGED"
        DEVICES_CHANGED = "DEVICES_CHANGED"
        STATUS_CHANGE = "STATUS_CHANGE"
        SAVED = "SAVED"
        
        @classmethod
        def get_from_string(cls, input_str: str | None) -> "CheckinTicketActivity.CheckinActivityType | None":
            if not input_str:
                return None

            try:
                return cls[input_str.upper().replace(' ', '_')]
            except KeyError:
                raise ValueError(f"{input_str} is not a valid category name!")

    def __init__(self, jsonID: str, checkinTicketID: str, userID: str, activity_type: str, metadata: str, createdAt: str):
        self.jsonID = jsonID; self.checkinTicketID = checkinTicketID; self.userID = userID
        self.activity_type = CheckinTicketActivity.CheckinActivityType.get_from_string(activity_type)
        self.metadata = metadata; self.createdAt = createdAt
    
    def __repr__(self):
        return str(self.activity_type)


class CheckInTicket:
    """
    A MyRepairApp ticket.

    This handles organization. WIP.
    """

    jsonID = None; orgID = None; ticketNumber = None; active = None; assigneeID = None; customerID = None; order = None; type = None; status = None
    closedAt = None; warrantyPeriodEnd = None; isWarranty = None; isReturn = None; notToExceed = None; appointmentTime = None; customerPossession = None
    storageBin = None; waitingForPart = None; shipper = None; trackingNumber = None; shipstationShipmentID = None; labelURL = None; claimRepairProvider = None
    createdAt = None; updatedAt = None; assignee = None; customer = None; checkinItems = None; checkinDevices = None; checkinPayments = None; checkinNotes = None
    checkinTicketActivities = None; myProtectionPlans = None

    def __init__(self, jsonID: str, orgID: str, ticketNumber: int, active: bool, assigneeID: str, customerID: str, order: int, _type: dict, status: str, closedAt: str,\
                 warrantyPeriodEnd: str, isWarranty: bool, isReturn: bool, notToExceed: float, appointmentTime: str, customerPossession: bool, storageBin: str,       \
                 waitingForPart: bool, shipper: str, trackingNumber: str, shipstationShipmentID: str, labelURL: str, claimRepairProvider: str, createdAt: str,        \
                 updatedAt: str, assignee: str, customer: str, checkinItems: list[InventoryItem], checkinDevices: str, checkinPayments: str, checkinNotes: str,                \
                 checkinTicketActivities:list[CheckinTicketActivity], myProtectionPlans: list):
        
        self.jsonID = jsonID; self.orgID = orgID; self.ticketNumber = ticketNumber; self.active = active; self.assigneeID = assigneeID; self.customerID = customerID
        self.order = order; self.type = _type; self.status = status; self.closedAt = closedAt; self.warrantyPeriodEnd = warrantyPeriodEnd; self.isWarranty = isWarranty
        self.isReturn = isReturn; self.notToExceed = notToExceed; self.appointmentTime = appointmentTime; self.customerPossession = customerPossession
        self.storageBin = storageBin; self.waitingForPart = waitingForPart; self.shipper = shipper; self.trackingNumber = trackingNumber
        self.shipstationShipmentID = shipstationShipmentID; self.labelURL = labelURL; self.claimRepairProvider = claimRepairProvider
        # - todo: same as inventory_item.py:275 -
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        # ---------------------------------------
        self.assignee = assignee; self.customer = customer; self.checkinItems = checkinItems; self.checkinDevices = checkinDevices; self.checkinPayments = checkinPayments
        self.checkinNotes = checkinNotes; self.checkinTicketActivities = checkinTicketActivities; self.myProtectionPlans = myProtectionPlans
    
    def __repr__(self):
        if len(self.checkinItems) > 0:
            self.checkinItems = [inventory_item.item_from_json(item["inventoryItem"]) for item in self.checkinItems]
        else: self.checkinItems = "NO ITEMS"
        return str(self.__dict__)

def ticket_from_json(json: dict):
    activities = [CheckinTicketActivity(item["id"], item["checkinTicketId"], item["userId"], item["type"], item["metadata"], item["createdAt"]) for item in json["checkinTicketActivities"]]
    return CheckInTicket(json["id"], json["orgId"], json["ticketNumber"], json["active"], json["assigneeId"], json["customerId"], json["order"], json["type"], json["status"],
                  json["closedAt"], json["warrantyPeriodEnd"], json["isWarranty"], json["isReturn"], json["notToExceed"], json["appointmentTime"], json["customerPossession"],
                  json["storageBin"], json["waitingForPart"], json["shipper"], json["trackingNumber"], json["shipstationShipmentId"], json["labelURL"], json["claimRepairProvider"],
                  json["createdAt"], json["updatedAt"], json["assignee"], json["customer"], json["checkinItems"], json["checkinDevices"], json["checkinPayments"],
                  json["checkinNotes"], activities, json["myProtectionPlans"])