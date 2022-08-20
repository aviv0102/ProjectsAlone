import { Request, Response } from "express";


export async function setNewItem(_request: Request, response: Response) {

    response.send('were here');

}

export async function updateItemInventory(_request: Request, response: Response) {
    response.send('were here');
}

export async function getInventory(_request: Request, response: Response) {
    response.send('were here');
}