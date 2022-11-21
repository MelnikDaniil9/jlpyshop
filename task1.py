from pprint import pprint
import random
import math


TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {"offset": 0, "score": {"home": 0, "away": 0}}


def generate_stamp(previous_value):
    score_changed = (
        random.random() > 1 - PROBABILITY_SCORE_CHANGED
    )  # 0.99999 > 0.9999 is True
    home_score_change = (
        1 if score_changed and random.random() > 1 - PROBABILITY_HOME_SCORE else 0
    )
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change,
        },
    }


def generate_game():
    stamps = [
        INITIAL_STAMP,
    ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


game_stamps = generate_game()

pprint(game_stamps)


def get_score(game_stamps, offset):
    # Скорость алгоритма в худшем случае - log2n
    low = 0
    high = len(game_stamps) - 1
    mid = (low + high) // 2
    if game_stamps[0]["offset"] <= offset <= game_stamps[-1]["offset"]:
        while offset != game_stamps[mid]["offset"] and low <= high:
            if offset > game_stamps[mid]["offset"]:
                low = mid + 1
            else:
                high = mid - 1
            mid = (low + high) // 2
        if low > high:
            return (
                game_stamps[low - 1]["score"]["home"],
                game_stamps[low - 1]["score"]["away"],
            )
        return game_stamps[mid]["score"]["home"], game_stamps[mid]["score"]["away"]
    raise "Значение offset слишком велико!"


# Один из вариантов решения - использовать алгоритм бинарного поиска bisect, но как я понимаю,
# для проверки навыков важна сама реализация алгоритма, поэтому не стал дописывать код ниже.
#
# def get_score(game_stamps, offset):
#     index = bisect_left(game_stamps, offset, key=lambda elem: elem["offset"])
#     if index > 0:
#         index = index - 1
#     return game_stamps[index]["score"]["home"], game_stamps[index]["score"]["away"]
