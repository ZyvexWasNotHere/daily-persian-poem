import requests
import random

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

poems = [
    ("حافظ", "دوش دیدم که ملائک در میخانه زدند\nگل آدم بسرشتند و به پیمانه زدند"),
    ("سعدی", "بنی آدم اعضای یکدیگرند\nکه در آفرینش ز یک گوهرند"),
    ("فردوسی", "توانا بود هر که دانا بود\nز دانش دل پیر برنا بود"),
    ("مولانا", "این قافله عمر عجب می‌گذرد\nدریاب دمی که با طرب می‌گذرد"),
]

poet, poem = random.choice(poems)

message = f"""📜 شعر روز

✍️ {poet}

{poem}
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
