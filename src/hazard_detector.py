from ultralytics import YOLO
import cv2

class HazardDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """
        Initialize YOLOv8 model for hazard and object detection.
        Uses 'yolov8n.pt' (Nano) by default for speed.
        """
        # This will download the model if not present
        print(f"[INFO] Loading YOLO model: {model_path}...")
        self.model = YOLO(model_path)
        
        # COCO Class IDs
        self.TARGET_CLASSES = {
            0: 'person',
            15: 'cat',
            16: 'dog',
            43: 'knife',
            76: 'scissors'
            # Note: Firearms are not in default COCO. Requires custom training.
        }

    def detect_hazards(self, frame):
        """
        Run inference on a frame.
        Returns a dictionary of detections and the annotated frame.
        """
        results = self.model(frame, verbose=False, conf=0.4) # conf=0.4 threshold
        
        detections = {
            'person_count': 0,
            'weapons': [],
            'pets': [],
            'crowd_alert': False,
            'weapon_alert': False,
            'pet_alert': False
        }

        # Process results
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                if cls_id in self.TARGET_CLASSES:
                    class_name = self.TARGET_CLASSES[cls_id]
                    
                    if class_name == 'person':
                        detections['person_count'] += 1
                    
                    elif class_name in ['knife', 'scissors']:
                        detections['weapons'].append(class_name)
                        detections['weapon_alert'] = True
                    
                    elif class_name in ['cat', 'dog']:
                        detections['pets'].append(class_name)
                        detections['pet_alert'] = True

        # Crowd Logic
        if detections['person_count'] > 10:
            detections['crowd_alert'] = True

        return detections, results[0].plot() # .plot() returns BGR numpy array with boxes

