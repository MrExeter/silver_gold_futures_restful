from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from dateutil.parser import parse


class PageRipper:
    """
    Utility class to perform page scraping and parsing tasks.
    """

    @classmethod
    def page_request(cls, url):
        """
        Method to open a url and request the page information
        :param url: URL of the page
        :return: HTML source for page
        """
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            webpage = BeautifulSoup(webpage, 'lxml')
            return webpage

        except Exception as err:
            return -79, "Error encountered in page request : {}".format(err)

    @classmethod
    def clean_convert(cls, str_value, replace_chr):
        """
        Method to strip unwanted characters from price and percent data
        :param str_value: Raw string representing a float number
        :param replace_chr: Character to be removed e.g., commas, percents,
        currency symbols etc.
        :return: Float value of number
        """
        return float(str_value.text.replace(replace_chr, ''))

    @classmethod
    def parse_date(cls, str_value):
        """
        Method that takes string value of a date and parses it into a date
        object
        :param str_value: Raw date string from html source.
        :return: Date object
        """
        try:
            return parse(str_value).date()

        except Exception as err:
            return -89, "Error encountered in date parser : {}".format(err)

    @classmethod
    def parse_price_data(cls, page):
        """
        Method that parses price and date values from html source
        :param page: HTML source of webpage
        :return: list of dictionaries containing date and price info
        """
        try:
            table = page.find("table", {"id": "curr_table"})
            tbody = table.find("tbody")
            rowz = tbody.findAll("tr")

            ohlc_items = []
            for item in rowz:
                data = item.findAll("td")
                daily_data = {
                    'Date': cls.parse_date(data[0].text),
                    'Price': cls.clean_convert(data[1], ','),
                }

                ohlc_items.append(daily_data)

            return ohlc_items

        except Exception as err:
            return -99, "Error encountered in price parser : {}".format(err)

    @classmethod
    def get_prices(cls, url):
        """
        Method to retrieve futures price series given a url
        :param url: The url of the page containing the price data
        :return: List of dictionaries each containing date and price information
        """
        page = cls.page_request(url=url)
        price_data = cls.parse_price_data(page=page)
        return price_data
