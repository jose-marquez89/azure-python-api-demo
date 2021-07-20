import requests
import os
import json
import logging
from dotenv import load_dotenv

FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

# TODO: Morph below into a reuable class or function for use within
# the Azure function

load_dotenv()


def get_data(section='science'):
    base_url = "https://api.nytimes.com/svc/topstories/v2/science.json"
    api_key = os.environ["NYT_KEY"]
    key_param = f"?api-key={api_key}"
    res = requests.get(base_url + key_param)
    
    try:
        res.raise_for_status()
    except Exception as err:
        logging.error(err)
        return

    data = res.json()

    return data

if __name__ == "__main__":
    ny_data = get_data()
    print("Data Size:", len(ny_data))
    print("Keys: ", ny_data.keys())

    results = ny_data["results"]
    print("Results size: ", len(results))

    result_zero = results[0]
    print("First Result Keys: ", result_zero.keys())

    for key, value in result_zero.items():
        print(key, end=": ")
        print(value)

    rkeys = result_zero.keys()
    same_keys = []
    item_type = []

    for result in results:
        same_keys.append(result.keys() == rkeys)
        item_type.append(result['item_type'])

    logging.debug(all(same_keys))
    logging.debug(all(map(lambda x: x == 'Article', item_type)))
