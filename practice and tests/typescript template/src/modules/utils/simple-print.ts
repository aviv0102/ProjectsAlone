
const isExist: any = {}

export function simplePrint(simpleObject: object, tabLength: string = ""): void {
    // @ts-ignore: Unreachable code error
    isExist[simpleObject] = true;

    console.log(tabLength + "Object:");
    console.log(tabLength + "----------------------------------------")
    tabLength = tabLength + '   ';

    if (!simpleObject) { throw (`got Null instead of simple object`) }



    // if (Object.keys(simpleObject).length === 0) { throw ('An Empty Object is not allowed') }


    for (const [prop, value] of Object.entries(simpleObject)) {

        if (!value) { throw ('An Empty attribute is not allowed') }

        if (typeof value == "string" || typeof value == "boolean" || typeof value == "number") {
            console.log(tabLength + prop + " = " + value)
        }

        else if (typeof value == "object") {
            console.log(tabLength + prop + " =\n")
            
            simplePrint(value, tabLength + "");
        }
        else {
            throw ('Not legal value')
        }
    }
}


