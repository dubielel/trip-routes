import { configureStore } from '@reduxjs/toolkit';
import { combinedReducers } from './reducers/combinedReducers';

export const reduxStore = configureStore({
  reducer: combinedReducers,
});

export type RootState = ReturnType<typeof reduxStore.getState>;
export type AppDispatch = typeof reduxStore.dispatch;

export const { dispatch } = reduxStore;
