import MySQLdb 
from pymemcache.client import base

memcached_client = base.Client(('memcachedcache.m0hama.cfg.use1.cache.amazonaws.com', 11211))
TTL_INT = 60 * 3; # 3 min cache

mydb = MySQLdb.connect(
  "supplierdb.cluster-ckqqk6qrvh4g.us-east-1.rds.amazonaws.com",
  "nodeapp",
  "coffee",
  "COFFEE"
)

def main():
    print('Adding a new bean item')

    db_query = "INSERT INTO beans (supplier_id, type, product_name, price, description, quantity) VALUES (%s, %s, %s, %s, %s, %s)"
    vals = (1, 'Java Java','Worlds greatest bean','38.00','Nutty tasting coffee.',400 )

    mycursor = mydb.cursor()

    try:
        mycursor.execute(db_query, vals)
        print(mycursor.rowcount, "record(s) inserted into RDS.")
        mydb.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        #closing the database cursor
        mycursor.close()
        return None
        exit()

    #closing the database cursor
    mycursor.close()

    print("FLUSH the CACHE as it is stale")
    #we could update just this item if we stored each item in the cache but this is fine for testing.
    try:
        memcached_call = memcached_client.delete('all_beans')
        print('Purged the cache:', memcached_call)
    except:
        print('There was a problem flushing the cache' )

if __name__ == "__main__":
    main()
"""
Copyright @2021 [Amazon Web Services] [AWS]
    
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
