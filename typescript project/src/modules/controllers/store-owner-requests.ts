import { Request, Response } from "express";
import { ItemIds } from "../../types";
import * as LogicLayer from "../logic-layer/logic-handler";


export async function setItemDetailsRequest(request: Request, response: Response) {
    try {
        const { username, item_id, price } = request.body;

        if (!username || !item_id || !price || item_id == '') {
            response.status(400).send('Missing fields username or item_id or price in request body');
        }

        else if (typeof (username) !== 'string' || typeof (item_id) !== 'string' || typeof (price) !== 'number') {
            response.status(400).send('One of field types is illegal');
        }

        else if (username !== 'admin') {
            response.status(401).send('User must be admin in order to place item on store');
        }

        else {
            await LogicLayer.newItemDetails(item_id, price);
            response.send(`Item details were changed.`);
        }

    } catch (errror) { console.log(`an error occured within setNewItem function`) }
}



export async function updateItemInventoryRequest(request: Request, response: Response) {
    try {
        const { username, item_id, amount, add } = request.body;

        if (!username || !item_id || (!add && !amount)) {
            response.status(400).send('Missing fields username or item_id or amount/add in request body');
        }

        else if (typeof (username) !== 'string' || typeof (item_id) !== 'string' || (typeof (add) !== 'number' && typeof (amount) !== 'number')) {
            response.status(400).send('One of field types is illegal');
        }

        else if (!await LogicLayer.isExist(item_id)) {
            response.status(400).send('Item does not exist');
        }

        else if (username !== 'admin') {
            response.status(401).send('User must be admin in order to change the store');
        }

        else {
            const result = await LogicLayer.updateItemInventory(item_id, amount, add);
            response.send(`Item inventory was changed. ${JSON.stringify(result)}`);
        }


    } catch (errror) { console.log(`an error occured within update inventory function`) }
}



export async function getInventoryRequest(request: Request, response: Response) {
    try {
        const { username, items } = request.body;

        if (!username || typeof (username) !== 'string') {
            response.status(400).send('Missing username field or illegal field type');
        }

        else if (username !== 'admin') {
            response.status(401).send('User must be admin in order to get items on store');
        }

        else if (items) {
            const exist = await validateItems(items);
            if (!exist) { response.status(400).send('Unvalid item ids'); }

            const result = await LogicLayer.getMatchingItems(items);
            response.send(result);
        }

        else {
            const result = await LogicLayer.getAllItems();
            response.send(result);
        }


    } catch (errror) { console.log(`an error occured within getInventory function`) }
}


async function validateItems(items: ItemIds[]): Promise<boolean> {

    if (!items.length) { return false }

    for (const item of items) {
        if (!item.item_id) { return false }

        if (!await LogicLayer.isExist(item.item_id)) { return false }

    }

    return true
}