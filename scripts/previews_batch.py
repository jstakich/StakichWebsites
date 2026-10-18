import json
from pathlib import Path
BATCH = json.loads(Path(__file__).with_name('previews_batch.json').read_text())
