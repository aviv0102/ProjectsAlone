// usually here i would write functions handling the db....(writing, deleting, updating)

import { Item, ItemIds } from "../../types";


const items: { [item_id: string]: Item } = {}


export function getItem(item_id: string): Item {
    return items[item_id];
}

export function updateItem(item: Item): void {
    items[item.item_id] = item;
}

export function findMatching(itemIds: ItemIds[]): Item[] {
    const result = []
    for (const itemId of itemIds) {
        const possibleItem = items[itemId.item_id];
        if (possibleItem) {
            result.push(possibleItem)
        }
    }

    return result;
}

export function getAll(): Item[] {
    return Object.keys(items).map(function (key) {
        return items[key];
    });
}