import express from 'express';
import { Config } from '../../config/config';
import { clientRouter } from '../routers/client-routes';
import { storeOwnerRouter } from '../routers/store-owner-routes';

export const Server = express();

export async function start(): Promise<void> {
    Server.use(storeOwnerRouter);
    Server.use(clientRouter);
    Server.listen(Config.port, () => console.log("Server listening on PORT", Config.port));
}
