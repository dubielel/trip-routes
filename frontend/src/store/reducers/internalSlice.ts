import { createSlice } from '@reduxjs/toolkit';

export type InternalState = {
  hoveredDayIndex: number | null;
};

const initialState: InternalState = {
  hoveredDayIndex: null,
};

export const internalSlice = createSlice({
  name: 'internal',
  initialState,
  reducers: {
    setHoveredDayIndex: (state, action: { payload: { hoveredDayIndex: number | null } }) => {
      state.hoveredDayIndex = action.payload.hoveredDayIndex;
    },
  },
});

export const { setHoveredDayIndex } = internalSlice.actions;
export const { reducer: internalReducer } = internalSlice;
