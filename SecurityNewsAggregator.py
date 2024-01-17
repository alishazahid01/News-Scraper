import scrapy
from SecurtiyNews.items import SecurtiynewsItem
from pymongo import MongoClient

client = MongoClient("mongodb+srv://AlishaZahid:123456789alisha@cybernews.uvgy6mw.mongodb.net/")
db = client.SecurityNewsAggregator

def insertToMongo(title,link):
    collection = db.News
    doc = {"title": title, "link": link}
    inserted = collection.insert_one(doc)
    return inserted.inserted_id

class ScrapeNewsSpider(scrapy.Spider):
    name = "scrape_news"
    allowed_domains = ["darkreading.com", "threatpost.com", "csoonline.com"]
    start_urls = ["https://www.darkreading.com/latest/news"]

    def start_requests(self):
        urls = [
            "https://www.darkreading.com/latest/news",
            "https://threatpost.com/",
            "https://www.csoonline.com"

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = SecurtiynewsItem()

        if "darkreading.com" in response.url:
            yield from self.darkreading(response, item)
        elif "threatpost.com" in response.url:
            yield from self.threatpost(response, item)
        elif "csoonline.com" in response.url:
            yield from self.csoOnline(response, item)

    def darkreading(self, response, item):
        cards = response.css(".topic-content-article")
        for card in cards:
            item['title'] = card.css(".article-title::text").get()
            link_tag = card.css("a")
            item['link'] = link_tag.attrib["href"]
            yield item
            insertToMongo(item['title'],item['link'])
            print("\n")

    def threatpost(self, response, item):
        cards = response.css("article.c-card")
        for card in cards:
            item['title'] = card.css("h2.c-card__title a::text").get()
            article_class = card.css("h2.c-card__title a")
            item['link'] = article_class.attrib["href"]
            yield item
            insertToMongo(item['title'],item['link'])
            print("\n")

    def csoOnline(self, response, item):
        cards = response.css("div.latest-content__card-main")
        for card in cards:
            item['title'] = card.css("h4::text").get()
            article_class = card.css("a")
            item['link'] = article_class.attrib["href"]
            yield item
            insertToMongo(item['title'],item['link'])
            print("\n")

        latest_cards = response.css("div.latest-content__card-secondary")
        for card in latest_cards:
            item['title'] = card.css("h4::text").get()
            article_class = card.css("a")
            item['link'] = article_class.attrib["href"]
            yield item
            insertToMongo(item['title'],item['link'])
            print("\n")

