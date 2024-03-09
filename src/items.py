import requests

async def scrape(session, cookie, cursor, current_max_price, current_min_price):
    response = await session.get(f"https://catalog.roblox.com/v2/search/items/details?category=Accessories&limit=120&Subcategory=2&salesTypeFilter=2&cursor={cursor}&maxPrice={current_max_price}&minPrice={current_min_price}", proxy=cookie.proxy.current, headers={"x-csrf-token": cookie.x_token()})
    if response.status == 429:
        cookie.proxy.next()
        return {"stop": False, "success": False, "message": "ratelimit hit switching proxy", "response": await response.json()}
    elif response.status == 403:
        if response.json()['message'] == "Token Validation Failed":
            cookie.generate_token()
            return {"stop": False, "success": False ,"message": "invalid x-csrf-token. Refreshed token", "response": await response.json()}
        else:
            return {"stop": True, "success": False, "message": "unexpected response", "response": await response.json()}
    elif response.status== 200:
        rsp = await response.json()
        return {"stop": False, "success": True, "message": f"scraped: {len(rsp['data'])} items", "response": rsp}
    else:
        return {"stop": True, "success": False, "message": "unexpected response", "response": await response.json()}