#importing the libraries
import scrapy
#making the class inheriting scrapy.Spider class
class RentoSpider(scrapy.Spider):
    name = 'rento' #name of the spider
    allowed_domains = ['londonrelocation.com'] #allowed domains
    #urls of the areas
    Fulham="https://londonrelocation.com/our-properties-to-rent/properties/?keyword=Fulham&pageset={}"
    Canary_Wharf="https://londonrelocation.com/our-properties-to-rent/properties/?keyword=Canary+Wharf&minimum_price=&maximum_price=&minimum_bedrooms=&property_type=&furnished=&minimum_price_mobile=&maximum_price_mobile={}"
    Angel="https://londonrelocation.com/our-properties-to-rent/properties/?keyword=Angel&minimum_price=&maximum_price=&minimum_bedrooms=&property_type=&furnished=&minimum_price_mobile=&maximum_price_mobile=&pageset=1"
    #starting urls
    start_urls = [Fulham.format(1),Canary_Wharf.format(1),Angel]
    #function to parse the data
    def parse(self, response):
        #selecting all properties in the page and extracting title,price and link of each one property
        for property in response.css('div.row-flex'):
            yield {
                'Title':property.css('div.h4-space > h4 > a::text').get().replace("\n","") ,
                'price per month': property.css('div.bottom-ic > h5::text').get().replace(" £ ","").replace(" pcm",""),
                'Link': response.urljoin(property.css('div.h4-space > h4 > a::attr(href)').get())
            }
        #extracting the next page of fulham by using parse function
        for i in range(2,26):
            next_page = self.Fulham.format(i)
            yield response.follow(next_page, self.parse)
        #extracting the next page of canary wharf by using parse function
        for i in range(2,46):
            next_page = self.Canary_Wharf.format(i)
            yield response.follow(next_page, self.parse)