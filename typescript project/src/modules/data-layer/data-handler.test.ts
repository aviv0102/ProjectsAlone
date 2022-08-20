import { Item } from '../../types';
import { updateItem, getAll, getItem } from './data-handler';

function createItem(): Item {
    return {
        item_id: "305",
        price: 20,
        inventory: 5
    }
}


test('When adding new item', () => {
    updateItem(createItem());
    expect(getAll().length).toBe(1);
    expect(getItem("305").inventory).toBe(5);
    expect(getItem("305").price).toBe(20);
});
