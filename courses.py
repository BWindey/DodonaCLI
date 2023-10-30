import json


def show_the_courses(connection, headers, short_tab='m'):
    if short_tab in ('m', 'my'):
        tab = 'my'
    elif short_tab in ('f', 'featured'):
        tab = 'featured'
    elif short_tab in ('i', 'institution'):
        tab = 'institution'
    elif short_tab in ('a', 'all'):
        tab = 'all'
    else:
        return

    connection.request("GET", "/courses.json?tab=" + tab, headers=headers)
    res = connection.getresponse()
    if res.status != 200:
        print('Error connecting to dodona: ' + str(res.status))
        print(res.reason)
        return
    data = res.read()
    connection.close()

    json_data = json.loads(data)

    print('\033[4;94m' + tab.capitalize() + ' courses:\033[0m')
    courses = []
    for course in json_data:
        courses.append((str(course['id']), course['name'], course['teacher']))
    max_course_id_length = max(len(e[0]) for e in courses)
    max_course_name_length = max(len(e[1]) for e in courses)

    courses = sorted(courses, key=lambda x: x[1])
    for e in courses:
        print(f'{e[0].ljust(max_course_id_length)}: \033[1m{e[1].ljust(max_course_name_length)}\033[0m\tby {e[2]}')
