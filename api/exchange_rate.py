import httpx

URL_PATH = "https://www.cbr-xml-daily.ru/daily_json.js"

async def _get_rate_value(weight, price):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.cbr-xml-daily.ru/daily_json.js")
        response_data = response.json()

    rate = float(response_data["Valute"]["USD"]["Value"])
    return (weight * 0.5 + price * 0.01) * rate


