import scrapy

class AldiSpider(scrapy.Spider):
    name = "aldi"

    start_urls = [
        "https://www.aldi.com.au/en/"
    ]

    def parse(self, response):
        groceries_sub_xpath = "//*[@id='main-nav']//ul[@class='main-nav--level']//li[2]//ul[@role='menu']//li/div/a[@role='menuitem']/@href"
        submenu_links = []
        for submenu in response.xpath(groceries_sub_xpath).extract():
            submenu_links.append(submenu)

        i = 0 #for debugging purposes 1 2 6 7 8
        for link in submenu_links:
            # print(link)
            # 1,2,6,7,8 correspond to the sub categories position that they appear
            # under the grocery category. 1,2,6,7,8 have sublinks you need to pass
            # through before you can get to their product page
            if i not in [1,2,6,7,8]:
                yield scrapy.Request(link, callback=self.parse_link)
            else:
                yield scrapy.Request(link, callback=self.parse_sub_link)

            i += 1
            
            
    def parse_link(self, response):   
        product_info_xpath = "//div[@class='page-wrapper']//article[@id='main-content']//div[@class='tx-aldi-products']//a[@title='to product detail']/div[@class='box m-text-image']"
        # all_products_in_link = response.xpath(product_info_xpath)
        for product in response.xpath(product_info_xpath):       
            product_title = product.xpath(".//div[@class='box--description--header']").get()
            img_url = product.xpath(".//img/@src").extract_first()
            pack_size = product.xpath(".//div[@class='box--price']//span[@class='box--amount']/text()").extract_first()
            price_dollar = product.xpath(".//div[@class='box--price']//span[@class='box--value']/text()").extract_first()
            price_cents = product.xpath(".//div[@class='box--price']//span[@class='box--decimal']/text()").extract_first()
            price_per_unit = product.xpath(".//span[@class='box--baseprice']/text()").extract_first()

            # just cleaning data here
            # Using get instead of extract_first in product title, in case a copyright symbol splits the string
            product_title = product_title.replace('<div class=\"box--description--header\">\n\t\t\t\t\t', '')
            product_title = product_title.replace('\n\t\t\t\t</div>', '')

            # Price append
            total_price = ''
            if price_cents is None:
                total_price = str(price_dollar) + "c"
            elif price_cents is None and price_dollar is None:
                total_price = ''
            else:
                total_price = str(price_dollar) + str(price_cents)

            yield {
                'Product_title': product_title,
                'Product_image': img_url,
                'Packsize': pack_size,
                'Price': total_price,
                'Price per unit': price_per_unit,
            }

    # Method for parsing the sublinks in order to get to their corresponding product page
    def parse_sub_link(self, response):
        # Note we can rely to get the 3rd one as dir like structure starts from
        # root /ALDI Austalia/Groceries/xxx
        category_name = response.xpath("(//span[@itemprop='name'])[3]/text()").extract_first()
        print(category_name)
        if category_name == "Fresh Produce":
            # This is a special case
            link = response.xpath("//div[@class='csc-default']//a[contains(@href, 'fresh-produce/dairy-eggs')]/@href").extract_first()
            yield scrapy.Request(link, callback=self.parse_link)
        else :
            category_name = category_name.lower()
            # special case having the & char here
            if category_name == "laundry & household":
                category_name = category_name.replace(' & ', '-')
            sublinks_xpath = "//div[@class='csc-default']//a[contains(@href, '" + str(category_name) + "/')]/@href"
            for link in response.xpath(sublinks_xpath).extract():
                yield scrapy.Request(link, callback=self.parse_link)
