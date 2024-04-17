import sqlite3
from crawldata.functions import *
from crawldata.items import *


class MongodbPipeline:
    collection = ""

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        
        self.create_indexes()
    
    def close_spider(self, spider):
        self.client.close()

    def create_indexes(self):
        collections = {
            "stock_price": [('ticker_', 1), ('day_', 1)],
            "index_price": [('ticker_', 1), ('day_', 1)],
            # Add more collections if needed
        }
        
        for collection_name, unique_fields in collections.items():
            collection = self.db[collection_name]
            collection.create_index(unique_fields, unique=True)
    
    def process_item(self, item, spider):
        if isinstance(item, PriceItem):
            collection_name = "stock_price" if "stock" in spider.name else "index_price"
            collection = self.db[collection_name]
            unique_fields = ('ticker_', 'day_')
            insert_unique_document(collection, dict(item), unique_fields)
        # elif isinstance(item, ComponentsItem):
        #     collection = self.db["components"]
        #     update_index_components(collection, item.get('ticker_'), item.get('name_'), item.get('id_'), item.get('components_'))
        return item
    

class SQLitePipeline:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            db_file=settings.get('DATABASE_NAME')
        )
    
    def open_spider(self, spider):
        self.conn = sqlite3.connect(f"{SQLITE3_PATH}/{self.db_file}.sqlite3")   # db
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.cursor = self.conn.cursor()
        self.create_prices_table()

    def create_prices_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                _id TEXT PRIMARY KEY,
                ticker_ TEXT,
                name_ TEXT,
                time_entered_ TEXT,
                timeframe_ TEXT,
                time_ TEXT,
                close_ REAL,
                open_ REAL,
                high_ REAL,
                low_ REAL,
                volume_ INTEGER
            )
        ''')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_prices_id ON prices (_id)')
        self.conn.commit()

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, PriceItem):
            self.cursor.execute("SELECT _id FROM prices WHERE _id = ?", (item['_id'],))
            existing_item = self.cursor.fetchone()

            if existing_item is None:
                self.cursor.execute("""
                    INSERT INTO prices (_id, ticker_, name_, time_entered_, timeframe_, time_, close_, open_, high_, low_, volume_)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item['_id'], item['ticker_'], item['name_'], item['time_entered_'],
                    item['timeframe_'], str(item['time_']), item['close_'], item['open_'],
                    item['high_'], item['low_'], item['volume_']
                ))
            else:
                should_update = False
                for key in ['ticker_', 'name_', 'time_entered_', 'timeframe_', 'time_', 'close_', 'open_', 'high_', 'low_', 'volume_']:
                    if item[key] != existing_item[key]:
                        should_update = True
                        break
                if should_update:
                    self.cursor.execute("""
                        UPDATE prices
                        SET ticker_ = ?, name_ = ?, time_entered_ = ?, timeframe_ = ?, time_ = ?,
                            close_ = ?, open_ = ?, high_ = ?, low_ = ?, volume_ = ?
                        WHERE _id = ?
                    """, (
                        item['ticker_'], item['name_'], item['time_entered_'], item['timeframe_'],
                        str(item['time_']), item['close_'], item['open_'], item['high_'],
                        item['low_'], item['volume_'], item['_id']
                    ))

            self.conn.commit()
        return item