import {Cluster} from 'src/types';

export class CrossingResult {
    cluster: Cluster;
    contextToProfession: boolean;
    outputGeoValue: string;
    outputEssenceValue: string;

    constructor(cluster: Cluster, outputGeoValue: string, outputEssenceValue: string) {
        this.cluster = cluster;
        this.outputGeoValue = outputGeoValue;
        this.outputEssenceValue = outputEssenceValue;

        // todo: handle contextToProfession
        this.contextToProfession = false;
    }
}
