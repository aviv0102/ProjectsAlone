import {Cluster, Constitution} from 'src/types';
import {CrossingResult} from '../cross-checker';

// export function getClusterGrade(constitution: Constitution, cluster: Cluster): CrossingResult {
//     const key = createKey(cluster);
//     const value = constitution[key];

//     // TODO validate value

//     const result = new CrossingResult(cluster, value.geographicScore, value.essenceScore);

//     return result;
// }

// function createKey(cluster: Cluster): string {
//     const {clusteringQuality, inBuildingQuality, stayingInterval,
//         numberOfBuildings} = cluster;

//     return clusteringQuality + ',' + inBuildingQuality + ',' +
//         stayingInterval?.minTimeinHours + '_to_' + stayingInterval?.maxTimeInHours +
//         ',' + numberOfBuildings;
// }
