# Script that generate servers and users on a map and allows to calculate distance between them

import math
import random
import copy
import numpy as np


class Server:
    def __init__(self, x, y, sid):
        self.latitude = x
        self.longitude = y
        self.server_id = sid


class User:
    def __init__(self, x, y):
        self.latitude = x
        self.longitude = y


if __name__ == '__main__':
    map_width = 100
    map_length = 100

    number_of_users = 20
    number_of_servers = 10

    users = []
    servers = []

    for user in range(number_of_users):
        userx = User(random.randint(0, map_width), random.randint(0, map_length))
        users.append(userx)

    server_distance_length = map_length / number_of_servers
    server_distance_width = map_width / number_of_servers
    i = 0
    j = 0
    sid = 0
    for server in range(number_of_servers):
        serverx = Server(server_distance_width / 2 + i, server_distance_length / 2 + j, sid)
        i = i + server_distance_width
        j = j + server_distance_length
        sid = sid + 1
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
            distance = math.sqrt(pow((servers[s_id].latitude - users[u_id].latitude), 2) + pow(
                (servers[s_id].longitude - users[u_id].longitude), 2))
            e[s_id][u_id] = int(distance)
            u_id = u_id + 1
        s_id = s_id + 1
        u_id = 0


    # Wektor ee - odległości userów od poszczególnych serwerów w chwili T1
    # Odległość zmienia się randomowo o (-2,2) w którąś ze stron (olałam to, że użytkownik może wyjść poza mapę xd)
    # wiersze - serwery, kolumny użytkownicy
    ee = copy.deepcopy(e)

    s_id = 0
    u_id = 0
    for server in servers:
        for user in users:
            random_number = random.randrange(-2, 2)
            # print(random_number)
            ee[s_id][u_id] = ee[s_id][u_id] + random_number
            u_id = u_id + 1
        s_id = s_id + 1
        u_id = 0

    # print(e[9][19])
    # print(ee[9][19])

    # Wektor eee - odległości userów od poszczególnych serwerów w chwili T1
    # Odległość zmienia się randomowo o (-4,4) w którąś ze stron (olałam to, że użytkownik może wyjść poza mapę xd)
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


    print("\n\nVector e:")
    for i in range(number_of_servers):
        print(e[i])

    print("\n\nVector ee:")
    for i in range(number_of_servers):
        print(ee[i])

    print("\n\nVector eee:")
    for i in range(number_of_servers):
        print(eee[i])

# Heuristic algorithm
# assignment of users to servers based only on the cost of transmission (distance) in T0 moment

# Create new vector - nb of columns == nb of users
# the value in each column will represent then the server to which each user will be assigned
user_to_server = []
servers_capacity = [100, 200, 100, 40, 20, 60, 40, 60, 40, 40]

# resources required for one instance of the application
app_req = 20

# array where each row corresponds to the server_id which contains currently used resources
servers_usage = [[0 for x in range(2)] for y in range(number_of_servers)]

servers_usage = np.array(servers_usage)
servers_usage[:, 0] = servers_capacity

# loop that assign users to servers
for user_id in range(number_of_users):

    # for user_id it returns the costs of transmission to each of the servers
    # those costs are taken from vector e
    # - each column in vector e represents cost of transmission to each server for one user
    user_to_server_cost = [row[user_id] for row in e]

    # returns sored costs
    sorted_user_to_server_cost = sorted(user_to_server_cost)

    # loop that assign users to servers
    # - users are assigned to the closest server (lowest transmission costs) that still have free resources
    for cost in sorted_user_to_server_cost:

        # in user_to_server_cost vector
        server_index = user_to_server_cost.index(cost)
        if servers_usage[server_index][0] > (servers_usage[server_index][1] + app_req):
            user_to_server.append(server_index)
            servers_usage[server_index][1] += app_req
            break

# calculate number of users per server
number_of_users_per_server = np.zeros((number_of_servers, 1))
i = 0
for usage in servers_usage[:, 1]:
    number_of_users_per_server[i][0] = (servers_usage[i][1] / app_req)
    i += 1

servers_usage = np.append(servers_usage, number_of_users_per_server, axis = 1)

print(f"\nAssignment of users to servers - columns represent users, value represents server id (0-{number_of_servers-1}):")
print(user_to_server)
print("\nResources available on each server\ consumed resources\ nb of users assigned:")
print(servers_usage)
print("\nTotal usage of resources consumed:")
print(sum(servers_usage[:, 1]))
