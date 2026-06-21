import os
import json
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPixmap

from src.animation_manager import AnimationManager
from src.interaction_manager import InteractionManager
from src.particle_system import ParticleSystem

class PetWindow(QWidget):
    def __init__(self, config_path="config/settings.json"):
        super().__init__()
        self.config_path = config_path
        self.drag_position = QPoint()
        
        self.init_ui()
        self.init_systems()
        self.load_position()
        
    def init_ui(self):
        # Set window flags to make it frameless and stay on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        # Make the background transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Aktifkan pelacakan pergerakan mouse agar fitur 'petting' bekerja
        self.setMouseTracking(True)
        
        # Set a fixed size based on expected sprite size
        self.setFixedSize(200, 200)
        
    def init_systems(self):
        self.current_pixmap = None
        
        self.animation_manager = AnimationManager()
        self.animation_manager.frame_updated.connect(self.update_sprite)
        
        self.interaction_manager = InteractionManager(self.animation_manager)
        self.particle_system = ParticleSystem(parent=self)
        
    def load_position(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    x = data.get("position_x", 100)
                    y = data.get("position_y", 100)
                    self.move(x, y)
            except Exception as e:
                print(f"Failed to load settings: {e}")
                self.move(100, 100)
        else:
            self.move(100, 100)
            
    def save_position(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        try:
            with open(self.config_path, 'w') as f:
                json.dump({
                    "position_x": self.pos().x(),
                    "position_y": self.pos().y()
                }, f)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def update_sprite(self, pixmap: QPixmap):
        self.current_pixmap = pixmap
        self.update() # triggers paintEvent
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        if self.current_pixmap and not self.current_pixmap.isNull():
            # Draw sprite centered
            x = (self.width() - self.current_pixmap.width()) // 2
            y = (self.height() - self.current_pixmap.height()) // 2
            painter.drawPixmap(x, y, self.current_pixmap)
            
        # Draw particles on top of the sprite
        self.particle_system.draw(painter)
        
    # Mouse interaction overrides
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.interaction_manager.on_mouse_click()
            # Spawn particles near the center
            self.particle_system.spawn_particles(self.width() / 2, self.height() / 2, count=8)
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            # Dragging the window
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
        else:
            # Hover movement inside widget
            self.interaction_manager.on_mouse_move()

    def enterEvent(self, event):
        self.interaction_manager.on_mouse_enter()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.interaction_manager.on_mouse_leave()
        super().leaveEvent(event)
        
    def closeEvent(self, event):
        self.save_position()
        super().closeEvent(event)
