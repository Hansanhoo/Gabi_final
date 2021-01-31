from pymongo import MongoClient
from service.dataInitService import DataInitService
import threading
import time

UPDATETIME = 24 * 60 * 60


class GetData:

    def __init__(self):
        self.conn = MongoClient("mongo", 27017)
        self.db = self.conn.mydb
        self.collection_crime = self.db.chicago_crime
        self.last_update_collection = self.db.last_update
        self.first_error_date_collection = self.db.first_error_date
        print("Connection to Mongo ready \n Collections loaded")

    def invoke(self):
        if DataInitService.is_db_empty(self.last_update_collection):
            DataInitService.get_all_data(self.collection_crime, self.last_update_collection,
                                         self.first_error_date_collection)
        threading.Thread(target=self.get_actual_data_job()).start()
        print('started thread')

    def get_actual_data_job(self):
        while True:
            DataInitService.get_new_data(self.collection_crime, self.last_update_collection)
            print("job running")
            time.sleep(UPDATETIME)
