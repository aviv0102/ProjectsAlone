
export function findForMatchingSum(array: number[], sum: number): number[] {
    const hash: any = {}

    // if(!array || typeof array !== 'number[]') {}

    for (const k in array) { hash[k] = true }


    for (const potentialPartOfSum of array) {
        const otherNumberToFind = sum - potentialPartOfSum;

        if (hash[otherNumberToFind]) {
            return [otherNumberToFind, potentialPartOfSum];
        }
    }

    return []
}


export function findMatchingTriplets(array: number[], sum: number): number[] {

    for (const potentialPartOfSum of array) {
        const potentialSum = sum - potentialPartOfSum;
        const arrayWithoutOurNumber = array.splice(array.indexOf(potentialPartOfSum), 1);
        const potentialArray: number[] = findForMatchingSum(arrayWithoutOurNumber, potentialSum);
        
        if (potentialArray.length) {
            potentialArray.push(potentialPartOfSum);
            return potentialArray
        }
    }

    return []

}