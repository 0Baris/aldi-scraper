import re

product_count_text = "381 Products found"
count = re.match(r"\d+", product_count_text).group(0)
product_count_int = int(count)
print(product_count_int)
