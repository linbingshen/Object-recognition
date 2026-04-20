import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from PIL import Image, ImageTk
from yolo_detector import YOLODetector

## 登录系统类
class LoginSystem:
    # 初始化登录系统
    def __init__(self):
        # 创建登录窗口
        self.window = tk.Tk()
        self.window.title("系统登录")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        # 用户数据文件路径
        self.users_file = "users.json"
        self.current_frame = None
        # 居中窗口
        self.center_window()
        # 加载用户数据
        self.load_users()
        # 显示登录界面
        self.show_login_frame()

    # 居中窗口
    def center_window(self):
        # 更新窗口以获取正确尺寸
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        # 计算居中位置
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        # 设置窗口位置
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    # 加载用户数据
    def load_users(self):
        # 检查用户文件是否存在
        if os.path.exists(self.users_file):
            # 读取用户数据
            with open(self.users_file, "r", encoding="utf-8") as f:
                self.users = json.load(f)
        else:
            # 初始化空用户数据
            self.users = {}

    # 保存用户数据
    def save_users(self):
        # 将用户数据保存到文件
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    # 显示登录框架
    def show_login_frame(self):
        # 销毁现有框架
        if self.current_frame:
            self.current_frame.destroy()
        # 创建新的登录框架
        self.current_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # 登录标题
        title_label = tk.Label(
            self.current_frame,
            text="欢迎登录",
            font=("Microsoft YaHei", 24, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=20)

        # 登录输入框框架
        input_frame = tk.Frame(self.current_frame, bg="#f0f0f0")
        input_frame.pack(pady=20)

        # 用户名输入
        tk.Label(input_frame, text="用户名", font=("Microsoft YaHei", 12), bg="#f0f0f0").grid(row=0, column=0, pady=10, sticky="w")
        self.login_username = tk.Entry(input_frame, font=("Microsoft YaHei", 12), width=20)
        self.login_username.grid(row=0, column=1, pady=10, padx=10)

        # 密码输入
        tk.Label(input_frame, text="密码", font=("Microsoft YaHei", 12), bg="#f0f0f0").grid(row=1, column=0, pady=10, sticky="w")
        self.login_password = tk.Entry(input_frame, font=("Microsoft YaHei", 12), width=20, show="*")
        self.login_password.grid(row=1, column=1, pady=10, padx=10)

        # 登录按钮框架
        btn_frame = tk.Frame(self.current_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        # 登录按钮
        login_btn = tk.Button(
            btn_frame,
            text="登 录",
            font=("Microsoft YaHei", 14),
            width=15,
            height=2,
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            command=self.do_login
        )     
        login_btn.pack(pady=10, padx=10)     # 登录按钮位置
        # 绑定密码输入框的Return键事件
        self.login_password.bind("<Return>", lambda e: self.do_login())
        # 绑定登录按钮点击事件
        login_btn.bind("<Button-1>", self.do_login)

    # 登录按钮点击事件
    def do_login(self, event=None):
        # 获取用户名和密码
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        # 验证输入
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码")
            return

        # 验证用户凭证
        if username in self.users and self.users[username] == password:
            # 登录成功，关闭登录窗口并打开主窗口
            self.window.destroy()   # 关闭登录窗口

            main_window = MainWindow(username)   # 创建主窗口实例对象

            
        else:
            # 登录失败
            messagebox.showerror("错误", "用户名或密码错误")

    # 运行登录系统
    def run(self):
        # 启动主循环
        self.window.mainloop()

## 主窗口类
class MainWindow:
    # 初始化主窗口
    def __init__(self, username ="用户名"):
        # 保存用户名
        self.username = username
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title("主界面")
        # 获取屏幕尺寸
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        # 设置窗口尺寸为屏幕的一半
        self.window.geometry(f"{screen_width // 2}x{screen_height // 2}")
        # 设置最小窗口尺寸
        self.window.minsize(300, 200)
        # 居中窗口
        self.center_window()
        # 当前内容框架
        self.current_content = None

        self.show()   # 显示主窗口

    # 居中显示主窗口
    def center_window(self):
        # 更新窗口以获取正确尺寸
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        # 计算居中位置
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        # 设置窗口位置
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    # 显示主界面
    def show(self):
        # 创建布局
        self.create_layout()
        # 显示工作界面
        self.show_workspace()
        # 绑定关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    # 创建主界面布局
    def create_layout(self):
        # 设置窗口背景
        self.window.configure(bg="#ecf0f1")

        # 顶部导航栏
        top_frame = tk.Frame(self.window, bg="#3498db", height=60)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # 系统标题
        tk.Label(
            top_frame,
            text="管理系统",
            font=("Microsoft YaHei", 18, "bold"),
            bg="#3498db",
            fg="white"
        ).pack(side=tk.LEFT, padx=20)

        # 当前用户信息
        user_label = tk.Label(
            top_frame,
            text=f"当前用户：{self.username}",
            font=("Microsoft YaHei", 11),
            bg="#3498db",
            fg="white"
        )
        user_label.pack(side=tk.RIGHT, padx=20)

        # 退出登录按钮
        btn_logout = tk.Button(
            top_frame,
            text="退出登录",
            font=("Microsoft YaHei", 10),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.logout
        )
        btn_logout.pack(side=tk.RIGHT, padx=10)

        # 侧边栏
        sidebar_frame = tk.Frame(self.window, bg="#2c3e50", width=180)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # 菜单项
        menu_items = [
            ("工作界面", self.show_workspace),
            ("设置界面", self.show_settings)
        ]

        # 创建菜单按钮
        for i, (text, command) in enumerate(menu_items):
            btn = tk.Button(
                sidebar_frame,
                text=text,
                font=("Microsoft YaHei", 12),
                bg="#34495e" if i == 0 else "#2c3e50",
                fg="white",
                cursor="hand2",
                command=command,
                relief=tk.FLAT,
                width=15,
                height=2
            )
            btn.pack(pady=2)

        # 内容区域
        self.content_frame = tk.Frame(self.window, bg="#ecf0f1")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # 清除当前内容
    def clear_content(self):
        # 销毁当前内容框架
        if self.current_content:
            self.current_content.destroy()

    # 显示工作界面
    def show_workspace(self):
        # 清除当前内容
        self.clear_content()
        # 创建新的工作界面
        self.current_content = tk.Frame(self.content_frame, bg="#ecf0f1")
        self.current_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = tk.Label(
            self.current_content,
            text="YOLO V8 物体检测",
            font=("Microsoft YaHei", 20, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 30))

        # 主框架
        main_frame = tk.Frame(self.current_content, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 顶部按钮区域
        top_frame = tk.Frame(main_frame, bg="#ecf0f1")
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        # 第一行：加载模型
        btn_frame1 = tk.Frame(top_frame, bg="#ecf0f1")
        btn_frame1.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # 加载模型按钮
        tk.Button(
            btn_frame1,
            text="加载模型",
            font=("Microsoft YaHei", 12),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            width=12,
            command=self.load_model
        ).pack(side=tk.TOP, pady=5)

        # 第二行：文件检测
        btn_frame2 = tk.Frame(top_frame, bg="#ecf0f1")
        btn_frame2.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # 文件检测下拉菜单
        file_detect_var = tk.StringVar()
        file_detect_var.set("文件检测")
        
        file_detect_menu = tk.OptionMenu(btn_frame2, file_detect_var, "图片检测", "视频检测", "文件夹检测")
        file_detect_menu.config(
            font=("Microsoft YaHei", 11),
            bg="#3498db",
            fg="white",
            width=12,
            cursor="hand2"
        )
        file_detect_menu.pack(side=tk.TOP, pady=5)

        # 执行文件检测按钮
        def execute_file_detect():
            detect_type = file_detect_var.get()
            if detect_type == "图片检测":
                self.detect_single_image()
            elif detect_type == "视频检测":
                self.detect_video()
            elif detect_type == "文件夹检测":
                self.detect_folder()

        tk.Button(
            btn_frame2,
            text="执行检测",
            font=("Microsoft YaHei", 12),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            width=12,
            command=execute_file_detect
        ).pack(side=tk.TOP, pady=5)

        # 第三行：实时检测
        btn_frame3 = tk.Frame(top_frame, bg="#ecf0f1")
        btn_frame3.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # 摄像头检测按钮
        tk.Button(
            btn_frame3,
            text="实时检测（摄像头）",
            font=("Microsoft YaHei", 12),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            width=15,
            command=self.detect_camera
        ).pack(side=tk.TOP, pady=5)

        # 中间区域：预览和结果
        center_frame = tk.Frame(main_frame, bg="#ecf0f1")
        center_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧：待检测内容预览（左下角半部分）
        preview_frame = tk.Frame(center_frame, bg="#ddd", relief=tk.RIDGE, borderwidth=2)
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # 预览标题
        tk.Label(
            preview_frame,
            text="待检测内容预览",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#ddd",
            fg="#2c3e50"
        ).pack(pady=5, padx=10, anchor=tk.W)

        # 图片显示区域
        self.image_label = tk.Label(preview_frame, text="请选择文件或启动实时检测", bg="#f5f5f5")
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 右侧：检测结果（右半部分）
        result_frame = tk.Frame(center_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # 检测结果标题
        tk.Label(
            result_frame,
            text="检测结果",
            font=("Microsoft YaHei", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=10)

        # 滚动条
        result_scroll = tk.Scrollbar(result_frame)
        result_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # 结果文本框
        self.result_text = tk.Text(
            result_frame,
            font=("Microsoft YaHei", 11),
            yscrollcommand=result_scroll.set
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        result_scroll.config(command=self.result_text.yview)

        # 状态标签
        self.status_label = tk.Label(
            self.current_content,
            text="状态：就绪",
            font=("Microsoft YaHei", 10),
            bg="#ecf0f1",
            fg="#27ae60"
        )
        self.status_label.pack(pady=5)

    # 显示设置界面
    def show_settings(self):
        # 清除当前内容
        self.clear_content()
        # 创建设置界面
        self.current_content = tk.Frame(self.content_frame, bg="#ecf0f1")
        self.current_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = tk.Label(
            self.current_content,
            text="设置界面",
            font=("Microsoft YaHei", 20, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))

        # 设置框架
        settings_frame = tk.Frame(self.current_content, bg="white", relief=tk.RIDGE, borderwidth=2)
        settings_frame.pack(fill=tk.X, pady=10)

        # 设置项
        settings_items = [
            ("个人设置", "修改个人信息"),
            ("系统设置", "配置系统参数"),
            ("权限设置", "管理用户权限"),
            ("关于系统", "查看系统信息")
        ]

        # 创建设置项
        for i, (title, desc) in enumerate(settings_items):
            item_frame = tk.Frame(settings_frame, bg="white" if i % 2 == 0 else "#f8f9fa", relief=tk.RIDGE, borderwidth=1)
            item_frame.pack(fill=tk.X, pady=1)

            # 设置标题
            tk.Label(
                item_frame,
                text=title,
                font=("Microsoft YaHei", 12, "bold"),
                bg=item_frame.cget("bg"),
                fg="#2c3e50",
                width=15,
                anchor="w"
            ).pack(side=tk.LEFT, padx=20, pady=15)

            # 设置描述
            tk.Label(
                item_frame,
                text=desc,
                font=("Microsoft YaHei", 10),
                bg=item_frame.cget("bg"),
                fg="#7f8c8d",
                anchor="w"
            ).pack(side=tk.LEFT, padx=10, pady=15)

            # 设置按钮
            tk.Button(
                item_frame,
                text="设置",
                font=("Microsoft YaHei", 9),
                bg="#3498db",
                fg="white",
                cursor="hand2",
                command=lambda t=title: messagebox.showinfo("提示", f"打开{t}设置")
            ).pack(side=tk.RIGHT, padx=20)

    # 加载模型
    def load_model(self):
        try:
            # 更新状态
            self.status_label.config(text="状态：正在加载模型...", fg="#f39c12")
            self.window.update()
            # 初始化YOLO检测器
            self.detector = YOLODetector()
            # 更新状态
            self.status_label.config(text="状态：模型加载成功", fg="#27ae60")
        except Exception as e:
            # 显示错误信息
            self.status_label.config(text="状态：模型加载失败", fg="#e74c3c")
            messagebox.showerror("错误", f"模型加载失败：{str(e)}")

    # 单独检测单张图片
    def detect_single_image(self):
        # 检查模型是否加载
        if not hasattr(self, 'detector'):
            messagebox.showwarning("提示", "请先加载模型")
            return

        # 选择图片文件
        image_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp"), ("所有文件", "*.*")]
        )
        if not image_path:
            return

        # 获取图片所在目录
        image_dir = os.path.dirname(image_path)
        # 设置默认保存路径为图片目录下的 detection_results 文件夹
        default_save_path = os.path.join(image_dir, "detection_results")

        try:
            # 更新状态
            self.status_label.config(text="状态：正在检测图片...", fg="#f39c12")
            self.window.update()

            # 执行图片检测
            result = self.detector.detect_image(image_path)

            # 清空结果文本
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"图片检测结果：\n\n")
            self.result_text.insert(tk.END, f"文件：{os.path.basename(image_path)}\n\n")

            # 显示检测结果
            if result['objects']:
                self.result_text.insert(tk.END, f"检测到 {len(result['objects'])} 个物体：\n\n")
                for obj in result['objects']:
                    self.result_text.insert(tk.END, f"• {obj['class']} (置信度: {obj['confidence']:.2%})\n")
                
                # 保存检测结果
                if not os.path.exists(default_save_path):
                    os.makedirs(default_save_path)
                
                # 生成保存文件名
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                save_filename = f"detection_{timestamp}.jpg"
                save_filepath = os.path.join(default_save_path, save_filename)
                
                # 保存带标注的图像
                cv2.imwrite(save_filepath, result['image'])
                # 详细显示保存结果
                self.result_text.insert(tk.END, f"\n\n===== 保存结果 =====\n")
                self.result_text.insert(tk.END, f"保存路径：{default_save_path}\n")
                self.result_text.insert(tk.END, f"保存文件名：{save_filename}\n")
                self.result_text.insert(tk.END, f"完整路径：{save_filepath}\n")
                self.result_text.insert(tk.END, f"=================\n")
            else:
                self.result_text.insert(tk.END, "未检测到物体")

            # 更新状态
            self.status_label.config(text="状态：图片检测完成", fg="#27ae60")
        except Exception as e:
            # 显示错误信息
            self.status_label.config(text="状态：图片检测失败", fg="#e74c3c")
            messagebox.showerror("错误", f"图片检测失败：{str(e)}")

    # 视频检测
    def detect_video(self):
        # 检查模型是否加载
        if not hasattr(self, 'detector'):
            messagebox.showwarning("提示", "请先加载模型")
            return

        # 打开视频文件选择对话框
        video_path = filedialog.askopenfilename(
            title="选择视频",
            filetypes=[("视频文件", "*.mp4 *.avi *.mov"), ("所有文件", "*.*")]
        )
        if video_path:
            # 获取视频所在目录
            video_dir = os.path.dirname(video_path)
            # 设置默认保存路径为视频目录下的 detection_results 文件夹
            default_save_path = os.path.join(video_dir, "detection_results")
            
            # 创建保存目录
            if not os.path.exists(default_save_path):
                os.makedirs(default_save_path)
            
            # 生成输出视频路径
            video_name = os.path.basename(video_path)
            output_video_name = f"{os.path.splitext(video_name)[0]}_result.avi"
            output_video_path = os.path.join(default_save_path, output_video_name)
            
            try:
                # 更新状态
                self.status_label.config(text="状态：正在检测视频...", fg="#f39c12")
                self.window.update()
                # 执行视频检测
                self.detector.detect_video(video_path, output_video_path)
                # 更新状态
                self.status_label.config(text="状态：视频检测完成", fg="#27ae60")
                
                # 在结果文本框中显示保存结果
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "视频检测结果：\n\n")
                self.result_text.insert(tk.END, f"视频文件：{os.path.basename(video_path)}\n\n")
                self.result_text.insert(tk.END, "===== 保存结果 =====\n")
                self.result_text.insert(tk.END, f"保存路径：{default_save_path}\n")
                self.result_text.insert(tk.END, f"保存文件名：{output_video_name}\n")
                self.result_text.insert(tk.END, f"完整路径：{output_video_path}\n")
                self.result_text.insert(tk.END, f"=================\n")
                
                messagebox.showinfo("提示", f"视频检测完成！\n结果已保存到：{output_video_path}")
            except Exception as e:
                # 显示错误信息
                self.status_label.config(text="状态：视频检测失败", fg="#e74c3c")
                messagebox.showerror("错误", f"视频检测失败：{str(e)}")

    # 摄像头检测
    def detect_camera(self):
        # 检查模型是否加载
        if not hasattr(self, 'detector'):
            messagebox.showwarning("提示", "请先加载模型")
            return

        # 选择保存路径
        save_path = filedialog.askdirectory(title="选择保存识别结果的目录")
        
        # 设置默认保存路径
        if not save_path:
            # 默认保存到当前目录的detections文件夹
            default_path = os.path.join(os.getcwd(), "detections")
            # 询问用户是否使用默认路径
            if messagebox.askyesno("提示", f"是否使用默认保存路径：{default_path}？"):
                save_path = default_path
            else:
                # 如果用户拒绝默认路径，仍然可以进行检测但不保存
                try:
                    # 更新状态
                    self.status_label.config(text="状态：正在检测摄像头...", fg="#f39c12")
                    self.window.update()
                    # 执行摄像头检测（不保存）
                    self.detector.detect_camera()
                    # 更新状态
                    self.status_label.config(text="状态：摄像头检测完成", fg="#27ae60")
                except Exception as e:
                    # 显示错误信息
                    self.status_label.config(text="状态：摄像头检测失败", fg="#e74c3c")
                    messagebox.showerror("错误", f"摄像头检测失败：{str(e)}")
                return

        # 获取保存数量
        from tkinter import simpledialog
        max_save_count = simpledialog.askinteger(
            "保存设置", 
            "请输入最大保存数量：", 
            minvalue=1, 
            maxvalue=100, 
            initialvalue=10
        )
        if max_save_count is None:
            return

        try:
            # 更新状态
            self.status_label.config(text="状态：正在检测摄像头...", fg="#f39c12")
            self.window.update()
            # 执行摄像头检测（带保存）
            self.detector.detect_camera(save_path=save_path, max_save_count=max_save_count)
            # 更新状态
            self.status_label.config(text="状态：摄像头检测完成", fg="#27ae60")
            
            # 在结果文本框中显示保存结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "摄像头检测结果：\n\n")
            self.result_text.insert(tk.END, f"最大保存数量：{max_save_count}\n\n")
            self.result_text.insert(tk.END, "===== 保存结果 =====\n")
            self.result_text.insert(tk.END, f"保存路径：{save_path}\n")
            self.result_text.insert(tk.END, f"保存文件格式：detection_年月日_时分秒.jpg\n")
            self.result_text.insert(tk.END, f"=================\n")
            
            messagebox.showinfo("提示", f"摄像头检测完成！\n已保存识别结果到：{save_path}")
        except Exception as e:
            # 显示错误信息
            self.status_label.config(text="状态：摄像头检测失败", fg="#e74c3c")
            messagebox.showerror("错误", f"摄像头检测失败：{str(e)}")

    # 对文件夹中的文件检测（主要为视频和图片）
    def detect_folder(self):
        # 检查模型是否加载
        if not hasattr(self, 'detector'):    # 检查是否有检测器实例
            messagebox.showwarning("提示", "请先加载模型")
            return

        # 选择文件夹
        folder_path = filedialog.askdirectory(title="选择要检测的文件夹")
        if not folder_path:
            return

        # 设置默认保存路径为文件夹所在目录下的 detection_results 文件夹
        folder_dir = os.path.dirname(folder_path)
        default_save_path = os.path.join(folder_dir, "detection_results")
        
        # 创建保存目录
        if not os.path.exists(default_save_path):
            os.makedirs(default_save_path)

        try:
            # 更新状态
            self.status_label.config(text="状态：正在批量检测文件夹...", fg="#f39c12")
            self.window.update()

            # 执行文件夹检测
            result = self.detector.detect_folder(folder_path, default_save_path)
            
            # 清空结果文本
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "文件夹检测结果：\n\n")
            
            # 显示检测统计
            self.result_text.insert(tk.END, f"总文件数：{result['total_files']}\n")
            self.result_text.insert(tk.END, f"检测到的物体数：{result['detected_objects']}\n\n")
            
            # 显示保存结果
            self.result_text.insert(tk.END, "===== 保存结果 =====\n")
            self.result_text.insert(tk.END, f"保存路径：{default_save_path}\n")
            self.result_text.insert(tk.END, f"=================\n\n")
            
            # 显示详细结果
            self.result_text.insert(tk.END, "详细结果：\n")
            for file, file_result in result['results'].items():
                if isinstance(file_result, list):
                    self.result_text.insert(tk.END, f"• {file}: 检测到 {len(file_result)} 个物体\n")
                else:
                    self.result_text.insert(tk.END, f"• {file}: {file_result}\n")

            # 更新状态
            self.status_label.config(text="状态：文件夹检测完成", fg="#27ae60")
            messagebox.showinfo("提示", f"文件夹检测完成！\n总文件数：{result['total_files']}\n检测到的物体数：{result['detected_objects']}\n结果已保存到：{default_save_path}")
        except Exception as e:
            # 显示错误信息
            self.status_label.config(text="状态：文件夹检测失败", fg="#e74c3c")
            messagebox.showerror("错误", f"文件夹检测失败：{str(e)}")

    # 关闭系统
    def on_close(self):
        # 确认关闭
        if messagebox.askyesno("确认", "确定要关闭系统吗？"):
            # 销毁窗口
            self.window.destroy()

    # 退出登录
    def logout(self):
        # 确认退出
        if messagebox.askyesno("确认", "确定要退出登录吗？"):
            # 销毁窗口
            self.window.destroy()

    # 运行主窗口
    def run(self):
        # 启动主循环
        self.window.mainloop()

if __name__ == "__main__":
    # 创建并运行登录系统
    app = LoginSystem()
    app.run()

  

