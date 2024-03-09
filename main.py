import json
import asyncio
import aiohttp
import ujson
import aiofiles

from src import proxy, cookie, items

async def main(config):
    cookie_class = cookie.cookie(proxy.make(20))
    cursor = ''
    config_file = []
    already_found = []
    current_max_price = 5
    current_min_price = 1
    
    async with aiohttp.ClientSession() as session:
        while True:
            response = await items.scrape(session, cookie_class, cursor, current_max_price, current_min_price)
            if response["stop"]:
                print(response["message"])
                break
            elif not response["success"]:
                print(response["message"])
            else:
                print(response["message"] + f", total items found: {len(config_file)}, Max Price: {current_max_price}, Min Price: {current_min_price}")
                response_items = [item for item in response["response"]["data"] if item['id'] not in already_found]
                already_found.extend(response_items)
                if response_items:
                    config_file.extend(response_items)
                    async with aiofiles.open("items.json", "w") as json_file:
                        await json_file.write(ujson.dumps(config_file, indent=4))
                if cursor.startswith("9"):
                    current_min_price = current_max_price
                    current_max_price = current_max_price + 10
                    cursor = ""
                    continue
                else:            
                    cursor = response["response"]["nextPageCursor"]
                    if not cursor: 
                        current_min_price = current_max_price
                        current_max_price = round(current_max_price * 1.2)
                        cursor = ""

config = json.loads(open("config.json", "r").read())
asyncio.run(main(config))
