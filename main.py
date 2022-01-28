# Script that generate servers and users on a map and allows to calculate distance between them

import math
import random
import copy


class Server:
    def __init__(self, x, y):
        self.latitude = x
        self.longitude = y


class User:
    def __init__(self, x, y):
        self.latitude = x
        self.longitude = y


if __name__ == '__main__':
    map_width = 100
    map_length = 100

    number_of_users = 20
    number_of_servers = 10

    s = Server(random.randint(0, map_width), random.randint(0, map_length))

    users = []
    servers = []

    for user in range(number_of_users):
        userx = User(random.randint(0, map_width), random.randint(0, map_length))
        users.append(userx)

    server_distance_length = map_length/number_of_servers
    server_distance_width = map_width / number_of_servers
    i = 0
    j = 0
    for server in range(number_of_servers):
        serverx = Server(server_distance_width/2 + i, server_distance_length/2 + j)
        #serverx = Server(random.randint(0, map_width), random.randint(0, map_length))
        i = i + server_distance_width
        j = j + server_distance_length
        servers.append(serverx)

    print(f"\nNumber of users: {len(users)}")
    for user in users:
        print(f"longitude = {user.longitude} + latitude = {user.latitude}")

    print(f"\nNumber of servers: {len(servers)}")
    for server in servers:
        print(f"longitude = {server.longitude} + latitude = {server.latitude}")

    # Wektor e - odległości userów od poszczególnych serwerów w chwili T0
    # wiersze - serwery, kolumny użytkownicy
    e = [[0 for x in range(number_of_users)] for y in range(number_of_servers)]
    s_id = 0
    u_id = 0

    for server in servers:
        for user in users:
            distance = math.sqrt(pow((servers[s_id].latitude - users[u_id].latitude), 2) + pow((servers[s_id].longitude - users[u_id].longitude), 2))
            e[s_id][u_id] = int(distance)
            u_id = u_id + 1
            #print(u_id)
        s_id = s_id + 1
        #print(s_id)
        u_id = 0

    """print("Wektor e:")
    for i in range(number_of_servers):
        print(e[i])"""


    # Wektor ee - odległości userów od poszczególnych serwerów w chwili T1
    # Odległość zmienia się randomowo o (-2,2) w którąś ze stron (olałam to, że użytkownik może wyjść poza mapę xd)
    # wiersze - serwery, kolumny użytkownicy
    ee = copy.deepcopy(e)

    s_id = 0
    u_id = 0
    for server in servers:
        for user in users:
            random_number = random.randrange(-2, 2)
            #print(random_number)
            ee[s_id][u_id] = ee[s_id][u_id] + random_number
            u_id = u_id + 1
        s_id = s_id + 1
        u_id = 0

    #print(e[9][19])
    #print(ee[9][19])

    # Wektor eee - odległości userów od poszczególnych serwerów w chwili T1
    # Odległość zmienia się randomowo o (-2,2) w którąś ze stron (olałam to, że użytkownik może wyjść poza mapę xd)
    # wiersze - serwery, kolumny użytkownicy
    eee = copy.deepcopy(ee)

    s_id = 0
    u_id = 0
    for server in servers:
        for user in users:
            random_number = random.randrange(-4, 4)
            eee[s_id][u_id] = eee[s_id][u_id] + random_number
            u_id = u_id + 1
        s_id = s_id + 1
        u_id = 0

    print("\nPorównanie odległości w trzech chwilach:")
    print(e[9][19])
    print(ee[9][19])
    print(eee[9][19])



    print("\n\nWektor e:")
    for i in range(number_of_servers):
        print(e[i])

    print("\n\nWektor ee:")
    for i in range(number_of_servers):
        print(ee[i])

    print("\n\nWektor eee:")
    for i in range(number_of_servers):
        print(eee[i])


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
