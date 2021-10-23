import pandas as pd

from config.settings.base import APPS_DIR

"""Code by Alexander Lakiza"""

MAX_THRESHOLD = 0.5
MIN_THRESHOLD = 0.6


def read_csvs():
    app_dir = APPS_DIR / "whouse_problems"
    agrs = pd.read_csv(app_dir / 'agregates.csv')
    links = pd.read_csv(app_dir / 'agregates_warehouses.csv')
    whouses = pd.read_csv(app_dir / 'warehouses.csv')
    return agrs, links, whouses


def get_problem(agrs, links, whouses, agregate, date=None):
    """
    Функция выдаёт информацию о том, какие проблемы есть со складами для указанного агрегата
    :param agrs: Таблица с агрегатами
    :param links: Таблица с агрегатами и их складами
    :param whouses: Таблица со складами
    :param agregate: Имя агрегата
    :param date: Дата (необязательный аргумент)
    :return: Словарь с подробной информацией по агрегату (и указанной дате)
    """
    response = {'Имя агрегата': agregate,
                'Дата': date,
                'Тип проблемы': None,
                'Описание проблем(ы)': None}

    if agregate not in list(agrs['Name'].unique()):
        response['Тип проблемы'] = 'Данного агрегата в таблице не существует.'
        response['Описание проблем(ы)'] = '-'
        return response

    # Есть ли данная дата для данного агрегата
    if date and (len(agrs[(agrs['Name'] == agregate) & (agrs['dStart'] == date)]) == 0):
        response['Тип проблемы'] = 'Данной даты для данного агрегата нет.'
        response['Описание проблем(ы)'] = '-'
        return response

    if date:  # Если у нас есть дата
        if all(list(agrs[(agrs['Name'] == agregate) & (agrs['dStart'] == date)]['OccupiedPercentage'] == 100)):
            # Если для данной даты у всех OccupiedPercentage = 100, то проблем нет
            response['Тип проблемы'] = 'Проблем для данного агрегата на выбранную дату нет.'
            response['Описание проблем(ы)'] = '-'
            return response
        else:
            pass
    else:  # Если даты нет
        if all(list(agrs[agrs['Name'] == agregate]['OccupiedPercentage'] == 100)):
            # Если у всех OccupiedPercentage = 100, то проблем нет
            response['Тип проблемы'] = 'Проблем для данного агрегата на все даты нет.'
            response['Описание проблем(ы)'] = '-'
            response['Дата'] = 'Дата не указана.'
            return response
        else:
            pass

    agr_id = agrs[agrs['Name'] == agregate]['Id'].unique()[0]  # Айди агрегата
    # Агрегаты, для которых у нас есть склады
    key_agr_ids = list(links['Идентификатор'].unique())

    if date:
        counter = list(agrs[(agrs['Name'] == agregate) &
                            (agrs['dStart'] == date)]['OccupiedPercentage'] == 100).count(False)
    else:
        counter = list(agrs[agrs['Name'] == agregate]
                       ['OccupiedPercentage'] == 100).count(False)

    if agr_id not in key_agr_ids:  # Если для данного агрегата нет информации по складам
        response['Тип проблемы'] = f'Для агрегата {agregate} есть {counter} проблем.'
        response[
            'Описание проблем(ы)'] = f'Для данного агрегата нет возможности выяснить ' \
                                     f'проблему, так как нет информации по складам.'
        response['Дата'] = 'Дата не указана.'
        return response

    inputs = list(links[links['Идентификатор'] == agr_id]['InputSP'].dropna())
    outputs = list(links[links['Идентификатор'] == agr_id]
                   ['OutputSP'].dropna())

    if inputs:
        input_whouses = inputs[0].split(';')
    else:
        input_whouses = []

    if outputs:
        output_whouses = outputs[0].split(';')  # аутпут склады
    else:
        output_whouses = []

    checking_inputs = False
    checking_outputs = False
    inputs_counter = 0
    outputs_counter = 0
    probs_input = []
    probs_output = []
    percent = 0

    # Проверка проблем с входными складами
    if date:
        for sklad in input_whouses:
            current_sklad = whouses[(whouses['Идентификатор'] == sklad) & (
                whouses['Плановая дата'] == date)]
            curr_cap = list(current_sklad['Уровень запасов'])[0]
            max_cap = list(current_sklad['Максимальное количество запасов'])[0]
            sklad_name = list(current_sklad['Имя'])[0]
            try:
                percent = round(100 * curr_cap / max_cap, 2)
            except ZeroDivisionError:
                pass
            if curr_cap < MAX_THRESHOLD * max_cap:
                checking_inputs = True
                inputs_counter += 1
                probs_input.append(
                    f'Уровень запасов во входном складе "{sklad_name}" '
                    f'меньше максимального и составляет {percent}% от максимально возможного объёма.')
            else:
                pass
    else:
        for sklad in input_whouses:
            current_sklad = whouses[whouses['Идентификатор'] == sklad]
            if len(current_sklad) == 1:
                curr_cap = list(current_sklad['Уровень запасов'])[0]
                max_cap = list(
                    current_sklad['Максимальное количество запасов'])[0]
                sklad_name = list(current_sklad['Имя'])[0]
                try:
                    percent = round(100 * curr_cap / max_cap, 2)
                except ZeroDivisionError:
                    pass
                if curr_cap < MAX_THRESHOLD * max_cap:
                    checking_inputs = True
                    inputs_counter += 1
                    probs_input.append(
                        f'Уровень запасов во входном складе "{sklad_name}" '
                        f'меньше максимального и составляет {percent}% от максимально возможного объёма.')
                else:
                    pass

    # проверка проблем с выходными складами
    if date:
        for sklad in output_whouses:
            current_sklad = whouses[(whouses['Идентификатор'] == sklad) & (
                whouses['Плановая дата'] == date)]
            curr_cap = list(current_sklad['Уровень запасов'])[0]
            max_cap = list(current_sklad['Максимальное количество запасов'])[0]
            sklad_name = list(current_sklad['Имя'])[0]
            try:
                percent = round(100 * curr_cap / max_cap, 2)
            except ZeroDivisionError:
                pass
            if curr_cap > MIN_THRESHOLD * max_cap:
                checking_outputs = True
                outputs_counter += 1
                probs_output.append(
                    f'Уровень запасов в выходном складе "{sklad_name}" '
                    f'составляет {percent}% от максимально возможного объёма. '
                    f'В выходном складе может закончиться место.')
            else:
                pass
    else:
        for sklad in output_whouses:
            current_sklad = whouses[whouses['Идентификатор'] == sklad]
            curr_cap = list(current_sklad['Уровень запасов'])[0]
            max_cap = list(current_sklad['Максимальное количество запасов'])[0]
            sklad_name = list(current_sklad['Имя'])[0]
            try:
                percent = round(100 * curr_cap / max_cap, 2)
            except ZeroDivisionError:
                pass
            if curr_cap > MIN_THRESHOLD * max_cap:
                checking_outputs = True
                outputs_counter += 1
                probs_output.append(
                    f'Уровень запасов в выходном складе "{sklad_name}" '
                    f'составляет {percent}% от максимально возможного объёма. '
                    f'В выходном складе может закончиться место.')
            else:
                pass

    if checking_inputs and checking_outputs:
        response[
            'Тип проблемы'] = f'Есть проблемы с входными и выходными складами.'
        response['Описание проблем(ы)'] = f'Обнаружено {inputs_counter} проблем ' \
                                          f'с входными складами и {outputs_counter} проблем с выходными складами.'
        response['Проблемы с входными складами'] = probs_input
        response['Проблемы с выходными складами'] = probs_output
    elif checking_inputs and (checking_outputs is False):
        response['Тип проблемы'] = f'Есть проблемы с входными складами.'
        response['Описание проблем(ы)'] = f'Обнаружено {inputs_counter} проблем с входными складами.'
        response['Проблемы с входными кладами'] = probs_input
    elif checking_outputs and (checking_inputs is False):
        response['Тип проблемы'] = f'Есть проблемы с выходными складами.'
        response['Описание проблем(ы)'] = f'Обнаружено {outputs_counter} проблем с выходными складами.'
        response['Проблемы с выходными складами'] = probs_output
    else:
        response['Тип проблемы'] = f'Проблем со складами не обнаружено. Возможно, причина в другом.'
        response['Описание проблем(ы)'] = '-'

    if not date:
        response['Дата'] = 'Дата не указана.'
    return response


def find_problems(date: str = '2021-10-07'):
    agrs, links, whouses = read_csvs()
    names = ['Конвертерный цех 1 УНРС 2,3,4,6', 'Конвертеры КЦ-1',
             'Конвертерный цех 2 УНРС 5,6,7,8,9', 'Конвертеры КЦ-2', 'АЗП ЦТС',
             'Травильный комплекс ЦТС', 'АНГЦ ЦХПП', 'АНО ЦХПП', 'НТА ЦХПП', 'Стан 2030 ЦХПП',
             'АНГЦ 2,4 ЦДС', 'НТА ЦДС', 'Реверсивный стан ЦДС', 'Стан 1400 ЦДС']

    res = []

    for name in names:
        res.append(get_problem(agrs, links, whouses, name, date))

    return res
