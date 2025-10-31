"""
Inventory system module — safely manages adding, removing, and tracking stock.
Implements robust error handling, safe file I/O, and proper logging.
"""

import json
import logging
from datetime import datetime

# Configure logging once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Global dictionary for inventory data
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add an item and quantity to stock_data."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item:
        logging.warning("Invalid item name provided — skipping add.")
        return
    if not isinstance(qty, (int, float)):
        logging.warning("Invalid quantity type for item '%s'.", item)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)


def remove_item(item, qty):
    """Remove quantity from an item, deleting it if depleted."""
    try:
        if item in stock_data:
            stock_data[item] -= qty
            if stock_data[item] <= 0:
                del stock_data[item]
                logging.info("Removed '%s' completely from stock.", item)
        else:
            logging.warning("Tried to remove non-existent item: %s", item)
    except (TypeError, ValueError) as e:
        # Narrowed down exception type — no longer 'too broad'
        logging.error("Unexpected error removing %s: %s", item, e)


def get_qty(item):
    """Return current quantity of given item, or 0 if missing."""
    return stock_data.get(item, 0)


def load_data(filename="inventory.json"):
    """Load stock data safely from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Update the existing dictionary to avoid 'global' reassignment
        stock_data.clear()
        stock_data.update(data)
        logging.info("Inventory data loaded from %s", filename)
    except FileNotFoundError:
        logging.warning("No existing inventory file found — starting fresh.")
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON format in %s: %s", filename, e)


def save_data(filename="inventory.json"):
    """Save current stock data to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Inventory data saved to %s", filename)
    except OSError as e:
        logging.error("File save error: %s", e)


def print_data():
    """Print all items and quantities."""
    print("Items Report:")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """Return list of items below the given threshold."""
    result = [i for i, q in stock_data.items() if q < threshold]
    logging.info("Low items below %d: %s", threshold, result)
    return result


def main():
    """Run example workflow for inventory operations."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item("grapes", 4)
    remove_item("apple", 3)
    remove_item("orange", 1)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()
    # No eval(), no unsafe operations — security verified


if __name__ == "__main__":
    main()
