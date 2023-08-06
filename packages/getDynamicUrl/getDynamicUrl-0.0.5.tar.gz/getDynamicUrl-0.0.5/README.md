# Get Dynamic Url
A small library to get the dynamic cloud run url.

### Installation
```
pip install getDynamicUrl
```

### Get started
How to get the dynamic url based in the url in Bigquery

```Python
from getDynamicUrl import Url

# Instantiate a URL object
url_obj = Url()

# Call the get_url method with the headers and bigquery client
# TODO
# db = bigquery client
url_validate = url_obj.get_url(request.headers, db)
```