def submission_data_handler(submission_data: dict) -> str:
    result = ""
    result += submission_tabs_handler(submission_data)
    result += submission_code_annotations(submission_data)
    return result


def submission_tabs_handler(submission_data: dict) -> str:
    """
    Handle all tabs, group together those that were accepted and delegate the failed tabs
    :param submission_data: dictionary with the results of a submission
    :return: formatted string with info per tab
    """
    failed_tabs = []
    correct_tabs = []
    for tab in submission_data['groups']:
        if tab['badgeCount'] > 0:
            failed_tabs.append(tab)
        else:
            correct_tabs.append(tab)

    result = "\n[bold bright_red]Wrong tabs[/]:"
    for failed_tab in failed_tabs:
        result += failed_tab_handler(failed_tab)

    if len(correct_tabs) > 0:
        result += "\n\n[bold bright_green]Correct tabs:[/] "
        result += ', '.join([tab['description'] for tab in correct_tabs])

    return result


def failed_tab_handler(tab: dict) -> str:
    """
    Handle failed tabs by delegating the first 3 failed contexts
    :param tab: dictionary with a failed tab
    :return: formatted string with failed tab things
    """
    result = f"\n[bold bright_red] \u00B7 [/]{tab['description']} ({tab['badgeCount']}):"
    contexts = tab['groups']
    index = 0
    amount_failed = 0

    # while index < len(contexts) and amount_failed < 3:
    #     context = contexts[index]
    #     if context['accepted']:
    #         index += 1
    #         continue
    #     result += failed_context_handler(context)
    #     amount_failed += 1
    #     index += 1
    return result


def failed_context_handler(context: dict) -> str:
    result = ""
    if 'data' in context:
        result += f"\n\t- {context['data']['statements'].strip()}:"
    elif 'description' in context:
        result += f"\n\t- {context['description']['description']}:"

    test_cases = context['groups']
    index = 0
    amount_failed = 0

    while index < len(test_cases) and amount_failed < 3:
        test_case = test_cases[index]

        if 'tests' in test_case:
            result += failed_tests_handler(test_case)
            pass
        else:
            result += f"\n\t\t- {test_case['description']['description']}"

        if not test_case['accepted']:
            amount_failed += 1
        index += 1

    return result


def failed_tests_handler(test_case: dict) -> str:
    result = ""
    if 'data' in test_case:
        result += f"\n\t- {test_case['data']['statements'].strip()}:"
    elif 'description' in test_case:
        result += f"\n\t- {test_case['description']['description']}:"

    tests = test_case['tests']
    if all(test['accepted'] for test in tests):
        result = result.rstrip('\n') + " [bright_green]:heavy_check_mark:[/]"
        return result

    index = 0
    amount_failed = 0

    while index < len(tests) and amount_failed < 3:
        test = tests[index]

        result += f"\n\t\tExpected:\t{test['expected']}"
        result += f"\n\t\tActual:  \t{test['generated']}"
        index += 1
        if not test['accepted']:
            amount_failed += 1

    return result


def submission_code_annotations(submission_data: dict) -> str:
    """
    Get code annotations out of the submission data
    :param submission_data: dictionary with the results of a submission
    :return: formatted string with code annotations
    """
    result = ""
    if 'annotations' in submission_data and len(submission_data['annotations']) > 0:
        result = "\n\n[bold]Code annotations:[/]"
        for annotation in submission_data['annotations']:
            result += f"\n- Row {annotation['row']}: {annotation['text']}"
    return result


if __name__ == '__main__':
    import json
    import pretty_console

    with open('/home/bram/tijdelijk4.json', 'r') as test_file:
        test_data: dict = json.load(test_file)

    pretty_console.console.print(submission_data_handler(test_data))
