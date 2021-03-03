"""
double
2020-3-2

编码目的：
    上传一张背景图片 在上面添加姓名 生成图片保存

编码思路：
    1。导入图片
    2。输入姓名
    3。字体选择
    4。大小调整
    5。位置调整
    6。字体颜色
    7。生成预览
    8。保存图片
"""
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk, ImageDraw, ImageFont


class GenerateImage:
    # 窗口
    window = None
    window_height = 800
    name = None
    font = None
    font_size = None
    font_x = None
    font_y = None
    font_color = None
    image_path = None
    cvs = None

    margin = 15

    coordinate = {
        'x': 0,
        'y': 0
    }

    # 左边内容
    frame_left = None
    frame_left_config = {
        'width': 800,
        'height': 770
    }

    # 右边内容
    frame_right = None
    frame_right_config = {
        'width': 400,
        'height': 770
    }

    gl_data = {
        'name': '',
        'style': '',
        'size': 50,
        'color': '#ffffff',
        'x': 0,
        'y': 0
    }

    image_buf = None
    background_buff = None
    image_frame = None
    image_paned = None

    def __init__(self):
        # 初始化窗口
        self.window = tk.Tk()

        # 设置标题
        self.window.title('上海如渔- 图片生成 - double')

        # 设置窗口大小
        self.window.geometry('%sx%s' % (self.frame_left_config['width'] + self.frame_right_config['width'] + self.margin*3,  self.window_height))

        # 监听姓名
        self.name = tk.StringVar()
        # 监听字体
        self.font = tk.StringVar()
        self.font.set('PingFangMedium.ttf')
        # 监听字体大小
        self.font_size = tk.IntVar()
        self.font_size.set(50)
        # 监听字体x坐标
        self.font_x = tk.IntVar()
        self.font_x.set(0)
        # 监听字体y坐标
        self.font_y = tk.IntVar()
        self.font_y.set(0)
        # 监听字体颜色
        self.font_color = tk.StringVar()
        self.font_color.set('#FFFFFF')
        # 图片地址
        self.image_path = tk.StringVar()

        # 构建框架
        self.created_frame()

        # 启动
        self.run()

    def created_frame(self):
        self.set_frame_left()
        self.set_frame_right()

    def set_image_frame(self, im):
        self.image_paned.photo = ImageTk.PhotoImage(im.resize((375, 630)))
        self.image_frame['image'] = self.image_paned.photo

    def open_image(self):
        file_path = askopenfilename(
            title='Please choose a file',
            initialdir='/',
            filetypes=[('jpg', '*.jpg'), ('png', '*.png')])

        self.image_path.set(file_path)
        self.background_buff = Image.open(file_path).convert('RGBA')

        # 把图片写如框架
        self.set_image_frame(self.background_buff)

    def set_frame_left(self):
        self.frame_left = tk.LabelFrame(self.window)
        self.frame_left.place(
            x=self.margin,
            y=self.margin,
            width=self.frame_left_config['width'],
            height=self.frame_left_config['height'])

        self.set_coordinate('x', self.frame_left_config['width'] + self.margin)

        # 设置图片选择和姓名输入
        top = tk.Frame(self.frame_left)
        top.columnconfigure(1, weight=1)

        top.place(
            x=self.margin,
            y=self.margin,
            width=self.frame_left_config['width'] - self.margin*2,
            height=60)

        image_path_label = tk.Label(top, text="图片地址:")
        image_path_text = tk.Label(top, textvariable=self.image_path)

        file_button = tk.Button(top, text='选择文件', command=self.open_image)

        image_path_label.grid(row=0, column=0)
        image_path_text.grid(row=0, column=1, sticky="w")
        file_button.grid(row=0, column=2)

        # img = ImageTk.PhotoImage(im)
        #
        # img=ImageTk.PhotoImage(self.image_buf.resize((100, 130)))

        image = tk.Frame(self.frame_left)

        image.place(
            y=self.margin*2 + 60,
            relwidth=1
        )
        self.image_paned = tk.PanedWindow(image, bg='#000000')
        self.image_paned.pack(side=tk.TOP)

        self.image_frame = tk.Label(self.image_paned)
        self.image_frame.pack()

    # 每次修改，都要改变名字的状态
    def change_name(self, key, val):
        self.gl_data[key] = val
        # 生成与原图大小完全一致的新图片,设定为完全透明
        # 设置字体信息所在的位置,写入的信息,颜色
        try:
            txt = Image.new('RGBA', self.background_buff.size, (0, 0, 0, 0))
            # 设置字体,字号
            fnt = ImageFont.truetype(self.gl_data['style'], int(self.gl_data['size']))
            d = ImageDraw.Draw(txt)
            d.text((int(self.gl_data['x']), int(self.gl_data['y'])), self.gl_data['name'], font=fnt, fill=self.gl_data['color'])
            # 保存新的图片
            self.image_buf = Image.alpha_composite(self.background_buff, txt)
            self.set_image_frame(self.image_buf)
        except:
            pass

        return True

    # 预览图片
    def show_image(self):
        try:
            self.image_buf.show()
        except:
            pass

    # 生成图片
    def go_image(self):
        try:
            file_path = askdirectory()
            self.image_buf.save('%s/%s.png' % (file_path, self.name.get()))
        except:
            pass

    def set_frame_right(self):
        self.frame_right = tk.LabelFrame(self.window)
        self.frame_right.place(
            x=self.coordinate['x'] + self.margin,
            y=self.margin,
            width=self.frame_right_config['width'],
            height=self.frame_right_config['height'])

        test_register = self.frame_right.register(self.change_name)

        name = tk.Label(self.frame_right, text='姓名:')
        name_text = tk.Entry(self.frame_right,
                             textvariable=self.name, validate='key',
                             validatecommand=(test_register, 'name', '%P'))

        font_style = tk.Label(self.frame_right, text='字体:')
        font_style_text = tk.Entry(self.frame_right,
                                   textvariable=self.font, validate='key', validatecommand=(test_register, 'style', '%P'))

        font_size = tk.Label(self.frame_right, text='字体大小:')
        font_size_text = tk.Entry(self.frame_right,
                                  textvariable=self.font_size,
                                  validate='key', validatecommand=(test_register, 'size', '%P'))

        font_color = tk.Label(self.frame_right, text='字体颜色:')
        font_color_text = tk.Entry(self.frame_right, textvariable=self.font_color,
                                   validate='key',
                                   validatecommand=(test_register, 'color', '%P'))

        font_x = tk.Label(self.frame_right, text='距离顶部:')
        font_x_text = tk.Entry(self.frame_right, textvariable=self.font_x,
                               validate='key',
                               validatecommand=(test_register, 'x', '%P'))

        font_y = tk.Label(self.frame_right, text='距离左侧:')
        font_y_text = tk.Entry(self.frame_right, textvariable=self.font_y,
                               validate='key',
                               validatecommand=(test_register, 'y', '%P'))

        submit_view = tk.Button(self.frame_right, text='预览图片', command=self.show_image)
        submit_go = tk.Button(self.frame_right, text='生成图片', command=self.go_image)

        name.grid(row=0, column=0)
        font_style.grid(row=1, column=0)
        font_size.grid(row=2, column=0)
        font_color.grid(row=3, column=0)
        font_x.grid(row=4, column=0)
        font_y.grid(row=5, column=0)

        name_text.grid(row=0, column=1)
        font_style_text.grid(row=1, column=1)
        font_size_text.grid(row=2, column=1)
        font_color_text.grid(row=3, column=1)
        font_x_text.grid(row=4, column=1)
        font_y_text.grid(row=5, column=1)

        submit_view.grid(row=6, column=0)
        submit_go.grid(row=6, column=1)

    # 设置坐标
    def set_coordinate(self, key, val):
        self.coordinate[key] = self.coordinate[key] + val

    def run(self):
        self.window.mainloop()


app = GenerateImage()
