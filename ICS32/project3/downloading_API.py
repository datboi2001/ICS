#Datthew Nguyen, 61886297
import json
import urllib
import urllib.parse
import urllib.request


def build_url_with_query(api_key: str, symbol: str, url: str) -> str:
    """This function will use the parameters provided and build an URL that can get
    a stock's data from the Alpha Advantage API.
    """
    query = {'function':'TIME_SERIES_DAILY' ,
             'symbol': symbol, 'outputsize': 'full',
             'apikey': api_key}
    return url + '/query?' + urllib.parse.urlencode(query)


def data_retrieval(link: str) -> dict or int:
    """Attempt to connect to the URL. It opens the URL, decodes it, turns the JSON object
    into a Python object. Return that Python object. If the http request fails, the urllib
    package will raise error. I will catch that error in an except clause. Return 0 if there
    is no network connection or 404 or 503 if the webpage is not found or the service is unavailable.
    """
    try:
        data = urllib.request.urlopen(link)
        json_object = data.read().decode(encoding = 'utf-8')
        stock_info = json.loads(json_object)
        return stock_info
    except urllib.error.HTTPError as e:
        return str(e)[11:14]
    except urllib.error.URLError:
        return 0
    except json.decoder.JSONDecodeError:
        return 200
    except ValueError:
        return '404'
    else:
        data.close()
