# =========================
# trajectory.py
# =========================

import cv2


def draw_player_trajectories(
    video_frames,
    player_detections
):

    trajectory_history = {}

    for frame_num, frame in enumerate(video_frames):

        players = player_detections[frame_num]

        for player_id, bbox in players.items():

            x1, y1, x2, y2 = bbox

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            if player_id not in trajectory_history:

                trajectory_history[player_id] = []

            trajectory_history[player_id].append(
                (center_x, center_y)
            )

            points = trajectory_history[player_id]

            for i in range(1, len(points)):

                cv2.line(
                    frame,
                    points[i - 1],
                    points[i],
                    (0, 255, 255),
                    2
                )

    return video_frames