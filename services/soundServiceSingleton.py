from .soundService import soundService

class soundServiceSingleton:
    __instance = None

    def __new__(cls, frequency=1000, duration_ms=500):
        # Check if an instance already exists in memory
        if cls._instance is None:
            # If it doesn't exist, allocate memory for the ONE AND ONLY instance
            cls._instance = super(soundServiceSingleton, cls).__new__(cls)
            
            # Initialize the underlying soundService once
            cls._instance.service = soundService(frequency, duration_ms)
            
        # return the EXACT SAME instance stored in cls._instance
        return cls._instance

    # def __init__(self, frequency, duration_ms):
    #     # init singleton obj
    #     self.soundService = self._create_sound_service_instance(frequency, duration_ms)


    def _create_sound_service_instance(self, frequency, duration_ms):
        # singleton checks if soundService obj doesnt exist already
        if not self.soundService:
            self.soundService = soundService(frequency, duration_ms)


    def play_sound(self, frequency, duration_ms):
        self.soundService.play_sound(frequency, duration_ms)
        