import gradio as gr
import cv2
import json
import numpy as np
import heapq
from dialogue_gradio import dialogue_page_gradio
from webui_pages.utils import *

api = ApiRequest(base_url=api_address())
def model(input_string):
    global api
    # return "书籍名称", "这是推荐的理由。"
    text = dialogue_page_gradio(api, "给我推荐一本书，要求：" + input_string + "，并给出推荐理由。你的回答格式为：\"书名：{}\n推荐理由：{}\"")
    name = text[text.find("书名：") + 3:text.find("推荐理由：")].strip(' ').strip('\n').strip("《").strip("》")
    reason = text[text.find("推荐理由：") + 5:].strip(' ').strip('\n')
    print(name, reason)
    return name, reason

# 从 setup_books.py 和 planner.py 中提取的相关函数
def load_location(img, json_file):
    with open(json_file, 'r') as file:
        location = json.load(file)
    for idx in range(len(location)):
        center = location[str(idx)]
        cv2.circle(img, center, 5, (0, 0, 255), -1)
    return img

def dijkstra(n, m, sx, sy, ex, ey, img_gray):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    dist = np.ones((n, m)) * 1000
    fromx = np.zeros((n, m), np.int32)
    fromy = np.zeros((n, m), np.int32)
    dist[sx, sy] = 0
    q = [(0, sx, sy)]
    
    while len(q) > 0:
        d, x, y = heapq.heappop(q)
        if d > dist[x, y]:
            continue
        if np.abs(x - ex) + np.abs(y - ey) <= 5:
            ex, ey = x, y
            break
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < n and 0 <= ny < m and dist[nx, ny] > dist[x, y] + 1 and img_gray[ny, nx] == 255:
                dist[nx, ny] = dist[x, y] + 1
                fromx[nx, ny] = x
                fromy[nx, ny] = y
                heapq.heappush(q, (dist[nx, ny], nx, ny))
    path = []
    x, y = ex, ey
    while not (x == sx and y == sy):
        path.append((x, y))
        nx, ny = fromx[x, y], fromy[x, y]
        x, y = nx, ny
    path.reverse()
    return path

def generate_path(sx, sy, ex, ey):
    global img, img_gray
    m, n = img_gray.shape
    path = dijkstra(n, m, sx, sy, ex, ey, img_gray)
    img_path = img.copy()
    for x, y in path:
        cv2.circle(img_path, (x, y), 1, (0, 255, 0), -1)
    cv2.circle(img_path, (ex, ey), 5, (0, 0, 255), -1)
    cv2.circle(img_path, (sx, sy), 5, (255, 0, 0), -1)
    return img_path

# Gradio 接口函数
def library_system(input_string):
    recommended_book, reason = model(input_string)
    return f"《{recommended_book}》", reason

def on_click(evt: gr.SelectData, locations, book_name):
    global img, img_gray
    try:
        print(f"推荐书名：{book_name}")
        print(f"图书位置集合：{locations}")

        # 去除书名中的《》符号并处理大小写
        clean_book_name = book_name.strip().strip('《').strip('》')

        # 找到书籍位置
        book_location_key = None
        for location, books in locations.items():
            if any(clean_book_name == book.strip() for book in books):  # 去除书名中的空格并忽略大小写
                book_location_key = location
                break
        print(f"书籍位置：{book_location_key}")
        print(f"点击坐标：({evt.index[0]}, {evt.index[1]})") # 获取点击的x和y坐标
        if book_location_key is None:
            raise ValueError("书籍位置未找到")
        
        # 从 location.json 中获取书籍位置
        with open('Library/location.json', 'r', encoding='utf-8') as file:
            location_data = json.load(file)
        print(f"书籍位置数据：{location_data}")
        if book_location_key not in location_data:
            raise ValueError("书籍位置的坐标未找到")
        
        ex, ey = location_data[book_location_key]
        sx, sy = evt.index[0], evt.index[1]
        
        # 生成路径
        img_with_path = generate_path(sx, sy, ex, ey)
        # img_with_path = img
        print(f"起始坐标：({sx}, {sy})")
        print(f"终点坐标：({ex}, {ey})")
        return img_with_path

    except Exception as e:
        print(f"发生错误: {e}")
        gr.Error("书籍未找到！")
        return img


def prepare_location(img_path):
    global img, img_gray
    with open('Library/books.json', 'r', encoding='utf-8') as file:
        locations = json.load(file)
    # 读取图书馆图像
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    inflation_radius = 0
    img_gray = cv2.imread("Library/library_gray.jpg", cv2.IMREAD_GRAYSCALE)
    # img_gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    # img_gray = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # img_gray[np.where(img_gray > 150)] = 255
    img_inflation = img_gray.copy()
    for (i, j), value in np.ndenumerate(img_gray):
        if value < 255:
            for k in range(-inflation_radius, inflation_radius):
                for w in range(-inflation_radius, inflation_radius):
                    if i + k >= 0 and i + k < img_gray.shape[0] and j + w >= 0 and j + w < img_gray.shape[1]:
                        if k ** 2 + w ** 2 <= inflation_radius ** 2:
                            img_inflation[i + k, j + w] = 0
    img_gray = img_inflation.copy()
    # cv2.imwrite("img_gray.jpg", img_gray)
    return locations

if __name__ == '__main__':
    print("=================================================")
    # dialogue_page_gradio(api, "给我推荐一本书，要求：动漫，并给出推荐理由。你的回答格式为：\"书名：{}\n推荐理由：{}\"")
    global img, img_gray
    locations = prepare_location("Library/library.jpg")
    img_library = load_location(img, "Library/location.json")
    # Gradio 组件定义
    with gr.Blocks() as demo:

        gr.Markdown("<h1><b>图书馆智能寻书系统</b></h1>")
        
        with gr.Row():
            with gr.Column():
                book_input = gr.Textbox(label="您想找本什么样的书？")
                recommended_book_output = gr.Textbox(label="为您推荐的书籍名称：")
                reason_output = gr.Textbox(label="为您推荐的理由：")
                image_output = gr.Image(value=img_library, label="请点击确认您的位置，下面是为您规划的最优路径")

            with gr.Column():
                submit_button = gr.Button("提交")
        
        submit_button.click(
            library_system, 
            inputs=[book_input], 
            outputs=[recommended_book_output, reason_output]
        )
        # 将 books.json 文件路径传递给 on_click 回调函数
        image_output.select(on_click, inputs=[gr.State(locations), recommended_book_output], outputs=image_output)

    # 启动 Gradio 应用
        demo.queue().launch(share=True, server_port=9004)

