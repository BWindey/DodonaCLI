def submission_data_handler(submission_data: dict) -> str:
    result = ""
    result += submission_tabs_handler(submission_data)
    result += "\n"
    result += submission_code_annotations(submission_data)
    return result


'''
# There were some problems, list them here
for tab in json_results['groups']:
    print(tab['description'] + ": " + str(tab['badgeCount']) + " tests failed.")

    if tab['badgeCount'] > 0:
        print("Failed exercises:")
        for context in tab['groups']:
            if not context['accepted']:
                for test_case in context['groups']:
                    if 'data' in test_case:
                        print(test_case['data']['statements'].strip())
                    else:
                        print(test_case['description']['description'])
                    if 'tests' in test_case:
                        for test in test_case['tests']:
                            print("Expected: \t" + test['expected'])
                            print("Actual: \t" + test['generated'])
    else:
        correct_tabs.append(tab['description'])
'''


def submission_tabs_handler(submission_data: dict) -> str:
    """
    Handle all tabs, group together those that were accepted and delegate the failed tabs
    :param submission_data: dictionary with the results of a submission
    :return: formatted string with
    """
    failed_tabs = []
    correct_tabs = []
    for tab in submission_data['groups']:
        if tab['badgeCount'] > 0:
            failed_tabs.append(tab)
        else:
            correct_tabs.append(tab)

    result = ""
    for failed_tab in failed_tabs:
        result += failed_tab_handler(failed_tab)

    if len(correct_tabs) > 0:
        result += "[bold bright_green]Correct tabs:[/] "
        result += ', '.join([tab['description'] for tab in correct_tabs])
        result += "\n"

    return result


def failed_tab_handler(tab: dict) -> str:
    result = f"[bold bright_red]{tab['description']}:[/]\n"

    return result


def submission_code_annotations(submission_data: dict) -> str:
    """
    Get code annotations out of the submission data
    :param submission_data: dictionary with the results of a submission
    :return: formatted string with code annotations
    """
    # Example annotation
    # {
    #   "column":0,
    #   "externalUrl":"https://pylint.pycqa.org/en/latest/messages/convention/trailing-newlines.html",
    #   "row":46,
    #   "text":"Trailing newlines",
    #   "type":"info"
    # }
    result = ""
    if 'annotations' in submission_data and len(submission_data['annotations']) > 0:
        for annotation in submission_data['annotations']:
            result += f"- Row {annotation['row']}: {annotation['text']}"
    return result

