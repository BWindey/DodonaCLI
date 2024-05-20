def submission_data_handler(submission_data: dict, settings: dict) -> str:
    result = ""
    result += submission_tabs_handler(submission_data, settings)
    result += submission_code_annotations(submission_data)
    return result


def submission_tabs_handler(submission_data: dict, settings: dict) -> str:
    """
    Handle all tabs, group together those that were accepted and delegate the failed tabs
    :param submission_data: dictionary with the results of a submission
    :param settings: dictionary with settings
    :return: formatted string with info per tab
    """
    failed_tabs = []
    correct_tabs = []
    for tab in submission_data['groups']:
        if tab['badgeCount'] > 0:
            failed_tabs.append(tab)
        else:
            correct_tabs.append(tab)

    if settings['amount_feedback_tab'] == -1:
        amount_failed_display = len(failed_tabs)
    else:
        amount_failed_display = min(settings['amount_feedback_tab'], len(failed_tabs))

    result = "[bold bright_red]Wrong tabs[/]:"
    result += ''.join(failed_tab_handler(failed_tab, settings) for failed_tab in failed_tabs[:amount_failed_display])

    if len(correct_tabs) > 0:
        result += "\n\n[bold bright_green]Correct tabs:[/] "
        result += ', '.join([tab['description'] for tab in correct_tabs])

    if amount_failed_display < len(failed_tabs):
        result += "\n[bold bright_red]Other failed tabs:[/] "
        result += ', '.join([tab['description'] for tab in failed_tabs[amount_failed_display:]])

    return result


def failed_tab_handler(tab: dict, settings: dict) -> str:
    """
    Handle failed tabs by delegating the first n failed contexts
    :param tab: dictionary with a failed tab
    :param settings: dictionary with settings
    :return: formatted string with failed tab things
    """
    result = f"\n[bold bright_red] \u00B7 [/][u]{str(tab['description']).capitalize()} ({tab['badgeCount']}):[/]"
    contexts = tab['groups']
    index = 0
    amount_failed = 0

    while index < len(contexts) and amount_failed < settings['amount_feedback_context']:
        context = contexts[index]
        if context['accepted']:
            index += 1
            continue
        result += failed_context_handler(context, settings)
        amount_failed += 1
        index += 1
    return result


def failed_context_handler(context: dict, settings: dict) -> str:
    """
    Handle failed context by delegating the first n failed contexts
    :param context: dictionary with a failed context
    :param settings: dictionary with settings
    :return: formatted string with failed tab things
    """
    result = ""

    test_cases = context['groups']
    index = 0
    amount_failed = 0

    context_content = []

    while index < len(test_cases) and amount_failed < settings['amount_feedback_testcase']:
        test_case = test_cases[index]

        if 'tests' in test_case:
            context_content.extend(failed_tests_handler(test_case, settings))
        else:
            if test_case['accepted']:
                emoji = '[bright_green]:heavy_check_mark:[/] '
            else:
                emoji = "[bright_red]:heavy_multiplication_x:[/] "
            context_content.append(emoji + test_case['description']['description'].rstrip())

        if not test_case['accepted']:
            amount_failed += 1
        index += 1

    if len(context_content) > 1:
        result += f"\n   \u256D {context_content[0]}" + (len(context_content[1:-1]) > 0) * "\n   \u2502 "
        result += "\n   \u2502 ".join(cc for cc in context_content[1:-1])
        result += f"\n   \u2570 {context_content[-1]}\n"
    else:
        result += "\n   - " + context_content[0] + "\n"

    return result


def failed_tests_handler(test_case: dict, settings: dict) -> list:
    """
    Handle failed test_case by displaying all tests
    :param test_case: dictionary with a failed context
    :param settings: dictionary with settings
    :return: formatted string with failed tab things
    """
    result = []
    if 'data' in test_case:
        result.append(test_case['data']['statements'].rstrip())
    elif 'description' in test_case:
        result.append(test_case['description']['description'].rstrip())

    tests = test_case['tests']
    if all(test['accepted'] for test in tests):
        result[-1] = "[bright_green]:heavy_check_mark:[/] " + result[-1]
        return result
    else:
        result[-1] = "[bright_red]:heavy_multiplication_x:[/] " + result[-1]

    index = 0
    amount_failed = 0

    while index < len(tests) and amount_failed < settings['amount_feedback_test']:
        test = tests[index]
        if not test['accepted']:
            result.append("\t    Expected:\t" + test['expected'].rstrip())
            result.append("\t    Actual:  \t" + test['generated'].rstrip())
        amount_failed += 1
        index += 1

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
