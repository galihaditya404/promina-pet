import os
import re
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, QObject, pyqtSignal

def natural_sort_key(s):
    """Fungsi untuk mengurutkan nama file secara natural (frame_2 sebelum frame_10)"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

class AnimationManager(QObject):
    frame_updated = pyqtSignal(QPixmap)
    
    def __init__(self, base_asset_path="assets"):
        super().__init__()
        
        # Selalu gunakan path absolut ke folder assets berdasarkan lokasi file ini
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_asset_path = os.path.join(project_root, base_asset_path)
        
        self.frames = {
            "idle": [],
            "happy": [],
            "love": [],
            "sleep": []
        }
        self.current_state = "idle"
        self.current_frame_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        
        self.load_assets()
        # Set animation speed to 40ms (25 FPS) untuk 24 frame yang sangat smooth
        self.timer.start(40)
        
    def load_assets(self):
        """Loads PNG assets for each state into memory."""
        for state in self.frames.keys():
            state_dir = os.path.join(self.base_asset_path, state)
            if os.path.exists(state_dir):
                # Gunakan natural_sort_key agar frame_10.png tidak berada di atas frame_2.png
                files = sorted([f for f in os.listdir(state_dir) if f.endswith('.png')], key=natural_sort_key)
                for file in files:
                    pixmap = QPixmap(os.path.join(state_dir, file))
                    if not pixmap.isNull():
                        self.frames[state].append(pixmap)
                        
        # Provide fallback if no frames loaded
        for state in self.frames.keys():
            if not self.frames[state]:
                print(f"Warning: No frames found for state '{state}'. Using empty pixmap.")
                self.frames[state].append(QPixmap(150, 150))
                
    def set_state(self, new_state):
        if new_state in self.frames and self.current_state != new_state:
            self.current_state = new_state
            self.current_frame_index = 0
            
    def update_frame(self):
        state_frames = self.frames[self.current_state]
        if not state_frames:
            return
            
        # Karena Anda membuat 24 frame (animasi utuh), kita kembali gunakan putaran normal
        # agar animasinya berputar dari frame 1 ke 24 lalu kembali ke 1.
        self.current_frame_index = (self.current_frame_index + 1) % len(state_frames)
                
        pixmap = state_frames[self.current_frame_index]
        self.frame_updated.emit(pixmap)

