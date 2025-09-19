from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer
import time
from datetime import date
import os
import logging


def buildMetaVersion(version):
    today = date.today()
    timestamp = int(time.time())
    tracking_date = today.strftime("%Y%m%d")
    return f"{version}.{tracking_date}{timestamp}"


def checkFileExists(filename):
    return os.path.exists(filename)


def getFilenamePath(fullpath):
    if not os.path.exists(fullpath):
        return None
    root_path = os.path.dirname(fullpath)
    parent_path = f"/{root_path.split('/')[-1]}"
    filename = os.path.basename(fullpath)
    return root_path, parent_path, filename


def checkMetaFileJs(path, filename):
    meta_file_name = f"{filename.rsplit('.')[0]}.meta.js"
    meta_file_path = os.path.join(path, meta_file_name)
    user_script_meta = readUserScriptsMeta(os.path.join(path, filename))
    if not os.path.exists(meta_file_path) or user_script_meta is not None:
        with open(meta_file_path, "w") as f:
            if user_script_meta is not None:
                f.write(user_script_meta)
            else:
                logging.error(f"User script meta not found in {filename}")
    current_version = checkRealVersion(os.path.join(path, filename))
    version = buildMetaVersion(current_version)
    is_meta_change = changeVersionInMeta(meta_file_path, version)
    if is_meta_change:
        logging.warning(f"Updated meta file {meta_file_name}")


def readVersionFromFile(filename):
    if not checkFileExists(filename):
        return None
    with open(filename, "r") as f:
        content = f.read()
        # get current version
        currVersion = content.split("\n")
        currVersion = [line for line in currVersion if line.startswith("// @version")]
        currVersion = currVersion[0].split(" ")[-1] if currVersion else None
        if not currVersion:
            currVersion = "0.0.0"
        return currVersion


def checkRealVersion(filename):
    if not checkFileExists(filename):
        return None
    currVersion = readVersionFromFile(filename)
    currVersion = ".".join(currVersion.split(".")[:-1])
    if not currVersion:
        currVersion = "0.0.0"
    return currVersion


def changeVersionInMeta(fullpath, version):
    import re

    if not checkFileExists(fullpath):
        return False
    with open(fullpath, "r") as f:
        content = f.read()
        if content is None or content == "":
            return False
        new_content = re.sub(
            r"(// @version\s+)([^\s]+)",
            f"// @version      {version}",
            content,
        )

        if new_content != content and new_content != "":
            with open(fullpath, "w") as f:
                f.write(new_content)
                return True


def readUserScriptsMeta(fullpath):
    if not os.path.exists(fullpath):
        return None
    with open(fullpath, "r") as f:
        import re

        content = f.read()
        if not content:
            return None
        match = re.search(r"// ==UserScript==([\s\S]*?)// ==/UserScript==", content)
        if match:
            allow_params = ["name", "namespace", "version", "description", "author"]
            content = match.group(0)
            # remove some line that not contains allowParams
            lines = content.split("\n")
            lines = [
                line
                for line in lines
                if any(f"// @{param}" in line for param in allow_params)
            ]
            # ensure starts with // ==UserScript== and ends with // ==/UserScript==

            if lines[0].strip() != "// ==UserScript==":
                lines.insert(0, "// ==UserScript==")
            if lines[-1].strip() != "// ==/UserScript==":
                lines.append("// ==/UserScript==")
            content = "\n".join(lines)
            return content
    return None


def syncMetaFilesInDir(filenames, path):
    for filename in filenames:
        if filename.endswith("user.js") and not filename.endswith(".meta.js"):
            meta_filename = f"{filename.rsplit('.')[0]}.meta.js"
            main_path = os.path.join(path, filename)
            meta_path = os.path.join(path, meta_filename)
            main_version = readVersionFromFile(main_path)
            meta_version = readVersionFromFile(meta_path)
            if main_version != meta_version:
                logging.warning(
                    f"Version mismatch for {filename} - main version {main_version}, meta version {meta_version}. Syncing..."
                )
                is_main_change = changeVersionInMeta(main_path, meta_version)
                if is_main_change:
                    logging.warning(f"Updated main file version {filename}")


class DebouncedHandler(FileSystemEventHandler):
    filenames = []

    def __init__(self):
        self.timer = None

    def on_any_event(self, event):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(0.5, self.handle_event, args=[event])
        self.timer.start()

    def handle_event(self, event):
        if not event.is_directory and not event.src_path.endswith(".meta.js"):
            root_path, parent_path, filename = getFilenamePath(event.src_path)
            logging.info(f"Handled event for: {filename} Parent Path: {parent_path}")
            if filename not in self.filenames:
                self.filenames.append(filename)
            checkMetaFileJs(root_path, filename)
            syncMetaFilesInDir(self.filenames, root_path)

    def on_modified(self, event):
        self.on_any_event(event)


def monitor_path_with_debounce(path, recursive=False):
    handler = DebouncedHandler()
    observer = Observer()
    observer.schedule(handler, path=path, recursive=recursive)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
