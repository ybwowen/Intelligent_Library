import json
import cv2
import asyncio
import threading

def load_location(img, json_file):
    
    for idx in range(len(json_file)):
        center = json_file[str(idx)]
        cv2.circle(img, center, 5, (0, 0, 255), -1)
    
    return img

    # cv2.namedWindow("book_setup")
    # cv2.imshow("book_setup", img)
    # cv2.waitKey(0)

def enter_books(json_file):
    books_list = {}
    for idx in range(len(json_file)):
        books_str = input(f"Enter the books for location {idx}, use ',' to seperate between books: ")
        books = books_str.split(',')
        for book in books:
            books_list[book] = idx

    with open('books.json', 'w') as file:
        json.dump(books_list, file)

    cv2.destroyAllWindows()
    print("book setup finished, config file saved as 'books.json'")
    

def run(img):

    print("Loading locations...")

    with open('location.json') as file:
        json_file = json.load(file)

    img = load_location(img, json_file)

    print("Locations load finished, img is shown")

    cv2.namedWindow("book_setup")
    cv2.imshow("book_setup", img)

    thread_enter_books = threading.Thread(target=enter_books, args=(json_file,))
    thread_enter_books.start()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    thread_enter_books.join()

