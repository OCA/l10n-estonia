# Copyright 2018 Ventor, Xpansa Group <https://ventor.tech/>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from datetime import datetime
import logging

from lxml import etree

from odoo.addons.currency_rate_update.services.currency_getter_interface \
    import CurrencyGetterInterface

_logger = logging.getLogger(__name__)


class UpdateServiceEEBEEP(CurrencyGetterInterface):
    """Implementation of Currency_getter_factory interface for Eesti Pank."""

    code = 'EE_BEEP'
    name = 'Bank of Estonia (Eesti Pank)'
    supported_currency_array = [
        "AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "GBP", "HKD",
        "HRK", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK",
        "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD",
        "ZAR",
    ]

    def rate_retrieve(self, dom, ns, curr):
        """Parse a dom node to retrieve currencies data."""
        res = {}
        xpath_curr_rate = ("/gesmes:Envelope/def:Cube/def:Cube/"
                           "def:Cube[@currency='%s']/@rate") % (curr.upper())
        res['rate_currency'] = float(
            dom.xpath(xpath_curr_rate, namespaces=ns)[0]
        )
        return res

    def get_updated_currency(
        self,
        currency_array,
        main_currency,
        max_delta_days,
    ):
        """Implementation of abstract method of Curreny_getter_interface."""
        url = 'https://www.eestipank.ee/en/exchange-rates/export/xml/latest'

        # We do not want to update the main currency
        if main_currency in currency_array:
            currency_array.remove(main_currency)
        _logger.debug("BEEP currency rate service: connecting...")
        rawfile = self.get_url(url)
        dom = etree.fromstring(rawfile)
        _logger.debug("BEEP sent a valid XML file")
        beep_ns = {
            'gesmes': 'http://www.gesmes.org/xml/2002-08-01',
            'def': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'
        }
        rate_date = dom.xpath(
            '/gesmes:Envelope/def:Cube/def:Cube/@time',
            namespaces=beep_ns,
        )[0]
        # Don't use DEFAULT_SERVER_DATE_FORMAT here, because it's
        # the format of the XML of EB, not the format of Odoo server !
        rate_date_datetime = datetime.strptime(rate_date, '%Y-%m-%d')
        self.check_rate_date(rate_date_datetime, max_delta_days)
        # We dynamically update supported currencies
        self.supported_currency_array = dom.xpath(
            "/gesmes:Envelope/def:Cube/def:Cube/def:Cube/@currency",
            namespaces=beep_ns
        )
        self.supported_currency_array.append('EUR')
        _logger.debug(
            "Supported currencies = %s",
            self.supported_currency_array,
        )
        self.validate_cur(main_currency)
        if main_currency != 'EUR':
            main_curr_data = self.rate_retrieve(dom, beep_ns, main_currency)
        for curr in currency_array:
            self.validate_cur(curr)
            if curr == 'EUR':
                rate = 1 / main_curr_data['rate_currency']
            else:
                curr_data = self.rate_retrieve(dom, beep_ns, curr)
                if main_currency == 'EUR':
                    rate = curr_data['rate_currency']
                else:
                    rate = (curr_data['rate_currency'] /
                            main_curr_data['rate_currency'])
            self.updated_currency[curr] = rate
            _logger.debug(
                "Rate retrieved : 1 %s = %s %s",
                main_currency,
                rate,
                curr,
            )
        return self.updated_currency, self.log_info
