#
# Jan Gobeli
# 02.2021
# This file initiates a new mongodb or connects to an existing one on 'localhost'.
# It also stores new ticks in a temporary list and saves them in the db when the batch_size is reached.
# 

from arctic import Arctic, TICK_STORE
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class DataBase(object):
    def __init__(self, no_db):
        """
        Initialize the object by creating empty lists, and defining a location to store the data.
        This can be changed but is naturally allocated to localhost. 

        :param no_db: Bool if there is already a database initiated or if one should be created.
        """

        self.logger = logging.getLogger(__name__)

        self.data = list()
        self.trades = list()
        self.counter = 0
        self.trade_count = 0
        self.batch_size = 10000
        
        self.key_mapper = {}

        self.store = Arctic('localhost')

        if no_db:
            self.create_db()
        
        self.connect_db()

    def create_db(self):
        """
        Create a new database library if no_db = True.
        """
        self.store.initialize_library('Tick_store', lib_type=TICK_STORE)
        self.logger.info('New db created.')

    def connect_db(self):
        """
        Connect to a existing library called Tick_store by default.
        """
        self.library = self.store['Tick_store']
        self.logger.info('Connection to db established.')

    def new_tick(self, tick, time):
        """
        Process incoming ticks from Bitmex.
        Save them into a list called "data" and if the batch size is reached,
        write them to the arctic library.

        :param tick: incoming tick from Bitmex which can contain multiple trades/changes at once.
        """
        action = tick['action']
        sub_ticks = tick['data']
        self.counter += 1
        #self.logger.info(self.key_mapper)

        if action == 'partial' or action == 'insert':
            if len(sub_ticks) > 1:
                for n in range(len(sub_ticks)):
                    temp = sub_ticks[n]
                    temp['index'] = time
                    self.data.append(temp)
                    self.key_mapper[temp['id']] = temp['price']
            else:
                temp = sub_ticks[0]
                temp['index'] = time
                self.data.append(temp)
                self.key_mapper[temp['id']] = temp['price']
        else:
            if len(sub_ticks) > 1:
                for n in range(len(sub_ticks)):
                    temp = sub_ticks[n]
                    temp['index'] = time
                    temp['price'] = self.key_mapper[temp['id']]
                    self.data.append(temp)
            else:
                temp = sub_ticks[0]
                temp['index'] = time
                temp['price'] = self.key_mapper[temp['id']]
                self.data.append(temp)
                self.key_mapper[temp['id']] = temp['price']
            
        if self.counter % self.batch_size == 0:
            self.logger.info('{} Ticks Stored'.format(self.counter))
            self.library.write('BTCUSD_ob', self.data)
            self.data.clear()


    def new_trade(self, trade, time):
        """
        Process incoming trades from Bitmex.
        Save them into a list called "trades" and if the batch size is reached,
        write them to the arctic library.

        :param trade: incoming trades from Bitmex.
        """
        sub_ticks = trade['data']
        self.trade_count += 1

        if  len(sub_ticks) > 1:
            for n in range(len(sub_ticks)):
                temp = sub_ticks[n]
                temp['index'] = time
                self.trades.append(temp)
        else:
            temp = sub_ticks[0]
            temp['index'] = time
            self.trades.append(temp)
        
        if self.trade_count % self.batch_size == 0:
            self.logger.info('{} Trades Stored'.format(self.trade_count))
            self.library.write('BTCUSD_trades', self.trades)
            self.trades.clear()

