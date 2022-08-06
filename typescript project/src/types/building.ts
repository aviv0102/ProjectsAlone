import {Point as Point, Itur} from './';

export class Building {
    polygon: Point[];
    score: number;
    iturim?: Itur[];

    constructor(polygon: Point[]) {
        this.polygon = polygon;
        this.score = 0;
    }
}
