import cv2
import numpy as np
import random


class Augmenter:
    """
    A collection of dataset augmentation methods including transformations, 
    blurring, resizing, and brightness adjustments. 

    NOTE: This class is used to transform data necessary for training TechTrack's models.
          Imagine that the output of `self.transform()` is fed directly to train the model.
    
    The following transformations are included:
    - Horizontal flipping: i.e., def horizontal_flip(**kwargs)
    - Gaussian blurring: i.e., def gaussian_blur_image(**kwargs)
    - Resizing: i.e., def resize(**kwargs)
    - Brightness and contrast adjustments: i.e., def change_brightness(**kwargs)
        - HINT: you may use cv2.addWeighted()

    NOTE: These methods uses **kwargs to accept arbitrary keyword arguments,
    but explicit parameter definitions improve clarity and usability.
    - "**kwargs" reference: https://www.geeksforgeeks.org/args-kwargs-python/

    Finally, Provide a demonstration and visualizations of these methods in `notebooks/augmentation.ipynb`.
    You will define your own keywords for "**kwargs".
    """
    
    @staticmethod
    def horizontal_flip(frame):
        """
        Horizontally flip the image.
        """
        return cv2.flip(frame, 1)

    @staticmethod
    def gaussian_blur(frame, ksize, sigmax):
        """
        Apply Gaussian blur to the image.
        """
        return cv2.GaussianBlur(frame, ksize, sigmax)

    @staticmethod
    def resize(frame, w, h):
        """
        Resize the image.
        """
        return cv2.resize(frame, (w, h))

    @staticmethod
    def change_brightness(frame, alpha, beta):
        """
        Adjust brightness and contrast of the image.
        """
        return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    @staticmethod
    def transform(**kwargs):
        """
        Apply random augmentations from the available methods.
        
        Internal Process:
        1. A list of available augmentation functions is created.
        2. The list is shuffled to introduce randomness.
        3. A random number of augmentations is selected.
        4. The selected augmentations are applied sequentially to the image.
        
        :param image: Input image (numpy array)
        :param kwargs: Additional parameters for transformations (if any)
        :return: Augmented image
        """
        pass
        # augmentations = [0,1,2,3]
        # random.shuffle(augmentations)
        # n = random.randint(0,3)
        # for i in range(n):
        #     aug = augmentations[i]
        #     if aug == 0:
        #         new_image = horizontal_flip(kwargs)
            # elif aug == 1:

            # elif aug == 2:

            # elif aug == 3:


        
        

"""
EXAMPLE RUNNER:

# Create an instance of Augmenter
augmenter = Augmenter()

kwargs = {"image": your_image, # Numpy type
            ... # Add more...
        }

# Apply random transformations
augmented_image = augmenter.transform(**kwargs)

# Display the original and transformed images
cv2.imshow("Original Image", image)
cv2.imshow("Augmented Image", augmented_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

# Create an instance of Augmenter
# augmenter = Augmenter()


# image = '/Users/seandickson/JohnsHopkinsScripts/CreatingAIEnabledSystems/techtrack-Sean090900/techtrack/storage/detections/frame_120.jpg'
# kwargs = {"image": image}

# # Apply random transformations
# augmented_image = augmenter.transform(**kwargs)

# # Display the original and transformed images
# cv2.imshow("Original Image", image)
# cv2.imshow("Augmented Image", augmented_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()