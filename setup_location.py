import cv2
import json

idx = 0
json_file = None
image = None

def mouse_callback(event, x, y, flags, param):
    global idx, json_file, image
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击事件
        json_file[str(idx)] = (x, y)
        cv2.circle(image, [x, y], 5, (0, 0, 255), -1)
        cv2.imshow("location_setup", image)
        print(f"location idx {idx}: ({x}, {y})")
        idx += 1

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def run(img):
    global json_file, image
    image = img.copy()

    cv2.namedWindow("location_setup")
    # cv2.imshow("location_setup", img)
    cv2.setMouseCallback("location_setup", mouse_callback)

    json_file_path = "location.json"
    json_file = {}

    print("Click on the points to add locations. Press 'q' to finish.")

    while True:
        cv2.imshow("location_setup", image)
        key = cv2.waitKey(100)
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()
    with open(json_file_path, 'w') as file:
        json.dump(json_file, file)

    print("localtion setup finished, config file saved as 'location.json'")

if __name__ == "__main__":
    img = cv2.imread("Library/library.jpg")
    run(img)