import json
import os

def fix_string(s: str) -> str:
    try:
        return s.encode("latin1").decode("utf-8")
    except Exception:
        return s

def fix_obj(obj):
    if isinstance(obj, dict):
        return {k: fix_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [fix_obj(v) for v in obj]
    if isinstance(obj, str):
        return fix_string(obj)
    return obj

def process_json_file(path: str):
    print(f"Fixing {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    data = json.loads(raw)

    fixed = fix_obj(data)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(fixed, f, ensure_ascii=False, indent=2)

def walk_and_fix(root: str):
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.lower().endswith(".json"):
                full = os.path.join(dirpath, name)
                process_json_file(full)

if __name__ == "__main__":
    walk_and_fix("your_instagram_activity")
