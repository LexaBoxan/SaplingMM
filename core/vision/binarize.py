import cv2, numpy as np

def clean_binary(img_bgr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    bin_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 7)
    bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=1)
    return gray, bin_img