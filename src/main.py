import sys
import os

# Menambahkan path project root ke sys.path agar import 'src' bisa berjalan dari mana saja
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from src.pet_window import PetWindow

def main():
    # Initialize the PyQt Application
    app = QApplication(sys.argv)
    
    # Create and show the desktop pet window
    pet = PetWindow(config_path="config/settings.json")
    pet.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
