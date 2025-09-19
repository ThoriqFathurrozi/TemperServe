import os
import logging
from flask import Flask, send_from_directory, render_template, abort
import watchdog
from core.watcher import monitor_path_with_debounce
import config
import threading

PORT = int(config.getConfig()["Server"]["Port"])
WATCH_DIR = (
    config.getConfig()["Paths"]["BaseDirectory"]
    + config.getConfig()["Paths"]["TargetDirectory"]
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
)

app = Flask(__name__)


@app.route("/", defaults={"req_path": ""})
@app.route("/<path:req_path>")
def dir_listing(req_path):
    abs_path = os.path.join(WATCH_DIR, req_path)

    if not os.path.exists(abs_path):
        return abort(404)

    # If it's a file, serve it directly
    if os.path.isfile(abs_path):
        return send_from_directory(
            os.path.dirname(abs_path), os.path.basename(abs_path)
        )

    # Show directory contents
    files = []
    for name in os.listdir(abs_path):
        path = os.path.join(req_path, name)
        link = "/" + path
        files.append((name, link))

    parent = None
    if req_path:
        parent = "/" + os.path.dirname(req_path)

    return render_template("index.html", files=files, path=req_path, parent=parent)


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        watchdog_thread = threading.Thread(
            target=monitor_path_with_debounce, args=(WATCH_DIR, True), daemon=True
        )
        watchdog_thread.start()
        logging.info("Watching directory: %s", WATCH_DIR)

    app.run(debug=True, port=PORT)
