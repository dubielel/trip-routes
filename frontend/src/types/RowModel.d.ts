export declare type RowModel = {
  type: 'Feature';
  geometry: {
    type: 'Point';
    coordinates: [number, number];
  } | null;
  properties: {
    displayName: string | null;
    timeToSpend: number | null;
    markerColor: string;
    rowId: string;
    isNew: boolean;
  };
};
