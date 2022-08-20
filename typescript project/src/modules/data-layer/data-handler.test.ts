import { Item } from '../../types';
import { updateItem, getAll, getItem, items, cleanDictionary } from './data-handler';

function createItem(): Item {
    return {
        item_id: "305",
        price: 20,
        inventory: 5
    }
}

describe('tests for data-layer', () => {
    afterEach(() => cleanDictionary());

    test('When adding new item to data-layer', () => {
        updateItem(createItem());
        expect(items["305"].inventory).toBe(5);
        expect(items["305"].price).toBe(20);
    });

    test('When finding item in data-layer', () => {
        updateItem(createItem());
        expect(getItem("22")).toBe(undefined);
        expect(getItem("305").inventory).toBe(5);
        expect(getItem("305").price).toBe(20);
    });

    test('When getting all items in data-layer', () => {
        updateItem(createItem());
        const another = createItem();
        another.item_id = "2";
        updateItem(another);
        expect(getAll().length).toBe(2);
        expect(getAll()[0].item_id).toBe("2");
        expect(getAll()[1].item_id).toBe("305");
    });
})

