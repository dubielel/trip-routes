import { Layer, Source } from 'react-map-gl/maplibre';
import { useSelector } from 'react-redux';
import { RootState } from '../store/reduxStore';
import { useMemo } from 'react';

type MapLineLayerProps = {
  layerId: string;
  dayIndex: number;
  route: GeoJSON.LineString;
  color: string;
};

export const MapLineLayer = ({ layerId, dayIndex , route, color }: MapLineLayerProps) => {
  const hoveredDayIndex = useSelector((state: RootState) => state.internal.hoveredDayIndex);

  const opacity = useMemo(() => {
    if (hoveredDayIndex === null) {
      return 1;
    }
    return hoveredDayIndex === dayIndex ? 1 : 0.25;
  }, [hoveredDayIndex, dayIndex]);

  return (
    <Source
      type="geojson"
      data={route}
    >
      <Layer
        id={layerId}
        type="line"
        layout={{
          'line-join': 'round',
          'line-cap': 'round',
        }}
        paint={{
          'line-color': color,
          'line-width': 8,
          'line-opacity': opacity,
        }}
      />
    </Source>
  );
};
