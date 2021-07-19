import requests
import os
import json
from dotenv import load_dotenv

# TODO: Morph below into a reusable class or function for use within
# the Azure function

load_dotenv()


base_url = "https://api.nytimes.com/svc/topstories/v2/science.json"
api_key = os.environ["NYT_KEY"]
key_param = f"?api-key={api_key}"
res = requests.get(base_url + key_param)

res.raise_for_status()

ny_data = res.json()

if __name__ == "__main__":
    print("Data Size:", len(ny_data))
    print("Keys: ", ny_data.keys())

    results = ny_data["results"]
    print("Results size: ", len(results))

    result_zero = results[0]
    print("First Result Keys: ", result_zero.keys())

    for key, value in result_zero.items():
        print(key, end=": ")
        print(value)
