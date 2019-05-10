
from app import db


# Futures model
class Future(db.Model):
    """
    Class describes a commodities future, it describes a one-to-many relationship,
    one (Future) to many (Prices)
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(36), unique=True)
    url = db.Column(db.String(256), unique=True)
    prices = db.relationship('Price', cascade="all,delete", backref='future', lazy=True)

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Name %r>' % self.name

    @classmethod
    def create_future(cls, name, url):
        future = cls(name=name,
                     url=url)

        db.session.add(future)
        db.session.commit()
        return future

    @classmethod
    def delete_future(cls, future):
        db.session.delete(future)
        db.session.commit()


class Price(db.Model):
    """
    Class describes a price for a commodity future
    there is a many (price) to one (future) relationship
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    price = db.Column(db.Float)
    future_id = db.Column(db.Integer, db.ForeignKey('future.id'))

    def __init__(self, date, price, future_id):
        self.date = date
        self.price = price
        self.future_id = future_id

    @classmethod
    def create_price(cls, price_data, future_id):
        price = cls(date=price_data.get("Date"),
                    price=price_data.get("Price"),
                    future_id=future_id)

        db.session.add(price)
        db.session.commit()
        return price

    @classmethod
    def create_price_series(cls, price_series, future_id):
        for item in price_series:
            price = cls.create_price(price_data=item,
                                     future_id=future_id)


