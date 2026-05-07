"""
YOLO V8 目标检测工具类
功能描述: 提供基于YOLO V8的图像、视频、摄像头实时检测及文件夹批量检测功能
作者: 自动生成
版本: 1.0
"""

# 导入所需库
from ultralytics import YOLO  # YOLO V8模型库
import cv2  # OpenCV库，用于图像处理和视频操作
import numpy as np  # 数值计算库
from PIL import Image  # PIL图像库
import os  # 文件系统操作
import datetime  # 日期时间处理


class YOLODetector:
    """
    YOLO检测器类
    封装了YOLO V8模型的各种检测功能，包括：
    - 单张图片检测
    - 视频文件检测
    - 摄像头实时检测
    - 文件夹批量检测
    """

    def __init__(self, model_path="yolov8n.pt"):
        """
        初始化YOLO检测器
        
        Args:
            model_path: 模型文件路径，默认为yolov8n.pt（YOLO V8 nano版本）
        """
        # 加载YOLO模型（自动下载或从本地加载）
        self.model = YOLO(model_path)
        # 获取模型的类别名称列表
        self.class_names = self.model.names

    # 检测单张图片
    def detect_image(self, image_path, conf_threshold=0.3):
        """
        检测单张图片中的目标对象
        
        Args:
            image_path: 图片文件的路径
            conf_threshold: 置信度阈值，低于此值的检测结果将被过滤，默认0.3
            
        Returns:
            dict: 检测结果字典，包含：
                - objects: 检测到的对象列表，每个对象包含class、confidence、bbox
                - image: 原始图像（numpy数组格式）
        """
        # 使用YOLO模型检测图片，conf参数设置置信度阈值
        results = self.model(image_path, conf=conf_threshold)
        # 获取第一个检测结果（单张图片只有一个结果）
        result = results[0]

        # 提取检测框坐标（xyxy格式：x1, y1, x2, y2），转换为numpy数组
        boxes = result.boxes.xyxy.cpu().numpy()
        # 提取检测类别索引，转换为整数
        classes = result.boxes.cls.cpu().numpy().astype(int)
        # 提取置信度值
        confidences = result.boxes.conf.cpu().numpy()

        # 构建检测对象列表
        detected_objects = []
        # 遍历每个检测框
        for box, cls, conf in zip(boxes, classes, confidences):
            detected_objects.append({
                "class": self.class_names[cls],  # 类别名称
                "confidence": float(conf),       # 置信度
                "bbox": box.tolist()             # 检测框坐标
            })

        # 返回检测结果
        return {
            "objects": detected_objects,  # 检测到的对象列表
            "image": result.orig_img      # 原始图像
        }

    # 检测视频
    def detect_video(self, video_path, output_path=None, conf_threshold=0.3):
        """
        检测视频文件中的目标对象
        
        Args:
            video_path: 视频文件的路径
            output_path: 输出视频路径，为None时不保存只显示
            conf_threshold: 置信度阈值，默认0.3
            
        Returns:
            bool: 检测是否成功完成
        """
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        # 检查视频是否成功打开
        if not cap.isOpened():
            return False  # 无法打开视频，返回失败

        # 如果指定了输出路径，创建视频写入器
        if output_path:
            # 获取视频宽度
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            # 获取视频高度
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # 获取视频帧率
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            # 创建VideoWriter对象，使用XVID编码
            out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

        # 循环读取视频帧
        while cap.isOpened():
            # 读取一帧
            ret, frame = cap.read()
            # 如果读取失败（视频结束），退出循环
            if not ret:
                break

            # 使用YOLO模型检测当前帧
            results = self.model(frame, conf=conf_threshold)
            # 在帧上绘制检测结果
            annotated_frame = results[0].plot()

            # 如果指定了输出路径，写入帧
            if output_path:
                out.write(annotated_frame)

            # 显示检测结果窗口
            cv2.imshow('YOLO Video Detection', annotated_frame)
            # 等待1毫秒，按'q'键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 释放视频捕获对象
        cap.release()
        # 如果创建了视频写入器，释放它
        if output_path:
            out.release()
        # 关闭所有OpenCV窗口
        cv2.destroyAllWindows()

        # 返回成功
        return True

    # 检测摄像头
    def detect_camera(self, camera_id=0, conf_threshold=0.3, save_path=None, max_save_count=10, stop_event=None):
        """
        实时检测摄像头画面中的目标对象
        
        Args:
            camera_id: 摄像头ID，默认为0（内置摄像头）
            conf_threshold: 置信度阈值，默认0.3
            save_path: 保存识别结果的路径，为None时不保存
            max_save_count: 最大保存图片数量，默认10张
            stop_event: 停止事件（可选），用于外部控制停止检测
            
        Returns:
            dict/bool: 失败时返回错误信息字典，成功时返回True
        """
        # 打开摄像头
        cap = cv2.VideoCapture(camera_id)
        # 检查摄像头是否成功打开
        if not cap.isOpened():
            return {"status": "error", "message": "无法打开摄像头"}

        # 创建检测窗口
        cv2.namedWindow('YOLO Camera Detection')

        # 初始化保存计数
        save_count = 0

        # 记录上一次检测结果，用于判断是否有新内容
        last_detection = set()

        # 如果指定了保存路径，创建保存目录
        if save_path and not os.path.exists(save_path):
            os.makedirs(save_path)

        # 循环读取摄像头帧
        while cap.isOpened():
            # 检查外部停止信号
            if stop_event and stop_event.is_set():
                break

            # 读取一帧
            ret, frame = cap.read()
            # 如果读取失败，退出循环
            if not ret:
                break

            # 使用YOLO模型检测当前帧
            results = self.model(frame, conf=conf_threshold)
            # 在帧上绘制检测结果
            annotated_frame = results[0].plot()

            # 保存识别结果（如果设置了保存路径且未达到最大保存数量）
            if save_path and save_count < max_save_count:
                # 获取当前检测到的物体类别集合
                current_detection = set()
                for box in results[0].boxes:
                    cls = int(box.cls[0])
                    class_name = self.class_names[cls]
                    current_detection.add(class_name)

                # 检查是否有新内容（检测到的物体发生变化）
                if current_detection != last_detection:
                    # 生成带时间戳的保存文件名
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    save_filename = f"detection_{timestamp}.jpg"
                    save_filepath = os.path.join(save_path, save_filename)

                    # 保存带标注的图像
                    cv2.imwrite(save_filepath, annotated_frame)
                    save_count += 1
                    print(f"保存识别结果 {save_count}/{max_save_count}: {save_filename}")

                    # 更新上一次检测结果
                    last_detection = current_detection.copy()

            # 显示检测结果窗口
            cv2.imshow('YOLO Camera Detection', annotated_frame)

            # 检查按键，按'q'键退出
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

            # 检查窗口是否被关闭（处理点击右上角叉号的情况）
            try:
                # 尝试获取窗口属性，如果窗口已关闭会抛出异常
                if cv2.getWindowProperty('YOLO Camera Detection', cv2.WND_PROP_VISIBLE) < 1:
                    break
            except:
                break

        # 释放摄像头
        cap.release()
        # 关闭所有OpenCV窗口
        cv2.destroyAllWindows()

        return True

    # 绘制检测结果
    def draw_results(self, image, results):
        """
        在图像上手动绘制检测结果（用于自定义绘制）
        
        Args:
            image: 输入图像（numpy数组格式）
            results: 检测结果字典，包含objects列表
            
        Returns:
            numpy.ndarray: 绘制了检测结果的图像
        """
        # 遍历每个检测对象
        for obj in results['objects']:
            bbox = obj['bbox']          # 检测框坐标
            class_name = obj['class']   # 类别名称
            confidence = obj['confidence']  # 置信度

            # 将检测框坐标转换为整数
            x1, y1, x2, y2 = map(int, bbox)
            # 绘制矩形框（绿色，线宽2）
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # 绘制类别名称和置信度
            cv2.putText(
                image,
                f"{class_name}: {confidence:.2f}",  # 文本内容
                (x1, y1 - 10),                      # 文本位置（框上方10像素）
                cv2.FONT_HERSHEY_SIMPLEX,           # 字体
                0.9,                                # 字体大小
                (0, 255, 0),                        # 字体颜色（绿色）
                2                                   # 字体粗细
            )

        # 返回绘制后的图像
        return image

    # 批量检测文件夹中的图片和视频
    def detect_folder(self, folder_path, output_folder=None, conf_threshold=0.3):
        """
        批量检测文件夹中的所有图片和视频文件
        
        Args:
            folder_path: 待检测的文件夹路径
            output_folder: 检测结果保存路径，为None时不保存只显示
            conf_threshold: 置信度阈值，默认0.3
            
        Returns:
            dict: 检测结果统计，包含：
                - total_files: 处理的文件总数
                - detected_objects: 检测到的对象总数
                - results: 每个文件的检测结果
        """
        # 支持的图片格式列表
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        # 支持的视频格式列表
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']

        total_files = 0          # 总文件数
        detected_objects = 0     # 检测到的对象数
        results = {}             # 检测结果字典

        # 如果指定了输出文件夹且不存在，则创建
        if output_folder and not os.path.exists(output_folder):
            print(f"创建输出文件夹: {output_folder}")
            os.makedirs(output_folder)

        # 遍历文件夹中的所有文件
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # 获取文件完整路径
                file_path = os.path.join(root, file)
                # 获取文件扩展名（小写）
                file_ext = os.path.splitext(file)[1].lower()

                # 处理图片文件
                if file_ext in image_extensions:
                    total_files += 1
                    try:
                        # 检测图片
                        result = self.detect_image(file_path, conf_threshold)
                        # 保存检测结果
                        results[file] = result['objects']
                        # 更新检测到的对象数
                        detected_objects += len(result['objects'])

                        # 如果指定了输出文件夹，保存检测结果图片
                        if output_folder:
                            output_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_result.jpg")
                            cv2.imwrite(output_path, result['image'])
                    except Exception as e:
                        # 处理异常，打印错误信息
                        print(f"处理图片 {file} 时出错: {str(e)}")

                # 处理视频文件
                elif file_ext in video_extensions:
                    total_files += 1
                    try:
                        # 如果指定了输出文件夹，保存检测后的视频
                        if output_folder:
                            output_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_result.avi")
                            self.detect_video(file_path, output_path, conf_threshold)
                        else:
                            # 否则只显示不保存
                            self.detect_video(file_path, None, conf_threshold)
                        # 记录视频处理结果
                        results[file] = "视频已处理"
                    except Exception as e:
                        # 处理异常，打印错误信息
                        print(f"处理视频 {file} 时出错: {str(e)}")

        # 返回检测统计结果
        return {
            "total_files": total_files,      # 处理的文件总数
            "detected_objects": detected_objects,  # 检测到的对象总数
            "results": results              # 每个文件的详细结果
        }


# 主函数，用于测试
if __name__ == "__main__":
    # 创建YOLO检测器实例（使用默认模型）
    detector = YOLODetector()
    # 测试摄像头检测功能
    detector.detect_camera()
