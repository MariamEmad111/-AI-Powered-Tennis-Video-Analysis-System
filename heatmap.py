import numpy as np
import cv2


def generate_heatmap(player_detections,
                     mini_court,
                     frame_width,
                     frame_height,
                     save_path="output_videos/heatmap.jpg"):

    # Court size
    court_width = mini_court.drawing_rectangle_width
    court_height = mini_court.drawing_rectangle_height

    # Empty heatmap
    heatmap = np.zeros((court_height, court_width), dtype=np.float32)

    # Fill heatmap from player positions
    for frame in player_detections:

        for player_id, bbox in frame.items():

            x1, y1, x2, y2 = bbox

            # center of player
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # map to mini court
            mini_x = int((center_x / frame_width) * court_width)
            mini_y = int((center_y / frame_height) * court_height)

            # clamp
            mini_x = max(0, min(mini_x, court_width - 1))
            mini_y = max(0, min(mini_y, court_height - 1))

            # draw intensity point
            cv2.circle(heatmap, (mini_x, mini_y), 12, 1, -1)

    # blur for smooth heatmap
    heatmap = cv2.GaussianBlur(heatmap, (51, 51), 0)

    # normalize
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = heatmap.astype(np.uint8)

    # color map
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # court border
    cv2.rectangle(
        heatmap_color,
        (0, 0),
        (court_width - 1, court_height - 1),
        (255, 255, 255),
        2
    )

    # center line
    cv2.line(
        heatmap_color,
        (0, court_height // 2),
        (court_width, court_height // 2),
        (255, 255, 255),
        2
    )

    # upscale for display
    final_heatmap = cv2.resize(
        heatmap_color,
        (court_width * 4, court_height * 4)
    )

    # save image
    cv2.imwrite(save_path, final_heatmap)

    print(f"Heatmap saved to: {save_path}")

    return final_heatmap