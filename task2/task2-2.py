import re

generic_urls = ["https://www.genericdomain.com/abc/def/1290aodwb23-ghi.img", "https://www.genericdomain.com/abc/31287bdwakj-jkl.img","https://www.genericdomain.com/19unioawd02-jkl.img"]

for url in generic_urls:
    print(re.match('^[0-9a-z]{11}', url).group(0))
    special_sequence = [re.match('^[0-9a-z]', url).group(0)]