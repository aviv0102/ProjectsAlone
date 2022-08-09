import {Address} from './address';

export class Student {
    name: string;
    age: number;
    address: Address;


    constructor(name: string, age: number, address: Address) {
        this.name = name;
        this.age = age;
        this.address = address;
    }
}
