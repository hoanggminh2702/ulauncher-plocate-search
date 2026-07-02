from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import subprocess
import os

HOME = os.path.expanduser("~")

class FileSearchExtension(Extension):
    def __init__(self):
        super().__init__()
        self.recent_paths = []
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        if data.get("action") == "updatedb":
            subprocess.Popen(["updatedb"])
        elif data.get("action") == "open":
            path = data.get("path", "")
            if path:
                if path in extension.recent_paths:
                    extension.recent_paths.remove(path)
                extension.recent_paths.insert(0, path)
                extension.recent_paths = extension.recent_paths[:100]
                subprocess.Popen(["xdg-open", path])

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        is_dir_search = event.get_keyword() == extension.preferences.get("kw_dir", "fd")

        update_item = ExtensionResultItem(
            icon="icon.png",
            name="Update plocate database",
            description="Run updatedb to refresh file index",
            on_enter=ExtensionCustomAction({"action": "updatedb"}, keep_app_open=False)
        )

        if not query:
            return RenderResultListAction([update_item])

        limit = "100" if is_dir_search else "20"
        proc = subprocess.run(
            ["plocate", "-i", "--limit", limit, query],
            capture_output=True,
            text=True
        )
        all_lines = proc.stdout.strip().split("\n")

        if is_dir_search:
            filtered = [l for l in all_lines if l.strip() and os.path.isdir(l.strip())]
        else:
            filtered = [l for l in all_lines if l.strip()]

        recent = extension.recent_paths

        def sort_key(path):
            if path in recent:
                return (0, recent.index(path))
            if path.startswith(HOME):
                return (1, 0)
            return (2, 0)

        filtered.sort(key=sort_key)
        lines = filtered[:10]
        results = []

        for path in lines:
            results.append(
                ExtensionResultItem(
                    icon="icon.png",
                    name=os.path.basename(path),
                    description=path,
                    on_enter=ExtensionCustomAction({"action": "open", "path": path}, keep_app_open=False)
                )
            )

        if not results:
            results.append(update_item)

        return RenderResultListAction(results)

if __name__ == "__main__":
    FileSearchExtension().run()