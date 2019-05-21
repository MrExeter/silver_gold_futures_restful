from statistics import mean, variance

from dateutil.parser import parse
from flask import request, jsonify
from flask_restful import Api, Resource
from sqlalchemy import desc, asc

from app import create_app
from app.future.initializer import initialize_futures
from app.future.models import *


class Commodity(Resource):

    def get(self):
        """
        Handle the get request for commodity pricing information.
        :return: returns JSON output, either an error message or the pricing
        information and statistics in JSON format
        """
        if request.is_json:
            data = request.get_json()   # Retrieve json from get request if using postman
        else:
            data = request.args         # Retrieve args from get request if using curl

        commodity_type = data.get("commodity_type").lower()     # Make lowercase
        start_date = parse(data.get("start_date")).date()
        end_date = parse(data.get("end_date")).date()

        return self.commodity_info(commodity_type, start_date, end_date)

    def commodity_info(self, commodity_type, start_date, end_date):
        """
        Function that retrieves and formats the commodity pricing information
        :param commodity_type: String name of commodity i.e., gold, silver, lead
        :param start_date: First date of price series
        :param end_date: Last date of price series
        :return: Returns either an error message or the pricing information
        """
        try:
            # Check if the commodity id exists in the database
            comm_id = Future.query.filter_by(name=commodity_type).first().id
        except:
            # Return error message
            return jsonify({'Message': "Invalid commodity name : {}".format(commodity_type)})

        # Determine valid date range for price data requests
        min_date = Price.query.filter(Price.future_id == comm_id).order_by(asc(Price.date)).first().date
        max_date = Price.query.filter(Price.future_id == comm_id).order_by(desc(Price.date)).first().date

        # Error messages for dates outside valid date range
        error_1 = "Sorry, your start date must be greater than or equal to {}".format(min_date)
        error_2 = "Sorry, your end date must be less than or equal to {}".format(max_date)

        if start_date < min_date:
            return jsonify({'Message': error_1})
        elif end_date > max_date:
            return jsonify({'Message': error_2})

        # Retrieve Price information for selected commodity and date range.
        price_query = Price.query.filter(Price.future_id == comm_id,
                                         Price.date >= start_date,
                                         Price.date <= end_date).order_by(asc(Price.date)).all()

        return self.price_statistics(price_query)

    def price_statistics(self, price_list):
        """
        Function that takes price series, calculates mean, variance and
        constructs output JSON
        :param price_list: List of Prices each having a date and price
        :return: Formatted JSON object, showing both date, price information
        as well as the mean and variance of the price data.
        """
        data = {}
        for item in price_list:
            data[item.date.isoformat()] = round(item.price, 2)

        avg = round(mean(c.price for c in price_list), 2)
        var = round(variance(c.price for c in price_list), 2)

        return jsonify(
            {
                "data": data,
                "mean": avg,
                "variance": var
            })


if __name__ == '__main__':
    flask_app = create_app('dev_sqlite')

    api = Api(flask_app)
    api.add_resource(Commodity, "/commodity")

    with flask_app.app_context():
        # Create database if not already
        db.create_all()

        # Retrieve and populate the futures data
        initialize_futures()

    flask_app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)

