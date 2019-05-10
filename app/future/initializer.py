from app.future.models import *
from app.future.souper_utils import PageRipper


def initialize_futures():
    """
    Method checks if the futures and their respective price data are present
    in the database.  If not, the data is retrieved, parsed and inserted
    into the database.
    :return:
    """
    gold = Future.query.filter_by(name='Gold').first()
    silver = Future.query.filter_by(name='Silver').first()

    gold_url = 'https://www.investing.com/commodities/gold-historical-data'
    silver_url = 'https://www.investing.com/commodities/silver-historical-data'

    if not gold:
        Future.create_future(name='Gold',
                             url=gold_url)

    else:
        prices = Price.query.filter_by(future_id=gold.id).all()
        if not prices:
            price_data = PageRipper.get_prices(url=gold_url)
            Price.create_price_series(price_series=price_data, future_id=gold.id)

    if not silver:
        Future.create_future(name='Silver',
                             url=silver_url)

    else:
        prices = Price.query.filter_by(future_id=silver.id).all()
        if not prices:
            price_data = PageRipper.get_prices(url=silver_url)
            Price.create_price_series(price_series=price_data, future_id=silver.id)
