import platform
import logging

logger = logging.getLogger(__name__)

class soundService:
    def __init__(self, frequency: int = 1000, duration_ms: int = 500):
        self.os_type = platform.system()
        logger.info("init SoundService on platform: {self.os_type}")
        self._init_sound_module()
        self.frequency = frequency
        self.duration_ms = duration_ms
        # linux specific audio generation
        self.sample_rate = 0
        self.wave = []


    def _init_sound_module(self):
        if self.os_type == "Windows":
            try:
                import winsound
                self.sound_module = winsound
            except ImportError:
                logger.warning("Failed to load winsound module")

        elif self.os_type == "Linux":
            try:
                import sounddevice
                self.sound_module = sounddevice

                self.sample_rate = 44100
                cycle_length = self.sample_rate / self.frequency

                # Standard CD quality sampling rate
                total_samples = int(self.sample_rate * (self.duration_ms / 1000))

                # Generate a square wave: 255 for the first half of a cycle, 0 for the second half
                self.wave = bytes(
                    255 if (i % cycle_length) < (cycle_length / 2) else 0 
                    for i in range(total_samples)
                )

            except (ImportError, OSError):
                logger.warning("Failed to load ossaudiodev module. Playing fallback sound")
                self._play_sound_fallback()
                


    def play_sound(self):
        if self.os_type == "Windows":
            self._play_sound_windows()
        elif self.os_type == "Linux":
            self._play_sound_linux()
        else:
            self._play_sound_fallback()


    def _play_sound_linux(self):
        # Play raw float audio array directly
        self.sound_module.play(self.wave, self.sample_rate)
        self.sound_module.wait()  # Block execution until the sound finishes playing


    def _play_sound_windows(self, frequency, duration_ms):
        # need to import relevant module, play sound via the self.soundModule
        self.sound_module.Beep(frequency, duration_ms)


    # Fallback for Docker / headless Linux environments (ASCII terminal bell)
    def _play_sound_fallback(self):
        print("\a", end="", flush=True)