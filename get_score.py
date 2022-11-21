def get_score(game_stamps, offset):
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
    return "значение offset слишком велико!"
