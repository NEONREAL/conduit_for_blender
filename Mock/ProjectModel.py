from pathlib import Path

class Asset:
    def __init__(self, data: dict | None = None, name: str | None = None, tasks: list[str] | None = None):
        """
        Initialize an Asset either from a serialized dict or manually.
        - data: dict from serialize()
        - name + tasks: manual creation
        """
        if data is not None:
            self.name = data.get("name", "Unnamed")
            self.path = Path(data.get("path", self.name))
            self.tasks = [Task(path=self.path / t) for t in data.get("tasks", [])]
        else:
            if name is None:
                raise ValueError("Name must be provided if data is not used")
            self.name = name
            self.path = Path(name)
            self.tasks = [Task(path=self.path / t) for t in (tasks or [])]


class Task:
    def __init__(self, path: Path | str | None = None, data: dict | None = None):
        """
        Initialize a Task either from a Path or a serialized dictionary.
        - path: Path or string path to the task
        - data: dict from serialize()
        """
        if data is not None:

            self.path = Path(data.get("path", self.name))
        elif path is not None:
            self.path = Path(path)
            self.name = self.path.name
        else:
            raise ValueError("Either path or data must be provided")