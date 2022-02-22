from dotenv import load_dotenv, find_dotenv
import os
import psycopg2
import psycopg2.extras

load_dotenv(find_dotenv())
conf={
    'host':os.environ.get('host'),
    'database': os.environ.get('database'),
    'user':os.environ.get('user'),
    'port':os.environ.get('port'),
    'password':os.environ.get('password')
}

class Database:
    __instance=None

    @staticmethod
    def GetInstance():
        if Database.__instance==None:
            Database()
        return Database.__instance

    def __init__(self):
        if Database.__instance!=None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance=self
        self.conn=psycopg2.connect(**conf)


    def GetValuesList(self, tableName):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query = 'SELECT * from {0}'.format(tableName)
            cur.execute(query)
            response = cur.fetchall()
            return response

    def InsertValuesToTable(self, tableName, values):
        dynamicQuery='INSERT INTO {0} ({1}) VALUES ({2}) RETURNING idx'.format(tableName, ','.join(v[0] for v in values), ','.join('%s' for _ in range(len(values))))
        dynamicValues=tuple([v[1] for v in values])
        
        with self.conn.cursor() as cur:
            cur.execute(dynamicQuery, dynamicValues)
            self.conn.commit()

            return cur.fetchone()[0] 
    
    def CheckProductByStoreId(self, storeId):
        with self.conn.cursor() as cur:
            query=f'select exists(select 1 from product where storeid=\'{storeId}\')'
            cur.execute(query)
            response = cur.fetchone()
            return response[0]
    
    def GetProductByStoreId(self, storeId):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query=f'select * from product where storeid=\'{storeId}\''
            cur.execute(query)
            return cur.fetchone()
    
    def GetImagesByProductIdx(self, idx):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query=f'select * from images where pid=\'{idx}\''
            cur.execute(query)
            return cur.fetchall()

if __name__=='__main__':
    db=Database.GetInstance()
    response=db.GetProductByStoreId('129611781')
    print(response['idx'])


    # db=Database().GetInstance()
    # print('3',db)

    # db=Database().GetInstance()
    # print('4',db)

    