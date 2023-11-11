class Trail:
    trail_id: int
    x: int
    y: int
    point_index: int

    def __init__(self, trail_id: int, x: int, y: int, point_index: int) -> None:
        self.trail_id = trail_id
        self.x = x
        self.y = y
        self.point_index = point_index
