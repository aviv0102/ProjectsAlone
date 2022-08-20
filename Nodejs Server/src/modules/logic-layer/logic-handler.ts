import { Item, ItemIds } from '../../types';
import * as DataLayer from '../data-layer/data-handler';



export async function newItemDetails(item_id: string, price: number): Promise<void> {

    const matchingItem = DataLayer.getItem(item_id);

    if (matchingItem) {
        matchingItem.price = price;
        DataLayer.updateItem(matchingItem);
    }
    else {
        const item: Item = {
            item_id,
            price,
            inventory: 0
        }

        DataLayer.updateItem(item);
    }
}


export async function updateItemInventory(item_id: string, amount: number, add: number): Promise<Item> {

    const matchingItem = DataLayer.getItem(item_id);

    if (amount) { matchingItem.inventory = amount; }
    else if (add) { matchingItem.inventory += add; }

    DataLayer.updateItem(matchingItem);

    return matchingItem;
}


export async function getMatchingItems(itemIds: ItemIds[]) : Promise<Item[]> {
    return DataLayer.findMatching(itemIds);
}


export async function getAllItems(): Promise<Item[]> {
    return DataLayer.getAll();
}


export async function isExist(item_id: string): Promise<boolean> {
    return DataLayer.getItem(item_id) ? true : false;
}




