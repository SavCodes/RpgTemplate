class Quest:
    def __init__(self, title, description, objectives, reward):
        self.title = title
        self.description = description
        self.objectives = objectives  # List of objective descriptions
        self.progress = {objective: False for objective in objectives}  # Track completion of objectives
        self.completed = False
        self.reward = reward  # Can be items, experience points, etc.

    def update_progress(self, objective):
        """Mark an objective as complete"""
        if objective in self.objectives and not self.progress[objective]:
            self.progress[objective] = True
            if all(self.progress.values()):  # Check if all objectives are completed
                self.completed = True
                return True  # Quest completed
        return False

    def get_status(self):
        """Returns the current status of the quest"""
        if self.completed:
            return f"Quest '{self.title}' completed!"
        else:
            return f"Quest '{self.title}': {self.get_incomplete_objectives()}"

    def get_incomplete_objectives(self):
        """Returns a list of incomplete objectives"""
        return [obj for obj, status in self.progress.items() if not status]
