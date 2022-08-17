import { findForMatchingSum } from "../utils/simple-function";

export async function start(): Promise<void> {

    const array = [1, 2 ,3 , 4 ,5]
    console.log(findForMatchingSum(array, 10))

}























//export type Link = { [path: string]: string[] }

// export async function getAll(): Promise<any> {

//     const buul = { a: 5, b: 2 }
//     const { a, b } = buul

//     for (const x in []) {

//     }

//     return []
// }

// function identity<Type>(arg: Type): Type {
//     return arg;
// }

//     rules.forEach((rule) => constitution[rule.key] = rule.value);

//     const points = positions.map((position) => new Point(position[0], position[1]));


//     const polygons = buildingsAsString
//         .split('\'')
//         .filter((stringShape) => stringShape.includes('POLYGON'))
//         .map(terraformer.parse)
//         .map(extractPoints)
//         .map((points) => new Building(points));


//    const cluster: Cluster = {            for interfaces
    //         id: element['ID'],
    //         clusteringQuality: element['hatzvara_quality'],
    //         identification: element['Identification'],
    //         stayingInterval: parsedStayingInterval,
    //         profession: element['profession'],
    //         numberOfBuildings: Number(element['number_of_buildings']),
    //         geoBuildings: buildings,
    //         inBuildingQuality: element['in_building_quality'],
    //     };