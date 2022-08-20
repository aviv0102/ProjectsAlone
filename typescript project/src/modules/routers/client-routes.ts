import express from 'express';
import { setNewItem } from '../controllers/store-owner-requests';

export const clientRouter = express.Router();

clientRouter.get('/about', setNewItem)