import os
import smtplib

from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

load_dotenv()
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

practice_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
# url ="https://www.amazon.es/fire-tv-stick-4k/dp/B0CJKTWTVT/ref=zg_bsnr_c_electronics_d_sccl_2/258-9029977-7588302?pd_rd_w=syF3F&content-id=amzn1.sym.0c440de5-e3f6-4692-a81e-e4eb168275cc&pf_rd_p=0c440de5-e3f6-4692-a81e-e4eb168275cc&pf_rd_r=CX25SRCP8J9602SYB50B&pd_rd_wg=AfkEr&pd_rd_r=fe1bad9f-2efa-4c6b-955f-eca691094897&pd_rd_i=B0CJKTWTVT&psc=1"

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
}
response = requests.get(practice_url, headers=header)

soup = BeautifulSoup(response.content, "html.parser")

price = soup.find(class_="a-offscreen").get_text()

price_without_currency = price.split("$")[1]

price_as_float = float(price_without_currency)
print(price_as_float)

# Mandar email
title = soup.find(id="productTitle").getText().strip()
print(title)

BUY_PRICE = 100

if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}"

    with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_ADDRESS,
            to_addrs=EMAIL_ADDRESS,
            msg=f"Asunto: Alerta Amazon \n\n{message}\n{practice_url}".encode("utf-8")
        )