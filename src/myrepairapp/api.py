import requests, logging, asyncio, random, enum
if __name__ == "__main__":
    pass
    # import exceptions, inventory_item, checkin_ticket, generic
else:
    from . import exceptions, inventory_item, checkin_ticket, generic
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger(__name__)

class UpdateType(enum.Enum):
    """The item type that is being updated."""

    CHECKIN_TICKET = "Checkin Ticket"
    INVENTORY = "Inventory" # inventory item

class MyRepairApp:
    headers = None
    MYREPAIRAPP_LINK = "https://www.myrepairapp.com/api/v2"

    def __init__(self, token: str):
        self.headers = {"X-Api-Key": token}
        try:
            response = requests.get(self.MYREPAIRAPP_LINK+"/inventory", headers=self.headers)
            match response.status_code:
                case 401: raise exceptions.Forbidden
                case 405: pass # expected. can't get the entire inventory. for some reason.
        except requests.exceptions.ConnectionError:
            log.exception("Failed to connect to MyRepairApp. Are you connected to the internet?")

    async def __get(self, link: str, params: dict = None):
        try:
            while True:
                response = requests.get(link, headers=self.headers, params=params)
                match response.status_code:
                    case 401: raise exceptions.Forbidden()
                    case 405: raise exceptions.MethodNotAllowed()
                    case 429:
                        random_delay = random.uniform(10, 60)
                        log.warn(f"Too many requests. Trying again in {round(random_delay, 2)}s.")
                        await asyncio.sleep(random_delay)
                    case 500: raise exceptions.InternalServerError(response.reason)
                    case 200: break
        except requests.exceptions.ConnectionError:
            log.exception("Failed to connect to MyRepairApp. Are you connected to the internet?")
        return response
    
    async def __patch(self, update_type: UpdateType, data: generic.GenericItem, changed: dict):
        _patch_data = None
        match update_type:
            case UpdateType.INVENTORY:
                assert type(data) is inventory_item.InventoryItem
                _patch_data = data.export()
                non_matching_keys = [key for key in changed.keys() if key not in _patch_data.keys()]
                for key in non_matching_keys:
                    del changed[key]
                print(changed)
                print(_patch_data)
                link = self.MYREPAIRAPP_LINK+f"/inventory/{_patch_data['id']}"
        try:
            while True:
                response = requests.patch(link, headers=self.headers, data=changed)
                match response.status_code:
                    case 400: raise exceptions.BadRequest(response.json())
                    case 401: raise exceptions.Forbidden()
                    case 405: raise exceptions.MethodNotAllowed()
                    case 429:
                        random_delay = random.uniform(10, 60)
                        log.warn(f"Too many requests. Trying again in {round(random_delay, 2)}s.")
                        await asyncio.sleep(random_delay)
                    case 500: raise exceptions.InternalServerError()
                    case 200: break
        except requests.exceptions.ConnectionError:
            log.exception("Failed to connect to MyRepairApp. Are you connected to the internet?")
        return response.json()
    
    
    def update_item(self, data: generic.GenericItem, changed: dict):
        # raise NotImplementedError("Function reserved for future API update, estimated mid-December 2025.")
        # get the type of the item
        update_type = None
        match data.ITEM_TYPE:
            case "inventory": update_type = UpdateType.INVENTORY
            case "checkin ticket": raise NotImplementedError("Complicated function that goes beyond our limits currently. WIP.")
        response = asyncio.run(self.__patch(update_type, data, changed))
        return response

    def inventory_search(self, query: str):
        link = self.MYREPAIRAPP_LINK+"/inventory/search"
        response = asyncio.run(self.__get(link, params={"query": query}))
        item = [inventory_item.item_from_json(elem) for elem in response.json()]
        return item
    
    def ticket_search(self, query: str, closed_included: bool = False):
        link = self.MYREPAIRAPP_LINK+"/checkin-ticket"
        # https://myrepairapp.com/api/v2/checkin-ticket?query=<string>&closed=<boolean>
        query_link = f"{link}?query={query}&closed={str(closed_included)}"
        response = asyncio.run(self.__get(query_link))
        return [checkin_ticket.ticket_from_json(ticket) for ticket in response.json()["tickets"]]