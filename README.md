# Corporate Desktop Pet Companion 🐾

A premium, interactive desktop pet application built with Python and PyQt6. This app creates a frameless, transparent, "always-on-top" companion that lives on your screen, responding to your mouse interactions and keeping you company while you work.

## ✨ Features

*   **Frameless & Transparent Window:** Integrates seamlessly into your desktop environment.
*   **Always On Top:** Your companion is always visible, hovering above other applications.
*   **High-Quality Animation System:** Supports up to 24-frame, 25 FPS buttery-smooth sprite sheet animations. Features "natural sorting" so frame files (`frame_1.png` to `frame_24.png`) load in the exact correct sequence.
*   **Interactive Emotional States:**
    *   **Idle:** Default breathing/idling animation.
    *   **Happy:** Triggered by hovering the mouse over the pet for 2 seconds, or by "petting" (wiggling the mouse over the character).
    *   **Love:** Click the pet to trigger the Love state, complete with a custom floating pink heart particle effect!
    *   **Sleep:** If left alone for 15 seconds, the pet dozes off to save energy.
*   **Draggable:** Click and drag to move the pet anywhere on your screen.
*   **Persistent Location:** Automatically saves its screen coordinates upon exit, so it spawns exactly where you left it next time.
*   **Anti-Aliased Rendering:** Uses smooth pixmap transformations for premium image quality without pixelation.

## 🛠️ Tech Stack

*   Python 3
*   PyQt6

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd desktop_pet
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python src/main.py
   ```

## 🎨 Adding Your Own Animations

You can completely customize the pet by replacing the images in the `assets/` directory.

1. Create a series of transparent `.png` frames for your character's animations.
2. Name them sequentially (e.g., `frame_1.png`, `frame_2.png`, ... `frame_24.png`).
3. Place them in the corresponding folder:
   *   `assets/idle/`
   *   `assets/happy/`
   *   `assets/love/`
   *   `assets/sleep/`

*Note: If no images are provided, the app will fall back to using transparent placeholders to prevent crashing.*

## 📂 Project Structure

```text
desktop_pet/
│
├── assets/                  # Animation frames (idle, happy, love, sleep)
├── config/                  # Configuration files (settings.json stores screen X/Y)
├── src/
│   ├── main.py              # Application entry point
│   ├── pet_window.py        # Core UI, transparent window, dragging logic
│   ├── animation_manager.py # Loads PNGs and runs the 25fps timer loop
│   ├── interaction_manager.py # Handles hover, click, petting, and sleep logic
│   └── particle_system.py   # Spawns and animates floating hearts on click
├── requirements.txt         # Python dependencies
└── README.md                # You are here!
```

## 🔮 Future Integrations (Prepared Stubs)

The `InteractionManager` contains code stubs ready to be hooked into external APIs for:
*   Microsoft Teams notifications.
*   Outlook Calendar event reminders.
*   Company-wide announcements.
*   AI Assistant queries.
