# document/manager.py
import os
import json
from datetime import datetime


# =====================================================
# Storage Directory
# =====================================================
# We try multiple locations in order of preference.
# On Android, the app-specific directory is best (no permissions needed).

def _get_storage_dir():
    """Get the best storage directory for documents."""
    candidates = []

    # 1) Android app-specific external files dir (best, no permissions)
    try:
        from android.storage import app_storage_path
        base = app_storage_path()
        candidates.append(os.path.join(base, "documents"))
    except Exception:
        pass

    # 2) Kivy's user_data_dir (falls back if #1 fails)
    try:
        from kivy.app import App
        if App.get_running_app():
            base = App.get_running_app().user_data_dir
            candidates.append(os.path.join(base, "documents"))
    except Exception:
        pass

    # 3) Local relative directory (for desktop testing)
    candidates.append(os.path.join("data", "documents"))

    # Return the first candidate whose parent is writable
    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            test_file = os.path.join(path, ".write_test")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            print(f"[STORAGE] Using: {path}")
            return path
        except Exception:
            continue

    # If all fail, use the last one anyway
    print(f"[STORAGE] Fallback: {candidates[-1]}")
    return candidates[-1]


STORAGE_DIR = _get_storage_dir()


# =====================================================
# Document Manager
# =====================================================
class DocumentManager:
    """Manage document files (JSON format)."""

    # -----------------------------------------------------
    # File paths
    # -----------------------------------------------------
    @staticmethod
    def _path_for(doc_id):
        return os.path.join(STORAGE_DIR, f"{doc_id}.json")

    # -----------------------------------------------------
    # Save / Load / Delete
    # -----------------------------------------------------
    @staticmethod
    def save(doc_id, title, content, created=None):
        """
        Save a document.
        - doc_id: unique id (str). If None/empty, a new one is generated.
        - title: document title.
        - content: text content.
        - created: ISO string (kept on updates).
        Returns the doc_id.
        """
        if not doc_id:
            doc_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Ensure storage dir exists
        os.makedirs(STORAGE_DIR, exist_ok=True)

        # Preserve original created date on updates
        if created is None:
            existing = DocumentManager.load(doc_id)
            if existing:
                created = existing.get("created")
            else:
                created = datetime.now().isoformat()

        data = {
            "id": doc_id,
            "title": title or "Untitled",
            "content": content or "",
            "created": created,
            "updated": datetime.now().isoformat(),
        }

        path = DocumentManager._path_for(doc_id)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[SAVE] {path}")
            return doc_id
        except Exception as e:
            print(f"[SAVE ERROR] {e}")
            return None

    @staticmethod
    def load(doc_id):
        """Load a document by id. Returns dict or None."""
        if not doc_id:
            return None
        path = DocumentManager._path_for(doc_id)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[LOAD ERROR] {e}")
            return None

    @staticmethod
    def delete(doc_id):
        """Delete a document. Returns True/False."""
        if not doc_id:
            return False
        path = DocumentManager._path_for(doc_id)
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"[DELETE] {path}")
                return True
        except Exception as e:
            print(f"[DELETE ERROR] {e}")
        return False

    # -----------------------------------------------------
    # List documents
    # -----------------------------------------------------
    @staticmethod
    def list_all():
        """
        List all saved documents.
        Returns a list of dicts:
        [{
            "id": ...,
            "title": ...,
            "content": ...,        # optional, kept short
            "created": ...,
            "updated": ...,
        }, ...]
        Sorted by 'updated' desc.
        """
        docs = []
        if not os.path.isdir(STORAGE_DIR):
            return docs

        try:
            for fname in os.listdir(STORAGE_DIR):
                if not fname.endswith(".json"):
                    continue
                path = os.path.join(STORAGE_DIR, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    # Don't load huge content into the list
                    content = data.get("content", "")
                    preview = content[:80] + ("..." if len(content) > 80 else "")
                    docs.append({
                        "id": data.get("id", fname[:-5]),
                        "title": data.get("title", "Untitled"),
                        "preview": preview,
                        "created": data.get("created", ""),
                        "updated": data.get("updated", ""),
                    })
                except Exception as e:
                    print(f"[LIST] Skipping {fname}: {e}")
        except Exception as e:
            print(f"[LIST ERROR] {e}")

        # Sort by updated desc
        docs.sort(key=lambda d: d.get("updated", ""), reverse=True)
        return docs

    # -----------------------------------------------------
    # Utilities
    # -----------------------------------------------------
    @staticmethod
    def exists(doc_id):
        """Check if a document exists."""
        if not doc_id:
            return False
        return os.path.exists(DocumentManager._path_for(doc_id))

    @staticmethod
    def new_id():
        """Generate a new unique document id."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def storage_dir():
        """Return the current storage directory."""
        return STORAGE_DIR


# =====================================================
# Quick self-test (only when run directly)
# =====================================================
if __name__ == "__main__":
    print("=== Document Manager Self Test ===")
    print(f"Storage: {DocumentManager.storage_dir()}")

    # Save
    doc_id = DocumentManager.save(None, "Test Doc", "Hello World")
    print(f"Saved: {doc_id}")

    # Load
    doc = DocumentManager.load(doc_id)
    print(f"Loaded: {doc}")

    # List
    docs = DocumentManager.list_all()
    print(f"Found {len(docs)} document(s)")

    # Delete
    DocumentManager.delete(doc_id)
    print("Deleted")
