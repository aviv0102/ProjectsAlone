export class StayingInterval {
    minTimeinHours: number;
    maxTimeInHours?: number;

    constructor(minTimeinHours: number, maxTimeInHours?: number) {
        this.minTimeinHours = minTimeinHours;
        this.maxTimeInHours = maxTimeInHours;
    }
}
