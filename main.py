from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import subprocess
import os

class FileSearchExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        if data.get("action") == "updatedb":
            subprocess.Popen(["updatedb"])

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

        proc = subprocess.run(
            ["plocate", "-i", "--limit", "50", query],
            capture_output=True,
            text=True
        )
        all_lines = proc.stdout.strip().split("\n")

        if is_dir_search:
            filtered = [l for l in all_lines if l.strip() and os.path.isdir(l.strip())]
        else:
            filtered = [l for l in all_lines if l.strip()]

        lines = filtered[:10]
        results = []

        for path in lines:
            results.append(
                ExtensionResultItem(
                    icon="icon.png",
                    name=os.path.basename(path),
                    description=path,
                    on_enter=OpenAction(path)
                )
            )

        if not results:
            results.append(update_item)

        return RenderResultListAction(results)

if __name__ == "__main__":
    FileSearchExtension().run()