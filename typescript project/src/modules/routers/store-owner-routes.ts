import express from 'express';
import { getInventory, setNewItem, updateItemInventory } from '../controllers/store-owner-requests';

export const storeOwnerRouter = express.Router();

storeOwnerRouter.post('/item', setNewItem);
storeOwnerRouter.post('/inventory', updateItemInventory);
storeOwnerRouter.get('/inventory', getInventory);

