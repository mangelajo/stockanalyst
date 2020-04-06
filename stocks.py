import datetime
import requests
import requests_cache
import os


requests_cache.install_cache('data/api_cache')

_HEADERS = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': os.getenv('RAPIDAPI_KEY')
    }


class Stock(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self._financials = cleanup_dict(self._get_financials())
        self._details = cleanup_dict(self._get_details())
        self.financials = AttrDict(self._financials)
        self.details = AttrDict(self._details)

    def _get_financials(self):
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"
        response = requests.request("GET", url, headers=_HEADERS, params={"symbol": self.symbol})
        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        return response.json()

    def _get_details(self):
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-detail"
        querystring = {"region":"US","lang":"en","symbol":self.symbol}
        response = requests.request("GET", url, headers=_HEADERS, params=querystring)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        return response.json()

    def __str__(self):
        return "%s\t%s\t%.2f\t%.2f" % (self.symbol, self.website,
                                       self.PE or -1.0,
                                       self.fPE or -1.0)

    def find(self, key):
        d = {'details': self._details, 'financials': self._financials}
        return find_paths(d, key)

    def find_detail(self, name):
        return find_key(self._details, name)

    def find_financial(self, name):
        return find_key(self._financials, name)

    @property
    def beta(self):
        return self.details.defaultKeyStatistics.beta

    def beta3Year(self):
        return self.details.defaultKeyStatistics.beta3Year

    @property
    def sector(self):
        return self.details.summaryProfile.sector

    @property
    def industry(self):
        return self.details.summaryProfile.industry

    @property
    def website(self):
        return self.details.summaryProfile.website

    @property
    def PE(self):
        return self.details.summaryDetail.trailingPE

    @property
    def fPE(self):
        return self.details.summaryDetail.forwardPE

    @property
    def dividendYield(self):
        return self.details.summaryDetail.dividendYield

    @property
    def price(self):
        return self.details.price.regularMarketOpen

    @property
    def yearlyEarnings(self):
        return self.details.earnings.financialsChart.yearly

def find_key(dictionary, key, path=''):
    if key in dictionary:
        #print(key, 'found @', path)
        val = dictionary[key]
        return val
    else:
        for k in dictionary:
            sub_item = dictionary[k]
            if not isinstance(sub_item, dict):
                continue
            res = find_key(sub_item, key, path + '/' + k)
            if res:
                return res


def find_paths(this, keyPart, path=''):
    found = []
    if isinstance(this, dict):
        for k, v in this.items():
            if path == '':
                k_path = k
            else:
                k_path = path + '.' + k
            if keyPart in k:
                print(k_path)
                found.append(k_path)
            if isinstance(v, dict):
                found.extend(find_paths(v, keyPart, k_path))
    elif isinstance(this, list):
        for i in this:
            found.extend(find_paths(i, keyPart, path))
    return found


def _final_value(val):
    if isinstance(val, dict):
        raw = val.get('raw')
        fmt = val.get('fmt')
        if raw is None:
            return
        if fmt:
            if fmt and len(val['fmt'].split('-')) == 3:
                # print(raw, val['fmt'])
                return datetime.datetime.fromtimestamp(raw)
        return raw


def cleanup_dict(dictionary):
    for k, v in dictionary.items():
        fv = _final_value(v)
        if fv is not None:
            # print(v, fv)
            dictionary[k] = fv
            continue
        if isinstance(v, dict):
            cleanup_dict(v)
        if isinstance(v, list):
            for i in range(len(v)):
                x = v[i]
                if isinstance(x, dict):
                    cleanup_dict(x)
                else:
                    fv = _final_value(x)
                    if fv is not None:
                        v[i] = fv

    return dictionary


class AttrDict(dict):
    MARKER = object()

    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError('expected dict')

    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, AttrDict):
            value = AttrDict(value)
        super(AttrDict, self).__setitem__(key, value)

    def __getitem__(self, key):
        found = self.get(key, AttrDict.MARKER)
        if found is AttrDict.MARKER:
            found = AttrDict()
            super(AttrDict, self).__setitem__(key, found)
        return found

    __setattr__, __getattr__ = __setitem__, __getitem__
