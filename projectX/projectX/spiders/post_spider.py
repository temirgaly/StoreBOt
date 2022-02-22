import scrapy

class PostSpider(scrapy.Spider):
    name='posts'
    start_urls=[
        'https://www.trendyol.com/kadin-t-shirt-x-g1-c73'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse,cookies={'language':'tr','storefrontId':'1','countryCode':'TR'})
    
    def parse(self, response):
        filename='post-trendy.html'

        wrp=response.css('div.p-card-wrppr::attr(data-id)').getall()
        print(wrp)
        # with open(filename, 'wb') as f:
        #     f.write(response.body)