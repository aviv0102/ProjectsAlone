export class SimpleObject <T>  {
    primitive : T;
    simpleObject : SimpleObject<T>;

    constructor(primitive: T, simpleObject:SimpleObject<T>) {
        this.primitive = primitive;
        this.simpleObject = simpleObject;
    }
}