from app.future.models import *
from app.future.souper_utils import PageRipper
from app.links import futures


def initialize_futures():
    """
    Method checks if the futures and their respective price data are present
    in the database.  If not, the data is retrieved, parsed and inserted
    into the database.
    :return: Nothing
    """

    for item in futures:
        comm = Future.query.filter_by(name=item.get('name')).first()
        if not comm:
            Future.create_future(name=item.get('name'),
                                 url=item.get('url'))

        else:
            prices = Price.query.filter_by(future_id=comm.id).all()
            if not prices:
                price_data = PageRipper.get_prices(url=item.get('url'))
                Price.create_price_series(price_series=price_data,
                                          future_id=comm.id)
