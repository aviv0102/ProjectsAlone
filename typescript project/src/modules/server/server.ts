// import {readClusters, readIturim, readConstitution} from '../data-providers';
// import {getClusterGrade} from '../grader';
// import {crossClusterWithIturim} from '../cross-checker';

import {currentConfig} from '../../config/config';

export async function start(): Promise<void> {
    console.log('this is a test');
    console.log(currentConfig);
    // const clusters = await readClusters();
    // const iturim = await readIturim();

    // const clustersWithIturim =
    //     clusters.map((cluster) => crossClusterWithIturim(cluster, iturim));

    // const results = clustersWithIturim.map((cluster) => getClusterGrade(constitution, cluster));

    // console.log(`there are ${results.length} results.`);
    // if (results.length > 0) {
    //     console.log(`first result: ${results[0]}
    //         with cluster id: ${results[0].cluster.id}
    //         with outputGeoValue ${results[0].outputGeoValue}
    //         with outputEssenceValue ${results[0].outputEssenceValue}`);
    // }
}
