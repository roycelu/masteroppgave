
class DronesPath:
    def __init__(self, id):
        self.id = id
        self.path = []

    def draw_path(self, canvas, points):
        # Antar bonden vet om den beste pathen for dronene a gjete sauene.
        p = []
        self.path = points
        for point in points:    # Antar at punktene kommer i tupler
            p.append(point[0])
            p.append(point[1])
        canvas.create_line(p, fill='orange', tags=self.id)
        canvas.create_text(p[0], p[1], text='Start', tags=self.id)
        canvas.create_text(p[-2], p[-1], text='End', tags=self.id)

    def get_path(self):
        return self.path
