import {Cluster, Point, Itur, Building} from './types';
import {crossClusterWithIturim} from './modules/cross-checker';

function createIturExample(points: Point): Itur {
    return {
        index: 123,
        location: points,
        profession: 'assassin',
        tabuOwner: 'moshe',
        names: 'bla',
    };
}

function createClusterExample(geoBuildings: Building[]): Cluster {
    return {
        id: 'clusterTest1',
        clusteringQuality: 'low',
        identification: 'sdsds',
        stayingInterval: {minTimeinHours: 2, maxTimeInHours: 3},
        profession: 'wizard',
        numberOfBuildings: 1,
        geoBuildings: geoBuildings,
        inBuildingQuality: '',
    };
};

test('Set1: basic itur inside cluster', () => {
    const point1 = new Point(31.3018, 34.2754);
    const point2 = new Point(31.3011, 34.2754);
    const point3 = new Point(31.3012, 34.2746);
    const building = new Building([point1, point2, point3]);
    const cluster = createClusterExample([building]);

    const itur = createIturExample({latitude: 31.3016, longitude: 34.2752});
    const crossBuildings = crossClusterWithIturim(cluster, [itur]).geoBuildings;

    expect(crossBuildings.length).toBe(1);
    expect(crossBuildings[0].iturim ? crossBuildings[0].iturim.length : -1).toBe(1);
    expect(crossBuildings[0].polygon.length).toBe(3);
    expect(crossBuildings[0].iturim ? crossBuildings[0].iturim[0].location.latitude : -1).toBe(31.3016);
});

test('Set1: basic itur not inside cluster', () => {
    const point1 = new Point(31.3018, 34.2754);
    const point2 = new Point(31.3011, 34.2754);
    const point3 = new Point(31.3012, 34.2746);
    const building = new Building([point1, point2, point3]);
    const cluster = createClusterExample([building]);

    const itur = createIturExample({latitude: 38.8888, longitude: 34.2752});
    const crossBuildings = crossClusterWithIturim(cluster, [itur]).geoBuildings;

    expect(crossBuildings.length).toBe(1);
    expect(crossBuildings[0].iturim ? 1 : 0).toBe(0);
    expect(crossBuildings[0].polygon.length).toBe(3);
});

test('Set2: itur with 2 buildings when in the second one', () => {
    const point1 = new Point(31.3029, 34.2731);
    const point2 = new Point(31.3017, 34.2729);
    const point3 = new Point(31.3023, 34.2740);
    const point4 = new Point(31.3018, 34.2754);
    const point5 = new Point(31.3011, 34.2754);
    const point6 = new Point(31.3012, 34.2746);

    const building1 = new Building([point1, point2, point3]);
    const building2 = new Building([point4, point5, point6]);
    const cluster = createClusterExample([building1, building2]);

    const itur = createIturExample({latitude: 31.3016, longitude: 34.2752});
    const crossBuildings = crossClusterWithIturim(cluster, [itur]).geoBuildings;

    expect(crossBuildings.length).toBe(2);
    expect(crossBuildings[0].iturim ? 1 : 0).toBe(0);
    expect(crossBuildings[0].polygon.length).toBe(3);
    expect(crossBuildings[1].polygon.length).toBe(3);
    expect(crossBuildings[1].iturim ? 1 : 0).toBe(1);
    expect(crossBuildings[1].iturim ? crossBuildings[1].iturim[0].location.latitude : 0).toBe(31.3016);
});

test('Set2: itur that does not appear in both buildings', () => {
    const point1 = new Point(31.3029, 34.2731);
    const point2 = new Point(31.3017, 34.2729);
    const point3 = new Point(31.3023, 34.2740);
    const point4 = new Point(31.3018, 34.2754);
    const point5 = new Point(31.3011, 34.2754);
    const point6 = new Point(31.3012, 34.2746);

    const building1 = new Building([point1, point2, point3]);
    const building2 = new Building([point4, point5, point6]);
    const cluster = createClusterExample([building1, building2]);

    const itur = createIturExample({latitude: 33.3016, longitude: 34.2752});
    const crossBuildings = crossClusterWithIturim(cluster, [itur]).geoBuildings;

    expect(crossBuildings.length).toBe(2);
    expect(crossBuildings[0].iturim ? 1 : 0).toBe(0);
    expect(crossBuildings[1].iturim ? 1 : 0).toBe(0);
});

