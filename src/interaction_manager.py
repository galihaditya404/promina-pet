from PyQt6.QtCore import QObject, QTimer

class InteractionManager(QObject):
    def __init__(self, animation_manager):
        super().__init__()
        self.animation_manager = animation_manager
        
        # Timers
        self.hover_timer = QTimer(self)
        self.hover_timer.setInterval(2000) # 2 seconds
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.trigger_happy_hover)
        
        self.sleep_timer = QTimer(self)
        self.sleep_timer.setInterval(15000) # 15 seconds (diturunkan agar lebih cepat bereaksi)
        self.sleep_timer.setSingleShot(True)
        self.sleep_timer.timeout.connect(self.trigger_sleep)
        
        self.petting_count = 0
        self.petting_timer = QTimer(self)
        self.petting_timer.setInterval(1000) # 1 second window for petting
        self.petting_timer.timeout.connect(self.reset_petting)
        
        # Start sleep timer initially
        self.reset_sleep_timer()
        
    def reset_sleep_timer(self):
        """Reset the sleep timer upon any interaction."""
        self.sleep_timer.start()
        if self.animation_manager.current_state == "sleep":
            self.animation_manager.set_state("idle")
            
    def on_mouse_enter(self):
        self.reset_sleep_timer()
        self.hover_timer.start()
        
    def on_mouse_leave(self):
        self.reset_sleep_timer()
        self.hover_timer.stop()
        if self.animation_manager.current_state == "happy":
            self.animation_manager.set_state("idle")
            
    def on_mouse_move(self):
        """Simulate petting based on frequent mouse movements over the pet."""
        self.reset_sleep_timer()
        self.petting_count += 1
        if not self.petting_timer.isActive():
            self.petting_timer.start()
            
        if self.petting_count > 15: # Arbitrary threshold for "petting"
            self.animation_manager.set_state("happy")
            self.petting_count = 0
            
    def on_mouse_click(self):
        self.reset_sleep_timer()
        self.animation_manager.set_state("love")
        # Revert to idle after a few seconds of love
        QTimer.singleShot(3000, lambda: self.animation_manager.set_state("idle") if self.animation_manager.current_state == "love" else None)
        
    def reset_petting(self):
        self.petting_count = 0
        self.petting_timer.stop()

    def trigger_happy_hover(self):
        """Trigger happy state after 2 seconds of hovering."""
        self.animation_manager.set_state("happy")
        
    def trigger_sleep(self):
        """Trigger sleep state after 60 seconds of inactivity."""
        self.animation_manager.set_state("sleep")

    # =================================================================
    # FUTURE INTEGRATIONS (Stubs)
    # =================================================================
    
    def on_teams_message(self):
        """Stub for Microsoft Teams integration. E.g. Pet brings an envelope."""
        pass
        
    def on_outlook_reminder(self):
        """Stub for Outlook Calendar integration. E.g. Pet points to a clock."""
        pass
        
    def on_company_announcement(self):
        """Stub for Company Announcements. E.g. Pet wears a tiny megaphone."""
        pass
        
    def on_ai_assistant_query(self):
        """Stub for AI Assistant integration. E.g. Pet shows thinking animation."""
        pass
