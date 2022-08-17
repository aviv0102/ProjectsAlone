import express from 'express';
import { Config } from '../../config/config';
import { sellerRouter } from '../routers/seller-routes';

export const Server = express();

export async function start(): Promise<void> {
    Server.use(sellerRouter);
    Server.listen(Config.port, () =>console.log("Server listening on PORT", Config.port));
}
