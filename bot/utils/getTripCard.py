import json


def get_trip_card(fromDirect, fromPoint, whereDirect, wherePoint, datetime, username, active=None, success=0) -> dict:
    with open('bot\pointsInfo.json', 'r', encoding='utf-8') as file:
        info = json.load(file)
    from_point = fromPoint.split('*')
    where_point = wherePoint.split('*')

    from_direct = info[str(fromDirect)]['name']
    from_point = info[str(fromDirect)][fromPoint[0]][int(from_point[1])]
    where_direct = info[str(whereDirect)]['name']
    where_point = info[str(whereDirect)][wherePoint[0]][int(where_point[1])]
    trip_success = 'неизвестно'
    status = 0
    if active == 1:
        status = 'активен'
    elif active == 0:
        status = 'остановлен'

    if success:
        if success == 1:
            trip_success = 'успешно'
        elif success == '2':
            trip_success = 'неуспешно'

    card = f'''<b>Пассажир</b>
когда: {datetime[0]} в {datetime[1]}
откуда: {from_direct}, {from_point}
куда: {where_direct}, {where_point}
связаться: @{username}
'''
    values = {
        'fromDirect': from_direct,
        'fromPoint': from_point,
        'whereDirect': where_direct,
        'wherePoint': where_point,
        'datetime': f'{datetime[0]} {datetime[1]}',
        'userName': username,
        'status': status,
        'success': trip_success
    }
    return {'card': card, 'values': values}
