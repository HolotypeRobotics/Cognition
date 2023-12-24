import os
import cv2

def validate_file(file_path):
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return False

    return True

def validate_image_file(file_path):
    if not validate_file(file_path):
        return False

    try:
        img = cv2.imread(file_path)
        if img is None:
            print(f"File is not a valid image: {file_path}")
            return False
    except Exception as e:
        print(f"Error occurred while validating image: {file_path}. Error: {str(e)}")
        return False

    return True

# Test
file_path = "/path/to/your/image/file.jpg"
if validate_image_file(file_path):
    print("The file is a valid image.")
else:
    print("The file is either missing or not a valid image.")