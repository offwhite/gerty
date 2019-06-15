import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database/gerty.db')
        self.db = self.connection.cursor()

    def call(self):
        print('current_users: ')
        print(self.all('users'))
        #self.execute('delete from users')
        #t = self.insert('users', {'name':'James'})
        # self.db.execute('create table users  ([id] INTEGER PRIMARY KEY,[name] text, [permissions] integer, [last_seen_at] date)')
        return

        print('inserting user...')
        #t = self.insert('users', {'name':'James'})

    def insert(self, table, params):
        values = list(params.values())
        keys_string = ','.join([*params])
        values_string = ','.join(['?']*len(params))
        query = 'insert into ' + table + ' ('+keys_string+') values('+values_string+')'
        return self.execute(query, values)

    def all(self, table):
        return self.execute('select * from '+table).fetchall()

    def find(self, table, id):
        return self.execute('select * from '+table+' where id = '+id).fetchall()

    def execute(self, query, values = None):
        print('[SQL LOG] query: '+query)
        if(values != None):
            print(values)
            q = self.db.execute(query, values)
        else:
            q = self.db.execute(query)

        self.connection.commit()
        return q
