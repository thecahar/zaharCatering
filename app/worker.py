import threading
import time
import datetime
import uuid

STORAGE = {
    "delivery": []
}

def add_item(item):
    now = datetime.datetime.now()
    item_id = str(uuid.uuid4())
    STORAGE["delivery"].append({
        "id": item_id,
        "item": item,
        "status": "active",
        "updated_at": now
    })
    print(f"Added: {item_id}, status=active")
    return item_id

def archive_item(item_id):
    for item in STORAGE["delivery"]:
        if item["id"] == item_id:
            item["status"] = "archived"
            item["updated_at"] = datetime.datetime.now()
            print(f"Archived: {item_id}")
            return
    print(f"Item with ID {item_id} not found.")

def cleanup_worker():
    while True:
        time.sleep(10)
        now = datetime.datetime.now()
        for item in STORAGE["delivery"][:]:
            if item["status"] == "archived" and (now - item["updated_at"]).total_seconds() > 60:
                STORAGE["delivery"].remove(item)
                print(f"Removed archived item: {item['id']}")

def main():

    worker_thread = threading.Thread(target=cleanup_worker, daemon=True)
    worker_thread.start()

    item1 = add_item("Pizza")
    time.sleep(2)
    item2 = add_item("Burger")

    time.sleep(3)
    archive_item(item1)

    time.sleep(70)


if __name__ == "__main__":
    main()
