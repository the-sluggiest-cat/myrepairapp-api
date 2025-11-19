import requests, exceptions, logging, asyncio, random
import inventory_item, checkin_ticket
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger(__name__)

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

    async def __make_request(self, link: str, params: dict = None):
        try:
            while True:
                response = requests.get(link, headers=self.headers, params=params)
                match response.status_code:
                    case 401: raise exceptions.Forbidden
                    case 429:
                        random_delay = random.uniform(10, 60)
                        log.warn(f"Too many requests. Trying again in {round(random_delay, 2)}s.")
                        await asyncio.sleep(random_delay)
                    case 500: raise exceptions.BadRequest(response.content) # untested. maybe it'll work, maybe it won't
                    case 200: break
        except requests.exceptions.ConnectionError:
            log.exception("Failed to connect to MyRepairApp. Are you connected to the internet?")
        return response


    def inventory_search(self, query: str):
        link = self.MYREPAIRAPP_LINK+"/inventory/search"
        response = asyncio.run(self.__make_request(link, params={"query": query}))
        item = [inventory_item.item_from_json(elem) for elem in response.json()]
        return item
    
    def ticket_search(self, query: str, closed_included: bool = False):
        link = self.MYREPAIRAPP_LINK+"/checkin-ticket"
        # https://myrepairapp.com/api/v2/checkin-ticket?query=<string>&closed=<boolean>
        query_link = f"{link}?query={query}&closed={str(closed_included)}"
        response = asyncio.run(self.__make_request(query_link))
        return [checkin_ticket.ticket_from_json(ticket) for ticket in response.json()["tickets"]]
