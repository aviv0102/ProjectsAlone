import express from 'express';
import { setItemDetailsRequest } from '../controllers/store-owner-requests';

export const clientRouter = express.Router();

clientRouter.get('/about', setItemDetailsRequest)