"""
Cross-platform safe audio playback utility.
"""
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


class SoundManager:
    """Manages sound effects with mute toggle and safe fallbacks."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled and HAS_WINSOUND

    def toggle(self) -> bool:
        self.enabled = not self.enabled and HAS_WINSOUND
        return self.enabled

    def play(self, sound_name: str) -> None:
        if not self.enabled:
            return
        try:
            if sound_name == "success":
                winsound.Beep(880, 90)
                winsound.Beep(1175, 110)
            elif sound_name == "error":
                winsound.Beep(260, 160)
            elif sound_name == "tick":
                winsound.Beep(650, 40)
            elif sound_name == "game_over":
                winsound.Beep(523, 140)
                winsound.Beep(392, 170)
                winsound.Beep(330, 240)
        except Exception:
            pass

