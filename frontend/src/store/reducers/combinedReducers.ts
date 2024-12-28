import { combineReducers } from 'redux';

import { tripReducer } from './tripSlice';
import { routeReducer } from './routeSlice';
import { internalReducer } from './internalSlice';

export const combinedReducers = combineReducers({ trip: tripReducer, route: routeReducer, internal: internalReducer });
