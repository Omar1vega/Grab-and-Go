import cv2


def takePicture():
    camera = cv2.VideoCapture(0)
    read, frame = camera.read()

    if read:
        filename = "pickup.png"
        cv2.imwrite(filename, frame)
        return filename
    return False


if __name__ == '__main__':
    picture = takePicture()
    if picture:
        print(picture)
    else:
        print("Failed to take picture")
