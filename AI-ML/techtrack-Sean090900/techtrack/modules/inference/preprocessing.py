import cv2
import numpy as np
from typing import Generator


class Preprocessing:
    """
    Handles video file reading and frame extraction for object detection inference.

    This class reads a video from a file and preprocesses frames before passing them 
    to an object detection module for inference.
    """

    def __init__(self, filename: str, drop_rate: int = 10) -> None:
        """
        Initializes the Preprocessing class.

        :param filename: Path to the video file.
        :param drop_rate: The interval at which frames are selected. For example, 
                          `drop_rate=10` means every 10th frame is retained.
                          
        :ivar self.filename: Stores the video file path.
        :ivar self.drop_rate: Defines how frequently frames are extracted from the video.
        """
        self.filename = filename
        self.drop_rate = drop_rate

    def capture_video(self) -> Generator[np.ndarray, None, None]:
        """
        Captures frames from a video file and yields every nth frame.

        :return: A generator yielding frames as NumPy arrays.

        **Functionality:**
        - Opens a video file using OpenCV.
        - Iterates through each frame.
        - Yields every `drop_rate`-th frame.
        - Releases the video resource when finished.

        **Usage Example:**
        ```python
        video_processor = Preprocessing("video.mp4", drop_rate=10)
        for frame in video_processor.capture_video():
            process_frame(frame)  # Custom processing function (...think Detector Methods!)
        ```

        **Reference:**
        - OpenCV VideoCapture Documentation: 
          https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
        """
        # TASK: Modify file to yield only every `drop_rate`-th frame.
        # HINT: When running in Docker avoid using:
        # -----------------------------
        # cv.imshow('frame', gray)
        # if cv.waitKey(1) == ord('q'):
        #     break
        # -----------------------------
        # The standard Docker Engine does not support graphic displays, 
        # unless configured to do so.

        cap = cv2.VideoCapture(self.filename)

        if not cap.isOpened():
            raise ValueError(f"Error: Unable to open video file '{self.filename}'.")
        
        frame_count = 0
        while cap.isOpened():
                
            # Read frame
            ret, frame = cap.read()

            # Check if video is still running
            if not ret:
                break

            # Yeild frame if drop_rate matches
            if frame_count % self.drop_rate == 0:
                yield frame

            frame_count += 1

        cap.release()




# video_path = 'techtrack-Sean090900/techtrack/storage/test_videos/worker-zone-detection.mp4'
# processer = Preprocessing(video_path, 100)
# captured_frames = list(processer.capture_video())


# import os
# import glob
# class DummyVideoCapture:
#     """
#     A dummy video capture class to simulate cv2.VideoCapture behavior.
    
#     If provided with a list of frames, it uses them directly. If provided with a string
#     and the string is a path to a directory, it loads all image files from that directory 
#     (sorted alphabetically) as frames.
#     """
#     def __init__(self, source, open_success=True):
#         self.index = 0
#         self.open_success = open_success

#         if isinstance(source, list):
#             self.frames = source
#         elif isinstance(source, str) and os.path.isdir(source):
#             files = sorted(glob.glob(os.path.join(source, "*")))
#             self.frames = []
#             for f in files:
#                 img = cv2.imread(f)
#                 if img is not None:
#                     self.frames.append(img)
#         else:
#             self.frames = []

#     def isOpened(self):
#         return self.open_success

#     def read(self):
#         if self.index < len(self.frames):
#             frame = self.frames[self.index]
#             self.index += 1
#             return True, frame
#         return False, None

#     def release(self):
#         pass

# dummy_frames = [np.full((100, 100, 3), fill_value=i, dtype=np.uint8) for i in range(15)]
# drop_rate = 3

# # mock_capture = DummyVideoCapture(dummy_frames)

# preprocessing = Preprocessing("", drop_rate=drop_rate)
# captured_frames = list(preprocessing.capture_video())

# expected_frames = [dummy_frames[i] for i in range(0, len(dummy_frames), drop_rate)]

# print(expected_frames)
# print(captured_frames)