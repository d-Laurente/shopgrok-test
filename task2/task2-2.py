import re

generic_urls = ["https://www.genericdomain.com/abc/def/1290aodwb23-ghi.img", "https://www.genericdomain.com/abc/31287bdwakj-jkl.img","https://www.genericdomain.com/19unioawd02-jkl.img"]

pattern = r'https://(\w+).(\w+).com/([0-9a-z]{3})?/?([0-9a-z]{3})?/?([0-9a-z]{11})+-(\w+).img'

for url in generic_urls:
    special_sequence = re.sub(pattern, r'\5', url)
    # print(special_sequence)
