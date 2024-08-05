import json
from functools import partial
from pystray import Icon, Menu, MenuItem
from custom_modules.config import load_settings, save_settings
from custom_modules.models import ModelManager
from custom_modules.audio import AudioManager
from custom_modules.ui import (
    create_image,
    set_temperature,
    set_prompt,
    set_model,
    setup,
    exit_action,
)
from custom_modules.speech import SpeechManager

# Load settings
settings = load_settings()

# Read API keys from file
with open("api_keys.txt", "r") as file:
    api_keys = json.load(file)

# Initialize managers
model_manager = ModelManager(api_keys)
audio_manager = AudioManager(model_manager.openai_client)

# Global variables
icon = None


def update_menu_status(icon):
    listen_status = "Stop Listening" if speech_manager.listening else "Start Listening"
    icon.menu = Menu(
        MenuItem(
            listen_status, lambda item: speech_manager.toggle_listening(icon, item)
        ),
        MenuItem(
            "Set Temperature",
            lambda: set_temperature(settings, save_settings, update_menu_status, icon),
        ),
        MenuItem(
            "Set Prompt",
            lambda: set_prompt(settings, save_settings, update_menu_status, icon),
        ),
        MenuItem(
            "Set Model",
            lambda: set_model(
                settings, save_settings, model_manager, update_menu_status, icon
            ),
        ),
        MenuItem("Exit", lambda: exit_action(icon, speech_manager.listening)),
    )


# Initialize SpeechManager after defining update_menu_status
speech_manager = SpeechManager(
    model_manager, audio_manager, settings, update_menu_status
)

if __name__ == "__main__":
    print("Starting AI Assistant application...")
    icon = Icon(
        "AI Assistant",
        create_image("red"),
        "AI Assistant",
        Menu(MenuItem("Placeholder", lambda: None)),
    )
    icon.run(partial(setup, update_menu_status=update_menu_status))
