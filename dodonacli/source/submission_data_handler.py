def submission_data_handler(submission_data: dict) -> str:
    result = ""
    result += submission_tabs_handler(submission_data)
    result += "\n"
    result += submission_code_annotations(submission_data)
    return result


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
        result += '\n'

    if len(correct_tabs) > 0:
        result += "[bold bright_green]Correct tabs:[/] "
        result += ', '.join([tab['description'] for tab in correct_tabs])
        result += "\n"

    return result


def failed_tab_handler(tab: dict) -> str:
    result = f"[bold bright_red]Tab [/]{tab['description']!r}:\n"
    contexts = tab['groups']
    index = 0
    amount_failed = 0

    while index < len(contexts) and amount_failed < 3:
        context = contexts[index]
        if context['accepted']:
            index += 1
            continue
        result += failed_context_handler(context)
        amount_failed += 1
        index += 1
    return result


def failed_context_handler(context: dict) -> str:
    result = ""
    if 'data' in context:
        result += f"\t- {context['data']['statements'].strip()}:\n"
    else:
        result += f"\t- {context['description']['description']}:\n"

    test_cases = context['groups']
    index = 0
    amount_failed = 0

    while index < len(test_cases) and amount_failed < 3:
        test_case = test_cases[index]
        if test_case['accepted']:
            index += 1
            continue

        if 'tests' in test_case:
            result += failed_tests_handler(test_case)
            pass
        else:
            result += f"\t\t- {test_case['description']['description']}\n"

        amount_failed += 1
        index += 1

    return result


def failed_tests_handler(test_case: dict) -> str:
    result = ""

    tests = test_case['tests']
    index = 0
    amount_failed = 0

    while index < len(tests) and amount_failed < 3:
        test = tests[index]
        if test['accepted']:
            index += 1
            continue

        result += f"\t\t\tExpected:\t{test['expected']}\n"
        result += f"\t\t\tActual:  \t{test['generated']}\n"
        index += 1
        amount_failed += 1

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


if __name__ == '__main__':
    import json
    import pretty_console

    with open('/home/bram/tijdelijk.json', 'r') as test_file:
        test_data: dict = json.load(test_file)

    pretty_console.console.print(submission_data_handler(test_data))
