import random
from PyQt6.QtCore import QObject, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alpha = 255
        self.size = random.uniform(10, 20)
        self.velocity_y = random.uniform(-1, -3)
        self.velocity_x = random.uniform(-1, 1)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.alpha -= 5
        if self.alpha < 0:
            self.alpha = 0

class ParticleSystem(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.parent_widget = parent
        
    def spawn_particles(self, x, y, count=5):
        for _ in range(count):
            self.particles.append(Particle(x, y))
        if not self.timer.isActive():
            self.timer.start(30) # ~30fps
            
    def update_particles(self):
        active_particles = []
        for p in self.particles:
            p.update()
            if p.alpha > 0:
                active_particles.append(p)
                
        self.particles = active_particles
        if not self.particles:
            self.timer.stop()
            
        if self.parent_widget:
            self.parent_widget.update()
            
    def draw(self, painter: QPainter):
        for p in self.particles:
            # simple drawing of a heart using an ellipse and polygon or just a red circle for now
            # To keep it simple, we draw a pink circle to represent a generic particle
            painter.setPen(QColor(0, 0, 0, 0)) # No border
            painter.setBrush(QColor(255, 105, 180, int(p.alpha))) # Pink color
            painter.drawEllipse(QPointF(p.x, p.y), p.size / 2, p.size / 2)
