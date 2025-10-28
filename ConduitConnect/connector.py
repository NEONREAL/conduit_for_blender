from ..Mock import Asset, Task
import requests

class Connector():
    def __init__(self):
        self.active = False
        if self.get("/"):
            self.active = True
        pass

    def get(self, command: str) -> dict | None:
        self.server = "http://127.0.0.1:8000/"
        res = requests.get(f"{self.server}{command}")
        return res.json()
    
    def get_asset(self) -> Asset | None:
        data = self.get("asset")
        if data:
            new_asset = Asset(data)
            print(new_asset.name)
            for task in new_asset.tasks:
                print(task.path)
            return new_asset
        else:
            return None
    
    def get_selected_task(self) -> Task | None:
        data = self.get("task")
        if data:
            new_task = Task(data=data)
            return new_task
        else:
            return None


