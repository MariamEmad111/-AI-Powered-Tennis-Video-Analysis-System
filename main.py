# =========================
# main.py (EXE READY)
# =========================

import os
import sys
import cv2
import pandas as pd
from copy import deepcopy

from utils import (
    read_video,
    save_video,
    measure_distance,
    draw_player_stats,
    convert_pixel_distance_to_meters
)

import constants

from trackers import PlayerTracker, BallTracker
from court_line_detector import CourtLineDetector
from mini_court import MiniCourt
from trajectory import draw_player_trajectories

from analysis import (
    calculate_court_coverage,
    classify_player_style,
    total_distance_covered
)

from heatmap import generate_heatmap


def resource_path(path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, path)


def main(input_video_path):

    os.makedirs("output_videos", exist_ok=True)

    video_frames = read_video(input_video_path)

    player_tracker = PlayerTracker(
        model_path=resource_path("models/yolov8n.pt")
    )

    ball_tracker = BallTracker(
        model_path=resource_path("models/yolo5_last.pt")
    )

    player_detections = player_tracker.detect_frames(
        video_frames,
        read_from_stub=True,
        stub_path=resource_path("tracker_stubs/player_detections.pkl")
    )

    ball_detections = ball_tracker.detect_frames(
        video_frames,
        read_from_stub=True,
        stub_path=resource_path("tracker_stubs/ball_detections.pkl")
    )

    ball_detections = ball_tracker.interpolate_ball_positions(ball_detections)

    court_line_detector = CourtLineDetector(
        resource_path("models/keypoints_model.pth")
    )

    court_keypoints = court_line_detector.predict(video_frames[0])

    player_detections = player_tracker.choose_and_filter_players(
        court_keypoints,
        player_detections
    )

    mini_court = MiniCourt(video_frames[0])

    ball_shot_frames = ball_tracker.get_ball_shot_frames(ball_detections)

    player_mini, ball_mini = mini_court.convert_bounding_boxes_to_mini_court_coordinates(
        player_detections,
        ball_detections,
        court_keypoints
    )

    h, w = video_frames[0].shape[:2]

    generate_heatmap(
        player_detections,
        mini_court,
        w,
        h
    )

    stats = [{
        'frame_num': 0,
        'player_1_number_of_shots': 0,
        'player_1_total_shot_speed': 0,
        'player_1_last_shot_speed': 0,
        'player_1_total_player_speed': 0,
        'player_1_last_player_speed': 0,
        'player_2_number_of_shots': 0,
        'player_2_total_shot_speed': 0,
        'player_2_last_shot_speed': 0,
        'player_2_total_player_speed': 0,
        'player_2_last_player_speed': 0,
    }]

    fps = 24

    for i in range(len(ball_shot_frames) - 1):

        start = ball_shot_frames[i]
        end = ball_shot_frames[i + 1]

        time = (end - start) / fps
        if time <= 0:
            continue

        ball_dist = measure_distance(
            ball_mini[start][1],
            ball_mini[end][1]
        )

        ball_meters = convert_pixel_distance_to_meters(
            ball_dist,
            constants.DOUBLE_LINE_WIDTH,
            mini_court.get_width_of_mini_court()
        )

        ball_speed = (ball_meters / time) * 3.6

        players = player_mini[start]

        shooter = min(
            players.keys(),
            key=lambda pid: measure_distance(
                players[pid],
                ball_mini[start][1]
            )
        )

        opponent = 1 if shooter == 2 else 2

        opp_dist = measure_distance(
            player_mini[start][opponent],
            player_mini[end][opponent]
        )

        opp_meters = convert_pixel_distance_to_meters(
            opp_dist,
            constants.DOUBLE_LINE_WIDTH,
            mini_court.get_width_of_mini_court()
        )

        opp_speed = (opp_meters / time) * 3.6

        current = deepcopy(stats[-1])
        current['frame_num'] = start

        current[f'player_{shooter}_number_of_shots'] += 1
        current[f'player_{shooter}_total_shot_speed'] += ball_speed
        current[f'player_{shooter}_last_shot_speed'] = ball_speed

        current[f'player_{opponent}_total_player_speed'] += opp_speed
        current[f'player_{opponent}_last_player_speed'] = opp_speed

        stats.append(current)

    df = pd.DataFrame(stats)

    frames_df = pd.DataFrame({'frame_num': range(len(video_frames))})

    df = frames_df.merge(df, on='frame_num', how='left').ffill().fillna(0)

    # =========================================================
    # SHOT SPEED AVERAGE
    # =========================================================
    df['player_1_average_shot_speed'] = df['player_1_total_shot_speed'] / df['player_1_number_of_shots'].replace(0, 1)
    df['player_2_average_shot_speed'] = df['player_2_total_shot_speed'] / df['player_2_number_of_shots'].replace(0, 1)

    # =========================================================
    # PLAYER SPEED AVERAGE (FIX ADDED)
    # =========================================================
    df['player_1_average_player_speed'] = df['player_1_total_player_speed'] / df['player_1_number_of_shots'].replace(0, 1)
    df['player_2_average_player_speed'] = df['player_2_total_player_speed'] / df['player_2_number_of_shots'].replace(0, 1)

    coverage = calculate_court_coverage(player_mini)
    distance = total_distance_covered(player_mini)

    p1_speed = df['player_1_average_shot_speed'].iloc[-1]
    p2_speed = df['player_2_average_shot_speed'].iloc[-1]

    p1_style = classify_player_style(p1_speed, coverage[1])
    p2_style = classify_player_style(p2_speed, coverage[2])

    report = f"""
========== MATCH ANALYSIS ==========

PLAYER 1
Speed: {p1_speed:.2f}
Coverage: {coverage[1]}
Distance: {distance[1]:.2f}
Style: {p1_style}

PLAYER 2
Speed: {p2_speed:.2f}
Coverage: {coverage[2]}
Distance: {distance[2]:.2f}
Style: {p2_style}
"""

    with open("output_videos/final_report.txt", "w") as f:
        f.write(report)

    frames = player_tracker.draw_bboxes(video_frames, player_detections)
    frames = ball_tracker.draw_bboxes(frames, ball_detections)
    frames = draw_player_trajectories(frames, player_detections)
    frames = court_line_detector.draw_keypoints_on_video(frames, court_keypoints)
    frames = mini_court.draw_mini_court(frames)

    frames = mini_court.draw_points_on_mini_court(frames, player_mini)
    frames = mini_court.draw_points_on_mini_court(frames, ball_mini, color=(0, 255, 255))

    df = df.iloc[:len(frames)]

    frames = draw_player_stats(frames, df)

    save_video(frames, "output_videos/output_video.avi")


if __name__ == "__main__":
    main(resource_path("input_videos/input_video.mp4"))