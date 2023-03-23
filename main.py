import tkinter
from tkinter import Tk, Canvas
import pandas as pd
from PIL import ImageTk, Image
from typing import List

filename = 'data.xlsx'

w, h = None, None  # fullscreen
coordinates: List = []
data: List = []
x_min, y_min = 22.138056, 44.386389
x_max, y_max = 40.223611, 52.377778
size_min = 2
size_max = 4


class War(Canvas):

    def __init__(self, root):
        super().__init__(root)
        self.pack(fill='both', expand=True, anchor=tkinter.NW)

    def draw(self):
        image = ImageTk.PhotoImage(Image.open('Ukraine.png'))
        self.create_image(0, 0, image=image)

        x, y = data['LATITUDE'], data['LONGITUDE']
        x_remap = lambda v: w * ((v - x_min) / (x_max - x_min))
        y_remap = lambda v: h * ((v - y_min) / (y_max - y_min))

        for index, row in data.iterrows():
            x, y = row['LONGITUDE'], row['LATITUDE']
            print(x, y)
            xx, yy = x_remap(x), y_remap(y)
            ss = size_min
            self.create_oval(xx-ss/2, yy-ss/2, xx+ss/2, yy+ss/2, fill='red', outline=None)


def load_data():
    global data
    excel_data = pd.read_excel(filename)
    df = pd.DataFrame(excel_data, columns=['YEAR', 'COUNTRY', 'LATITUDE', 'LONGITUDE', 'LOCATION'])
    data = df.loc[(df['COUNTRY'] == "Ukraine") & (df['YEAR'].astype(int) > 2021)]


if __name__ == '__main__':
    # root
    root = Tk()
    root.title("War")
    # window width and height
    if w is None:
        w = root.winfo_screenwidth()
    if h is None:
        h = root.winfo_screenheight()
    root.geometry(f'{w}x{h}')
    # skymap init
    war = War(root)
    # load the dataset
    load_data()
    # draw the stars
    war.draw()
    # mainloop
    root.mainloop()
