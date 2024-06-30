class Tooltipped:
    def set_scene(self, scene):
        self.scene = scene
        for child in self.children:
            if isinstance(child, Tooltipped):
                child.set_scene(scene)

        return self

    def set_tooltip(self, tooltip):
        if not self.scene:
            raise ValueError(f"No parent scene set for object {self!r}")

        self.scene.tooltip = tooltip
        self.scene.tooltip_of = self

    def remove_tooltip(self):
        self.scene.tooltip = None
        self.scene.tooltip_of = None
