from re import sub
from decimal import Decimal
import requests
from bs4 import BeautifulSoup

def get_price_int(prodUrl):
    PRODUCT_URL = prodUrl

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    page = requests.get(url=PRODUCT_URL, headers=headers)

    soup = BeautifulSoup(page.content, "lxml")

    product_price = soup.find("div", class_="price-new").get_text()
    product_price = product_price.replace(",", ".")
    product_price_int = Decimal(sub(r"[^\d\-.]", "", product_price))
    return product_price_int

def get_price(prodUrl):
    PRODUCT_URL = prodUrl

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    page = requests.get(url=PRODUCT_URL, headers=headers)

    soup = BeautifulSoup(page.content, "lxml")

    product_price = soup.find("div", class_="price-new").get_text()
    product_price = product_price.replace(",", ".")
    return product_price

def get_title(prodUrl):
    PRODUCT_URL = prodUrl

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    page = requests.get(url=PRODUCT_URL, headers=headers)

    soup = BeautifulSoup(page.content, "lxml")

    product_title = soup.find("h1", class_="sc-fubCfw cqjzZF product__title").get_text()
    return product_title

 
u1 = "https://www.perekrestok.ru/cat/372/p/desert-a-rostagrokompleks-cizkejk-tvoroznyj-s-vanilu-15-40g-4230660"
u2 = "https://www.perekrestok.ru/cat/373/p/syrok-a-rostagrokompleks-tvoroznyj-glazirovannyj-v-molocnom-sokolade-s-vanilu-26-50g-4227614"
u3 = "https://www.perekrestok.ru/cat/372/p/nuga-a-rostagrokompleks-glazirovannaa-v-molocnom-sokolade-40g-4230649"
u4 = "https://www.perekrestok.ru/cat/373/p/syrok-a-rostagrokompleks-tvoroznyj-glazirovannyj-v-molocnom-sokolade-so-sgusenkoj-26-50g-4227615"
u5 = "https://www.perekrestok.ru/cat/373/p/syrok-a-rostagrokompleks-kartoska-tvoroznyj-glazirovannyj-v-molocnom-sokolade-20-50g-4227635"
u6 = "https://www.perekrestok.ru/cat/373/p/syrok-a-rostagrokompleks-tvoroznyj-glazirovannyj-v-temnom-sokolade-s-vanilu-26-50g-4227647"
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------


from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime)
    price = Column(String(64))
    price_int = Column(Numeric(10, 2))
    url = Column(String(64))

    def __repr__(self):
        return f"{self.name} | {self.price}"

engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)

def add_price(title, price, price_int, url):
    is_exist = session.query(Price).filter(
        Price.name==title
    ).order_by(Price.datetime.desc()).first()

    if not is_exist:
        session.add(
            Price(
                name=title,
                datetime=datetime.now(),
                price=price,
                price_int=price_int,
                url=url
            )
        )
        session.commit()
    else:
        if is_exist.price_int != price_int:
            session.add(
                Price(
                    name=title,
                    datetime=datetime.now(),
                    price=price,
                    price_int=price_int
                )
            )
            session.commit()


add_price(get_title(u1), get_price(u1), get_price_int(u1), u1)
add_price(get_title(u2), get_price(u2), get_price_int(u2), u2)
add_price(get_title(u3), get_price(u3), get_price_int(u3), u3)
add_price(get_title(u4), get_price(u4), get_price_int(u4), u4)
add_price(get_title(u4), get_price(u4), get_price_int(u4), u4)
add_price(get_title(u5), get_price(u5), get_price_int(u5), u5)
add_price(get_title(u6), get_price(u6), get_price_int(u6), u6)


items = session.query(Price).all()
for item in items:
    print(item)