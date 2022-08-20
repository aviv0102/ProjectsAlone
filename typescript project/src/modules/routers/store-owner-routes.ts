import express from 'express';
import { getInventoryRequest, setItemDetailsRequest, updateItemInventoryRequest } from '../controllers/store-owner-requests';

export const storeOwnerRouter = express.Router();

storeOwnerRouter.post('/items', setItemDetailsRequest);
storeOwnerRouter.post('/inventory', updateItemInventoryRequest);
storeOwnerRouter.get('/inventory', getInventoryRequest);

