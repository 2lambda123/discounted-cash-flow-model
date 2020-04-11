import requests

class FinancialModelingPrep:
    def __init__(self):
        self.base_url = "financialmodelingprep.com"

    def get_quotes(self, symbol):
        """
        Fetches quote data for a company.

        Parameters
        ----------
        symbol : str
            ticker symbol

        Returns
        -------
        dict
            dictionary holding all quote data for the ticker symbol.

            structure of dict can be found in `financial_modeling_api.constants.Constants.QUOTES`
        """
        url = f"{self._version}quote/{symbol.upper()}"

        quote_response, err = self._call_api(url)
        if err:
            raise Exception(f"Failed to fetch quote data for ticker symbol {symbol}.")

        return quote_response.json()

    def get_financials(self, symbol, minimum_years):
        """
        Fetches the income, balance, and cash flow statement 
        using the given ticket symbol.

        Parameters
        ----------
        symbol : str
            ticker symbol
        minimum_years : int
            minimum amount of years of data needed 

        Returns
        -------
        dict
            dictionary holding all financial data for the ticker symbol

            structure of the dict:
            {
                "income_statement": {...},
                "balance_sheet": {...},
                "cash_flow_statement: {...}
            }
        """
        def _has_more_than_minimum(minimum_years, data):
            """
            Determines if we have enough data to perform DCF calculation.

            Parameters
            ----------
            minimum_years : int
                minimum amount of years of data needed
            data : dict
                financial data

                structure of data:
                {
                    "symbol": "XYZ",
                    "financials": [
                        {...},
                        ...
                    ]
                }
            
            Returns
            -------
            bool
                true if we have enough data, false otherwise
            """
            return len(data["financials"]) >= minimum_years

        financials = {}

        income_statement_response, income_err = self._get_income_statement(symbol)
        if income_err:
            raise Exception(f"Failed to fetch income statement for ticker symbol {symbol}.")
        if not _has_more_than_minimum(minimum_years, income_statement_response):
            raise Exception(f"Not enough data found in the income statement for ticker symbol {symbol}.")
        financials["income_statement"] = income_statement_response

        balance_sheet_response, balance_err = self._get_balance_sheet(symbol)
        if balance_err:
            raise Exception(f"Failed to fetch balance sheet for ticker symbol {symbol}")
        if not _has_more_than_minimum(minimum_years, balance_sheet_response):
            raise Exception(f"Not enough data found in the balance sheet for ticker symbol {symbol}.")
        financials["balance_sheet"] = balance_sheet_response

        cash_flow_statement_response, cash_flow_err = self._get_cash_flow_statement(symbol)
        if cash_flow_err:
            raise Exception(f"Failed to fetch cash flow statement for ticker symbol {symbol}")
        if not _has_more_than_minimum(minimum_years, cash_flow_statement_response):
            raise Exception(f"Not enough data found in the cash flow statement for ticker symbol {symbol}.")
        financials["cash_flow_statement"] = cash_flow_statement_response

        return financials

    def _version(self):
        """
        Combines the `self.base_url` with the API version.

        Returns
        -------
        str
            base url + api version
        """
        return self.base_url + "/api/v3/"

    def _financials(self):
        """
        Combines the `self._version` with financials.

        Returns
        -------
        str
            base url + version + financials
        """
        return self._version + "/financials/"

    def _call_api(self, url):
        """
        Performs a GET request using the requests module.

        Parameters
        ----------
        url : str
            url to be called

        Returns
        -------
        dict, Exception
            dict represents the json response coming from the api call. if there is an error, this will be None.
            Exception is an error object where if the api call is successful, this will be none
        """
        try:
            response = requests.get(url)
            return response.json(), None
        except Exception as e:
            return None, e

    def _get_income_statement(self, symbol):
        """
        Makes a GET request for the income statement using the ticker symbol.

        Parameters
        ----------
        symbol : str
            ticker symbol

        Returns
        -------
        dict, Exception
            dict represents the json response coming from the api call. if there is an error, this will be None.
            Exception is an error object where if the api call is successful, this will be none
        """
        url = f"{self._financials}income-statement/{symbol.upper()}"
        return self._call_api(url)

    def _get_balance_sheet(self, symbol):
        """
        Makes a GET request for the balance sheet statement using the ticker symbol.

        Parameters
        ----------
        symbol : str
            ticker symbol

        Returns
        -------
        dict, Exception
            dict represents the json response coming from the api call. if there is an error, this will be None.
            Exception is an error object where if the api call is successful, this will be none
        """
        url = f"{self._financials}balance-sheet-statement/{symbol.upper()}"
        return self._call_api(url)

    def _get_cash_flow_statement(self, symbol):
        """
        Makes a GET request for the cash flow statement using the ticker symbol.

        Parameters
        ----------
        symbol : str
            ticker symbol

        Returns
        -------
        dict, Exception
            dict represents the json response coming from the api call. if there is an error, this will be None.
            Exception is an error object where if the api call is successful, this will be none
        """
        url = f"{self._financials}cash-flow-statement/{symbol.upper()}"
        return self._call_api(url)

