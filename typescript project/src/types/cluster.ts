import {Building} from './';
import {StayingInterval} from './staying-interval';

export interface Cluster {
    id: string;
    clusteringQuality: string;
    identification: string;
    stayingInterval?: StayingInterval;
    profession: string;
    numberOfBuildings: number;
    geoBuildings: Building[];
    inBuildingQuality: string;
}
