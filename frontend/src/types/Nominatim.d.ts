export declare type NominatimSearchResponse = {
  licence: string;
  type: 'FeatureCollection';
  features: {
    type: 'Feature';
    geometry: GeoJSON.Geometry;
    bbox: [number, number, number, number];
    properties: {
      address: Record<string, unknown>;
      addresstype: string;
      category: string;
      display_name: string;
      importance: number;
      name: string;
      osm_id: number;
      osm_type: string;
      place_id: number;
      place_rank: number;
      type: string;
    };
  }[];
};

export declare type NominatimResultResponse = {
  id: string | number;
  type: 'Feature';
  geometry: GeoJSON.Point;
  place_name: string;
  properties: {
    place_id: number;
    osm_type: string;
    osm_id: number;
    place_rank: number;
    category: string;
    type: string;
    importance: number;
    addresstype: string;
    name: string;
    display_name: string;
    address: Record<string, unknown>;
  };
  text: string;
  place_type: string[];
};
