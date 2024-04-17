from scrapy import Item, Field



class PriceItem(Item):
    _id = Field()
    ticker_ = Field()
    name_ = Field()
    time_entered_ = Field()
    
    timeframe_ = Field()
    time_ = Field()
    close_ = Field()
    open_ = Field()
    high_ = Field()
    low_ = Field()
    volume_ = Field()
    # change_ = Field()

    
class CalendarItem(Item):
    time_ = Field()    # weekly
    data_ = Field()


class NewsItem(Item):
    day_ = Field()
    type_ = Field()
    data_ = Field()     # include date


class MarketItem(Item):
    type_ = Field()
    quote_ = Field()
    period_ = Field()
    window_ = Field()
    data_ = Field()


class PivotsItem(Item):
    day_ = Field()
    type_ = Field()
    period_ = Field()
    data_ = Field()


class BarchartQuotes(Item):
    symbols_ = Field()
    filter_ = Field()
    data_ = Field()
