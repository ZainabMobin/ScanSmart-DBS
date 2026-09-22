from .soundService import soundService

class soundServiceSingleton:
    _instance = None

    def __new__(cls, frequency=1000, duration_ms=500):
        # Check if instance already exists in memory
        if cls._instance is None:
            # If it doesn't exist, allocate memory for the ONE AND ONLY instance
            cls._instance = super(soundServiceSingleton, cls).__new__(cls)
            # Initialize soundService once
            cls._instance.service = soundService(frequency, duration_ms)
            
        # return instance stored in cls._instance
        return cls._instance
    

    def play_sound(self):
        self.service.play_sound()
        