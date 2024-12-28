import { createSlice } from '@reduxjs/toolkit';

export type PlaceToVisitProperties = {
  displayName: string;
  /** In minutes */
  timeToSpend: number;
  markerColor: string;

  // Props to display place in DataGrid
  rowId: string;
  isNew: boolean;
};

type TripState = {
  firstDayTimestamp: number | null;
  lastDayTimestamp: number | null;
  accommodation: GeoJSON.Feature<GeoJSON.Point, PlaceToVisitProperties> | null;
  dayStartTimestamp: number | null;
  dayEndTimestamp: number | null;
  placesToVisit: GeoJSON.FeatureCollection<GeoJSON.Point, PlaceToVisitProperties>;
  routeCalculations: RouteCalculations;
};

const initialState: TripState = {
  firstDayTimestamp: null,
  lastDayTimestamp: null,
  accommodation: null,
  dayStartTimestamp: null,
  dayEndTimestamp: null,
  placesToVisit: {
    type: 'FeatureCollection',
    features: [],
  },
};

export const tripSlice = createSlice({
  name: 'trip',
  initialState,
  reducers: {
    setFirstDayTimestamp: (state, action: { payload: { firstDayTimestamp: number | null } }) => {
      state.firstDayTimestamp = action.payload.firstDayTimestamp;
    },
    setLastDayTimestamp: (state, action: { payload: { lastDayTimestamp: number | null } }) => {
      state.lastDayTimestamp = action.payload.lastDayTimestamp;
    },
    setAccommodation: (
      state,
      action: { payload: { accommodation: GeoJSON.Feature<GeoJSON.Point, PlaceToVisitProperties> | null } },
    ) => {
      state.accommodation = action.payload.accommodation;
    },
    setDayStartTimestamp: (state, action: { payload: { dayStartTimestamp: number | null } }) => {
      state.dayStartTimestamp = action.payload.dayStartTimestamp;
    },
    setDayEndTimestamp: (state, action: { payload: { dayEndTimestamp: number | null } }) => {
      state.dayEndTimestamp = action.payload.dayEndTimestamp;
    },
    addPlaceToVisit: (
      state,
      action: { payload: { placeToVisit: GeoJSON.Feature<GeoJSON.Point, PlaceToVisitProperties> } },
    ) => {
      state.placesToVisit.features.push(action.payload.placeToVisit);
    },
    updatePlaceToVisit: (
      state,
      action: { payload: { placeToUpdate: GeoJSON.Feature<GeoJSON.Point, PlaceToVisitProperties> } },
    ) => {
      const index = state.placesToVisit.features.findIndex((placeToVisit) => {
        return placeToVisit.properties.rowId === action.payload.placeToUpdate.properties.rowId;
      });
      if (index === -1) {
        return;
      }

      state.placesToVisit.features[index] = action.payload.placeToUpdate;
    },
    removePlaceToVisit: (
      state,
      action: { payload: { placeToRemove: GeoJSON.Feature<GeoJSON.Point, PlaceToVisitProperties> } },
    ) => {
      const { coordinates: placeToRemoveCoords } = action.payload.placeToRemove.geometry;

      const placeToRemoveIndex = state.placesToVisit.features.findIndex((placeToVisit) => {
        const { coordinates: placeToVisitCoords } = placeToVisit.geometry;
        return placeToVisitCoords[0] === placeToRemoveCoords[0] && placeToVisitCoords[1] === placeToRemoveCoords[1];
      });
      if (placeToRemoveIndex === -1) {
        return;
      }

      const currentPlacesToVisit = [...state.placesToVisit.features];
      state.placesToVisit.features = [
        ...currentPlacesToVisit.slice(0, placeToRemoveIndex),
        ...currentPlacesToVisit.slice(placeToRemoveIndex + 1),
      ];
    },
    removePlaceToVisitByRowId: (state, action: { payload: { rowId: string; onlyWhenIsNew: boolean } }) => {
      const { rowId, onlyWhenIsNew } = action.payload;
      const placeToRemoveIndex = state.placesToVisit.features.findIndex((placeToVisit) => {
        return placeToVisit.properties.rowId === rowId && (onlyWhenIsNew ? placeToVisit.properties.isNew : true);
      });
      if (placeToRemoveIndex === -1) {
        return;
      }

      const currentPlacesToVisit = [...state.placesToVisit.features];
      state.placesToVisit.features = [
        ...currentPlacesToVisit.slice(0, placeToRemoveIndex),
        ...currentPlacesToVisit.slice(placeToRemoveIndex + 1),
      ];
    },
  },
});

export const {
  setFirstDayTimestamp,
  setLastDayTimestamp,
  setAccommodation,
  setDayStartTimestamp,
  setDayEndTimestamp,
  addPlaceToVisit,
  updatePlaceToVisit,
  removePlaceToVisit,
  removePlaceToVisitByRowId,
} = tripSlice.actions;
export const { reducer: tripReducer } = tripSlice;
