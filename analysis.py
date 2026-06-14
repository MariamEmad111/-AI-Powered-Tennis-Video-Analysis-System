# =========================
# analysis.py
# =========================

from utils import measure_distance


def calculate_court_coverage(
    player_mini_court_detections
):

    coverage = {}

    for player_id in [1, 2]:

        positions = []

        for frame in player_mini_court_detections:

            if player_id in frame:

                positions.append(
                    frame[player_id]
                )

        if len(positions) == 0:

            coverage[player_id] = 0
            continue

        xs = [p[0] for p in positions]
        ys = [p[1] for p in positions]

        width = max(xs) - min(xs)
        height = max(ys) - min(ys)

        area = width * height

        coverage[player_id] = round(area, 2)

    return coverage


def classify_player_style(
    avg_shot_speed,
    coverage
):

    if avg_shot_speed > 80 and coverage < 15000:

        return "Aggressive"

    elif coverage > 20000:

        return "Defensive"

    else:

        return "Balanced"


def total_distance_covered(
    player_mini_court_detections
):

    distances = {
        1: 0,
        2: 0
    }

    for player_id in [1, 2]:

        previous_position = None

        for frame in player_mini_court_detections:

            if player_id not in frame:
                continue

            current_position = frame[player_id]

            if previous_position is not None:

                distances[player_id] += (
                    measure_distance(
                        previous_position,
                        current_position
                    )
                )

            previous_position = current_position

    return distances