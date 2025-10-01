import cv2
import numpy as np
import os

def extract_panels(image_path, output_dir='demo/extracted_panels'):
    """
    Extracts panels from a manga page.

    Args:
        image_path (str): The path to the manga page image.
        output_dir (str): The directory to save the extracted panels.

    Returns:
        list: A list of filenames for the extracted panels.
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image at {image_path}")
        return []

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert and threshold
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio to find panels
    panels = []
    image_area = img.shape[0] * img.shape[1]
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Filter out very small or very large contours
        if w > 50 and h > 50 and w * h > image_area * 0.01 and w * h < image_area * 0.9:
            panels.append((x, y, w, h))

    # Remove overlapping boxes (keep the larger one)
    panels = non_max_suppression(np.array(panels))

    # Sort panels by reading order (top-to-bottom, right-to-left)
    panels = sorted(panels, key=lambda p: (p[1], -p[0]))

    # Crop and save panels
    panel_files = []
    for i, (x, y, w, h) in enumerate(panels):
        panel_img = img[y:y+h, x:x+w]
        panel_filename = os.path.join(output_dir, f"panel_{i+1}.png")
        cv2.imwrite(panel_filename, panel_img)
        panel_files.append(panel_filename)
        print(f"Saved panel to {panel_filename}")

    return panel_files

def non_max_suppression(boxes, overlapThresh=0.3):
    """
    Performs non-maximum suppression to remove overlapping bounding boxes.
    """
    if len(boxes) == 0:
        return []

    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    pick = []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 0] + boxes[:, 2]
    y2 = boxes[:, 1] + boxes[:, 3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]

        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")