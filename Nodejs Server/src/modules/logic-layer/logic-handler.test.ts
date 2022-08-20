import { Item } from '../../types';
import { items, cleanDictionary } from '../data-layer/data-handler';
import { newItemDetails, updateItemInventory, getMatchingItems, isExist } from './logic-handler';

function createItem(): Item {
    return {
        item_id: "305",
        price: 20,
        inventory: 5
    }
}


describe('tests for logic-layer', () => {
    afterEach(() => cleanDictionary());
    
    test('When using newItemDetails expect the add new item or update current one', async () => {
        const item = createItem();
        await newItemDetails(item.item_id, item.price);
        expect(items["305"].inventory).toBe(0);
        expect(items["305"].price).toBe(20);

        await newItemDetails(item.item_id, 5);
        expect(items["305"].price).toBe(5);

    });


    test('When using updateInventory expect the add or change inventory', async () => {
        const item = createItem();
        await newItemDetails(item.item_id, item.price);
        expect(items["305"].inventory).toBe(0);
        expect(items["305"].price).toBe(20);

        //@ts-ignore
        const undefinedAmount: number = undefined;
        await updateItemInventory(item.item_id, undefinedAmount, 4)
        expect(items["305"].inventory).toBe(4);


        //@ts-ignore
        const undefinedAdd: number = undefined;
        await updateItemInventory(item.item_id, 2, undefinedAdd)
        expect(items["305"].inventory).toBe(2);
    });


    test('When using findMatching expect the find matching items', async () => {
        await newItemDetails("300", 2);
        await newItemDetails("301", 3.14);

        let result = await getMatchingItems([{ "item_id": "300" }]);
        expect(result.length).toBe(1);
        expect(result[0].item_id).toBe("300");

        result = await getMatchingItems([{ "item_id": "300" }, { "item_id": "301" }]);
        expect(result.length).toBe(2);
        expect(result[1].item_id).toBe("301");
    });


    test('When using isExist expect the find matching items', async () => {
        await newItemDetails("300", 2);
        await newItemDetails("301", 3.14);

        let result = await isExist("300");
        expect(result).toBe(true);

        result = await isExist("305");
        expect(result).toBe(false);
    })

})
