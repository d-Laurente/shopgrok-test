import re
product_count_text = "381 Products found"
product_count_int = int(re.search('[0-9]{3}', product_count_text).group(0))

