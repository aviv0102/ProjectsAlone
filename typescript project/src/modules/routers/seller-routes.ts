import express from 'express';
import { setNewItem } from '../controllers/seller-controller';

export const sellerRouter = express.Router();

sellerRouter.get('/about', setNewItem)