import datetime
import os
from sodapy import Socrata
import time


class DataInitService:
    @staticmethod
    def get_all_data(_collection_crime, _last_update_collection, _first_error_date_collection):
        client = Socrata("data.cityofchicago.org", os.environ['APP_TOKEN'])

        years = ['2001-01-01T00:00:00', '2002-01-01T00:00:00', '2003-01-01T00:00:00', '2004-01-01T00:00:00',
                 '2005-01-01T00:00:00', '2006-01-01T00:00:00', '2007-01-01T00:00:00', '2008-01-01T00:00:00',
                 '2009-01-01T00:00:00', '2010-01-01T00:00:00', '2011-01-01T00:00:00', '2012-01-01T00:00:00',
                 '2013-01-01T00:00:00', '2014-01-01T00:00:00', '2015-01-01T00:00:00', '2016-01-01T00:00:00',
                 '2017-01-01T00:00:00', '2018-01-01T00:00:00', '2019-01-01T00:00:00', '2020-01-01T00:00:00',
                 '2021-01-01T00:00:00', '2022-01-01T00:00:00'
                 ]

        i = 0
        last_date_updated = datetime.datetime.strptime('2001-01-01T00:00:01.000', '%Y-%m-%dT%H:%M:%S.%f')
        try:
            for index, value in enumerate(years):
                print(value)
                if len(years) <= index + 1:
                    break
                search_string = 'date between \'' + years[index] + '\' and \'' + years[index + 1] + '\''
                print(search_string, 'search_string')
                for item in client.get_all("ijzp-q8t2", where=search_string):
                    _collection_crime.insert_one(item)
                    i += 1
                    if i % 10000 == 0:
                        print('{0} items inserted'.format(i))
                        print(item)
                        print(value)
                    updated_on = datetime.datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S.%f')
                    if updated_on > last_date_updated:
                        updated_on_dic = {"last_updated_on": updated_on}
                        _last_update_collection.delete_many({})
                        _last_update_collection.insert_one(updated_on_dic)
                        last_date_updated = updated_on
                time.sleep(30)

            print('{0} items Saved to MONGO'.format(i))
        except TimeoutError:
            first_error_dic = {"first_error_dic": updated_on}
            _first_error_date_collection.insert_one(first_error_dic)
            print('{0} items Saved to MONGO ERROR'.format(i))

    @staticmethod
    def get_new_data(_collection_crime, _last_update_collection):
        last_update = _last_update_collection.find_one()
        print(last_update, 'last update')
        date_last_update = last_update['last_updated_on']

        begin_date = date_last_update.strftime('%Y-%m-%dT%H:%M:%S')
        print(begin_date, 'begin date')

        today = datetime.datetime.now()
        end_date = today.strftime("%Y-%m-%dT%H:%M:%S")
        print('Parse Today ' + end_date)
        i = 0
        client = Socrata("data.cityofchicago.org", os.environ['APP_TOKEN'])
        search_string = 'date between \'' + begin_date + '\' and \'' + end_date + '\''
        for item in client.get_all("ijzp-q8t2", where=search_string):
            _collection_crime.insert_one(item)
            i += 1
            if i % 10000 == 0:
                print('{0} items inserted'.format(i))
                print(item)
            updated_on = datetime.datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S.%f')
            if updated_on > date_last_update:
                updated_on_dic = {"last_updated_on": updated_on}
                _last_update_collection.delete_many({})
                _last_update_collection.insert_one(updated_on_dic)
                date_last_update = updated_on

    @staticmethod
    def is_db_empty(last_update_collection):
        cursor = last_update_collection.find()
        results = list(cursor)
        return len(results) == 0
