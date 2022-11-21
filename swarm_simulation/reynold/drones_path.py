import random
from scipy.spatial import ConvexHull


class DronesPath:
    def __init__(self, id, canvas):
        self.id = id
        self.vertices = []
        self.canvas = canvas
        self.polygon = []
        self.point = (0,0)

    def click(self, c):
        self.vertices.append((c.x, c.y))
        if len(self.vertices) > 1:
            self.draw_path()

    def draw_path(self):

        # Antar bonden vet om den beste pathen for dronene a gjete sauene.
        p = []
        for point in self.vertices:    # Antar at punktene kommer i tupler
            p.append(point[0])
            p.append(point[1])
        self.canvas.create_line(p, fill='orange', tags=self.id)
        self.canvas.create_text(p[0], p[1], text='Start', tags=self.id)
        self.point = self.vertices[0]


