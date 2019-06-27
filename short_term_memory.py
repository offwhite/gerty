from datetime import datetime, timedelta

# we have a user_list of id = [name, last_seen_time, permissions]
class StmUnit:
    def __init__(self, db):
        self.db = db
        self.all_users = None
        self.time_format = '%Y-%m-%d %H:%M:%S'
        self.minutes_retention = 1
        self.prev_users_in_room = {}
        self.users_in_room = {}

    def update_users_in_room(self):
        self.prev_users_in_room = self.users_in_room
        self.users_in_room = {}
        if(self.all_users == None):
            return self.users_in_room

        cutoff = datetime.now() - timedelta(minutes=self.minutes_retention)
        for id in self.all_users:
            user = self.all_users[id]
            if(datetime.strptime(user[1], self.time_format) > cutoff):
                self.users_in_room[id] = user

    def new_users(self):
        return self.a_minus_b(self.users_in_room.keys(), self.prev_users_in_room.keys())

    def see_user(self, id):
        updated_user = list(self.all_users[id])
        updated_user[1] = self.now_str()
        self.all_users[id] = updated_user

    def users_name(self, id):
        if(len(self.users()) <= id):
            return 'not in db: ' + str(id)
        return self.all_users[id][0]

    def now_str(self):
        return datetime.now().strftime(self.time_format)

    def user(self, id):
      return self.all_users[id]

    def users(self):
        if(self.all_users != None):
            return self.all_users

        users = {}
        for (id, name, permissions, last_seen_at) in self.db.all('users'):
            users[id] = [name, last_seen_at, permissions]
        self.all_users = users
        print('[INFO] Users set')
        print(users)
        return users

    def a_minus_b(self, list_a, list_b):
        return [item for item in list_a if item not in list_b]
