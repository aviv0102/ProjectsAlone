import { Link } from "Links";

export async function WriteResults(results: Link[]) {
    // here i would write to a db the results...
    console.log('Writing to the fake db:')
    console.log(results)
}