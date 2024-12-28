import { createSlice } from '@reduxjs/toolkit';
import { type PlaceToVisitProperties } from './tripSlice';
import { chance } from '../../utils/chance';
import { AvailableParametersResponse } from '../../types/AvailableParametersResponse';
import { createUnionSchemaFromArray } from '../../utils/createUnionSchemaFromArray';

export type RoutePlaceToVisitProperties = PlaceToVisitProperties & {
  departureTimestamp: number | null;
  arrivalTimestamp: number | null;
};

export type RouteProperties = {
  colors: string[];
};

type RouteState = {
  availableMoveMethods: string[];
  availableAlgorithms: string[];

  moveMethod: string | null;
  algorithm: string | null;
  isCalculating: boolean;
  routePoints: GeoJSON.FeatureCollection<GeoJSON.Point, RoutePlaceToVisitProperties>[] | null;
  routeGeometry: GeoJSON.Feature<GeoJSON.MultiLineString, RouteProperties> | null;
};

const initialState: RouteState = {
  availableMoveMethods: [],
  availableAlgorithms: [],

  moveMethod: null,
  algorithm: null,
  isCalculating: false,
  routePoints: null,
  routeGeometry: null,
};

export const routeSlice = createSlice({
  name: 'route',
  initialState,
  reducers: {
    setAvailableParameters: (state, action: { payload: AvailableParametersResponse }) => {
      state.availableMoveMethods = action.payload.moves;
      state.availableAlgorithms = action.payload.algorithms;
    },
    setMoveMethod: (state, action: { payload: { moveMethod: string } }) => {
      if (state.availableMoveMethods.length === 0) {
        throw new Error('Available move methods are not set');
      }
      const validationSchema = createUnionSchemaFromArray(state.availableMoveMethods as [string, ...string[]]);
      state.moveMethod = validationSchema.parse(action.payload.moveMethod);
    },
    setAlgorithm: (state, action: { payload: { algorithm: string } }) => {
      if (state.availableAlgorithms.length === 0) {
        throw new Error('Available algorithms are not set');
      }
      const validationSchema = createUnionSchemaFromArray(state.availableAlgorithms as [string, ...string[]]);
      state.algorithm = validationSchema.parse(action.payload.algorithm);
    },
    setIsCalculating: (state, action: { payload: { isCalculating: boolean } }) => {
      state.isCalculating = action.payload.isCalculating;
    },
    setCalculations: (
      state,
      action: {
        payload: {
          route: GeoJSON.FeatureCollection<GeoJSON.Point, RoutePlaceToVisitProperties>[];
          geometry: GeoJSON.Feature<GeoJSON.MultiLineString, RouteProperties>;
        };
      },
    ) => {
      state.routePoints = action.payload.route;

      // Just to be sure that we have the same number of colors as LineStrings
      if (action.payload.geometry.properties.colors.length > action.payload.geometry.geometry.coordinates.length) {
        action.payload.geometry.properties.colors = [
          ...action.payload.geometry.properties.colors.slice(0, action.payload.geometry.geometry.coordinates.length),
        ];
      } else if (
        action.payload.geometry.properties.colors.length < action.payload.geometry.geometry.coordinates.length
      ) {
        action.payload.geometry.properties.colors = [
          ...action.payload.geometry.properties.colors,
          ...Array.from(
            {
              length:
                action.payload.geometry.geometry.coordinates.length - action.payload.geometry.properties.colors.length,
            },
            () => chance.color({ format: 'hex' }),
          ),
        ];
      }

      state.routeGeometry = action.payload.geometry;
    },
    clearCalculations: (state) => {
      state.routePoints = null;
      state.routeGeometry = null;
    },
  },
});

export const {
  setAvailableParameters,
  setMoveMethod,
  setAlgorithm,
  setIsCalculating,
  setCalculations,
  clearCalculations,
} = routeSlice.actions;
export const { reducer: routeReducer } = routeSlice;
