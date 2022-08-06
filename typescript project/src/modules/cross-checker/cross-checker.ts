// import {isPointInPolygon} from 'geolib';

// import {Cluster, Itur, Point, Building} from 'src/types';

// export function crossClusterWithIturim(cluster: Cluster, iturim: Itur[]): Cluster {
//     for (const building of cluster.geoBuildings) {
//         const relevantIturim = getIturimInsidePolygon(iturim, building.polygon);
//         if (!relevantIturim || relevantIturim.length === 0) {
//             continue;
//         }

//         building.iturim = relevantIturim;
//         building.score = 1;
//         building.score += getCrossIdentificationFactor(cluster.identification, building);
//     }

//     return cluster;
// }

// function getIturimInsidePolygon(iturim: Itur[], polygon: Point[]): Itur[] | undefined {
//     if (!polygon || polygon.length < 3) {
//         console.error(`can't search for iturim inside polygon: ${polygon}`);
//         return undefined;
//     }

//     // IMPORTANT!!! itur.location must have properies with the name 'longitude' and
//     // 'latitude', since 'isPointInPolygon' requires it.
//     // TODO: wrap it in function that builds a point for the library.
//     return iturim.filter((itur) => isPointInPolygon(itur.location, polygon));
// }


// function getCrossIdentificationFactor(clusterIdentification: string, building: Building): number {
//     const iturim = building.iturim;
//     if (!iturim || iturim.length == 0) {
//         return 0;
//     }

//     const crossFound = iturim.some((itur) => itur.tabuOwner === clusterIdentification);
//     const factor = crossFound ? 1 : -1;
//     return factor;
// }
