import { combineReducers } from 'redux';

import { tripReducer } from './tripSlice';

export const combinedReducers = combineReducers({ trip: tripReducer });