test('Set3: changing location , few iturim , polygon have 4 points', () => {
    const point1 = new Point(32.071341, 34.805351);
    const point2 = new Point(32.071382, 34.805109);
    const point3 = new Point(32.071223, 34.805077);
    const point4 = new Point(32.071164, 34.805324);
    const building = new Building([point1, point2, point3, point4]);
    const cluster = createClusterExample([building]);

    const firstItur = createIturExample({latitude: 32.071291, longitude: 34.805200}); // inside poly
    const secondItur = createIturExample({latitude: 31.30161, longitude: 34.2752}); // not inside
    const crossBuildings = crossClusterWithIturim(cluster, [firstItur, secondItur]).geoBuildings;

    expect(crossBuildings.length).toBe(1);
    expect(crossBuildings[0].iturim ? crossBuildings[0].iturim.length : -1).toBe(1);
    expect(crossBuildings[0].polygon.length).toBe(4);
    expect(crossBuildings[0].iturim ? crossBuildings[0].iturim[0].location.latitude : -1).toBe(32.071291);
});


test('Set4: few iturim inside the same building', () => {
    const point1 = new Point(32.071341, 34.805351);
    const point2 = new Point(32.071382, 34.805109);
    const point3 = new Point(32.071223, 34.805077);
    const point4 = new Point(32.071164, 34.805324);
    const building = new Building([point1, point2, point3, point4]);
    const cluster = createClusterExample([building]);

    const firstItur = createIturExample({latitude: 32.071291, longitude: 34.805200});
    const secondItur = createIturExample({latitude: 32.071273, longitude: 34.805088});
    const thirdItur = createIturExample({latitude: 32.071218, longitude: 34.805313});
    const fourthItur = createIturExample({latitude: 32.071332, longitude: 34.805222});
    const crossBuildings = crossClusterWithIturim(
            cluster,
            [firstItur, secondItur, thirdItur, fourthItur],
    ).geoBuildings;

    expect(crossBuildings.length).toBe(1);
    expect(crossBuildings[0].iturim ? crossBuildings[0].iturim.length : -1).toBe(4);
    expect(crossBuildings[0].polygon.length).toBe(4);
});

test('Set4: few iturim outside the building none should be considered', () => {
    const point1 = new Point(32.071341, 34.805351);
    const point2 = new Point(32.071382, 34.805109);
    const point3 = new Point(32.071223, 34.805077);
    const point4 = new Point(32.071164, 34.805324);
    const building = new Building([point1, point2, point3, point4]);
    const cluster = createClusterExample([building]);

    const firstItur = createIturExample({latitude: 32.071405, longitude: 34.804975});
    const secondItur = createIturExample({latitude: 32.071195, longitude: 34.804964});
    const thirdItur = createIturExample({latitude: 32.071136, longitude: 34.805431});
    const fourthItur = createIturExample({longitude: 32.071364, latitude: 34.805447});
    const crossBuildings = crossClusterWithIturim(
            cluster,
            [firstItur, secondItur, thirdItur, fourthItur],
    ).geoBuildings;

    expect(crossBuildings.length).toBe(1);
    expect(crossBuildings[0].iturim ? crossBuildings[0].iturim.length : 0).toBe(0);
    expect(crossBuildings[0].polygon.length).toBe(4);
});

test('Set5: few iturim split between 2 buildings', () => {
    const point1 = new Point(32.071341, 34.805351);
    const point2 = new Point(32.071382, 34.805109);
    const point3 = new Point(32.071223, 34.805077);
    const point4 = new Point(32.071164, 34.805324);
    const building1 = new Building([point1, point2, point3, point4]);

    const point5 = new Point(32.071241, 34.805608);
    const point6 = new Point(32.071114, 34.805855);
    const point7 = new Point(32.071014, 34.805807);
    const point8 = new Point(32.071050, 34.805544);
    const building2 = new Building([point5, point6, point7, point8]);
    const cluster = createClusterExample([building1, building2]);

    const firstItur = createIturExample({latitude: 32.071291, longitude: 34.805200});// in first
    const secondItur = createIturExample({latitude: 32.071273, longitude: 34.805088}); // in first
    const thirdItur = createIturExample({latitude: 32.071155, longitude: 34.805683}); // in second
    const fourthItur = createIturExample({latitude: 32.071086, longitude: 34.805619}); // in second
    const fifthItur = createIturExample({latitude: 32.071182, longitude: 34.805437}); // not in any

    const crossBuildings = crossClusterWithIturim(
            cluster, [firstItur, secondItur, thirdItur, fourthItur, fifthItur]).geoBuildings;

    expect(crossBuildings.length).toBe(2);
    expect(crossBuildings[0].iturim ? crossBuildings[0].iturim.length : 0).toBe(2);
    expect(crossBuildings[0].iturim ? crossBuildings[0].iturim[0].location.latitude : 0).toBe(32.071291);
    expect(crossBuildings[0].iturim ? crossBuildings[0].iturim[1].location.latitude : 0).toBe(32.071273);
    expect(crossBuildings[1].iturim ? crossBuildings[1].iturim.length : 0).toBe(2);
    expect(crossBuildings[1].iturim ? crossBuildings[1].iturim[0].location.latitude : 0).toBe(32.071155);
    expect(crossBuildings[1].iturim ? crossBuildings[1].iturim[1].location.latitude : 0).toBe(32.071086);
});

