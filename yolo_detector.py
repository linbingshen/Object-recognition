from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import os
import datetime
"""YOLO检测器类

"""

class YOLODetector:
    def __init__(self, model_path="yolov8n.pt"):
        """初始化YOLO检测器      
        Args:
            model_path: 模型文件路径，默认为yolov8n.pt
        """
        self.model = YOLO(model_path)   # 加载YOLO模型
        self.class_names = self.model.names
    
    def detect_image(self, image_path, conf_threshold=0.3):
        """检测单张图片       
        Args:
            image_path: 图片路径
            conf_threshold: 置信度阈值
            
        Returns:
            dict: 检测结果，包含boxes、classes、confidences
        """
        results = self.model(image_path, conf=conf_threshold)
        result = results[0]
        
        boxes = result.boxes.xyxy.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy().astype(int)
        confidences = result.boxes.conf.cpu().numpy()
        
        detected_objects = []
        for box, cls, conf in zip(boxes, classes, confidences):
            detected_objects.append({
                "class": self.class_names[cls],
                "confidence": float(conf),
                "bbox": box.tolist()
            })
        
        return {
            "objects": detected_objects,
            "image": result.orig_img
        }
    
    def detect_video(self, video_path, output_path=None, conf_threshold=0.3):
        """检测视频
     
        Args:
            video_path: 视频路径
            output_path: 输出视频路径
            conf_threshold: 置信度阈值
            
        Returns:
            bool: 检测是否成功
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False
        
        if output_path:
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            results = self.model(frame, conf=conf_threshold)
            annotated_frame = results[0].plot()
            
            if output_path:
                out.write(annotated_frame)
            
            cv2.imshow('YOLO Video Detection', annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
        
        return True
    
    def detect_camera(self, camera_id=0, conf_threshold=0.3, save_path=None, max_save_count=10):
        """检测摄像头
        
        Args:
            camera_id: 摄像头ID，默认为0（内置摄像头）
            conf_threshold: 置信度阈值
            save_path: 保存识别结果的路径
            max_save_count: 最大保存数量
            
        Returns:
            bool: 检测是否成功
        """
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            return False
        
        # 创建窗口
        cv2.namedWindow('YOLO Camera Detection')
        
        # 初始化保存计数
        save_count = 0
        
        # 记录上一次检测结果，用于判断是否有新内容
        last_detection = set()
        
        # 创建保存目录
        if save_path and not os.path.exists(save_path):
            os.makedirs(save_path)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            results = self.model(frame, conf=conf_threshold)
            annotated_frame = results[0].plot()
            
            # 保存识别结果
            if save_path and save_count < max_save_count:
                # 获取当前检测到的物体
                current_detection = set()
                for box in results[0].boxes:
                    cls = int(box.cls[0])
                    class_name = self.class_names[cls]
                    current_detection.add(class_name)
                
                # 检查是否有新内容（检测到的物体发生变化）
                if current_detection != last_detection:
                    # 生成保存文件名
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    save_filename = f"detection_{timestamp}.jpg"
                    save_filepath = os.path.join(save_path, save_filename)
                    
                    # 保存带标注的图像
                    cv2.imwrite(save_filepath, annotated_frame)
                    save_count += 1
                    print(f"保存识别结果 {save_count}/{max_save_count}: {save_filename}")
                    
                    # 更新上一次检测结果
                    last_detection = current_detection.copy()
            
            cv2.imshow('YOLO Camera Detection', annotated_frame)
            
            # 检查按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            
            # 检查窗口是否被关闭
            try:
                # 尝试获取窗口属性，如果窗口已关闭会抛出异常
                if cv2.getWindowProperty('YOLO Camera Detection', cv2.WND_PROP_VISIBLE) < 1:
                    break
            except:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        return True
    
    def draw_results(self, image, results):
        """在图像上绘制检测结果
        
        Args:
            image: 输入图像
            results: 检测结果
            
        Returns:
            numpy.ndarray: 绘制了检测结果的图像
        """
        for obj in results['objects']:
            bbox = obj['bbox']
            class_name = obj['class']
            confidence = obj['confidence']
            
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                image,
                f"{class_name}: {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )
        
        return image
    
    def detect_folder(self, folder_path, output_folder=None, conf_threshold=0.3):
        """批量检测文件夹中的图片和视频
        
        Args:
            folder_path: 文件夹路径
            output_folder: 输出文件夹路径
            conf_threshold: 置信度阈值
            
        Returns:
            dict: 检测结果统计
        """
         
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']  # 支持的图片格式
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']  # 支持的视频格式
        
        total_files = 0  # 总文件数
        detected_objects = 0  # 检测到的对象数
        results = {}  # 检测结果字典，键为文件名，值为检测到的对象列表或视频处理结果

        if output_folder and not os.path.exists(output_folder):  # 如果输出文件夹不存在
            print(f"创建输出文件夹: {output_folder}")
            os.makedirs(output_folder)  # 创建输出文件夹
        
        for root, dirs, files in os.walk(folder_path):  # 遍历文件夹中的所有文件
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in image_extensions:
                    total_files += 1
                    try:
                        result = self.detect_image(file_path, conf_threshold)
                        results[file] = result['objects']
                        detected_objects += len(result['objects'])
                        
                        if output_folder:
                            output_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_result.jpg")
                            cv2.imwrite(output_path, result['image'])
                    except Exception as e:
                        print(f"处理图片 {file} 时出错: {str(e)}")
                
                elif file_ext in video_extensions:
                    total_files += 1
                    try:
                        if output_folder:
                            output_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_result.avi")
                            self.detect_video(file_path, output_path, conf_threshold)
                        else:
                            self.detect_video(file_path, None, conf_threshold)
                        results[file] = "视频已处理"
                    except Exception as e:
                        print(f"处理视频 {file} 时出错: {str(e)}")
        
        return {
            "total_files": total_files,
            "detected_objects": detected_objects,
            "results": results
        }


if __name__ == "__main__":
    detector = YOLODetector()
    detector.detect_camera()

