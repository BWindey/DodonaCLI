import json


def courses_data(connection, headers):

    connection.request("GET", "/courses.json?tab=my", headers=headers)
    res = connection.getresponse()
    if res.status != 200:
        print('Error connecting to dodona: ' + str(res.status))
        print(res.reason)
        return
    data = res.read()
    connection.close()

    json_data = json.loads(data)

    return json_data
