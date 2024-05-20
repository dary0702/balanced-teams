class Player:
    def __init__(
        self,
        name: str,
        rating: float,
        intensity: float,
        position: str,
        is_base: bool,
    ):
        self.name = name
        self.rating = rating
        self.intensity = intensity
        self.position = position
        self.is_base = is_base
