import json


def update_file(places: dict) -> None:
    with open('bot\pointsInfo.json', 'w', encoding='utf-8') as file:
        json.dump(places, file, ensure_ascii=False, indent=2)
    return None
