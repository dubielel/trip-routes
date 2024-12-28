import { useCallback } from 'react';

import { SelectChangeEvent, Stack } from '@mui/material';

import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/reduxStore';
import { setAlgorithm, setMoveMethod } from '../store/reducers/routeSlice';

import { CalculateTripButton } from './CalculateTripButton';
import { AlgorithmParameterSelect } from './AlgorithmParameterSelect';
import { CollapsableDropdown } from './CollapsableDropdown';

export const CalculateTrip = () => {
  const { availableMoveMethods, moveMethod, availableAlgorithms, algorithm } = useSelector(
    (state: RootState) => state.route,
  );
  const dispatch = useDispatch();

  const handleAlgorithmChange = useCallback(
    (event: SelectChangeEvent) => {
      dispatch(setAlgorithm({ algorithm: event.target.value as string }));
    },
    [dispatch],
  );

  const handleMoveMethodChange = useCallback(
    (event: SelectChangeEvent) => {
      dispatch(setMoveMethod({ moveMethod: event.target.value as string }));
    },
    [dispatch],
  );

  return (
    <Stack
      direction="column"
      spacing={2}
    >
      <CollapsableDropdown label={<i>Advanced algorithm options</i>}>
        <Stack
          direction="row"
          spacing={2}
        >
          <AlgorithmParameterSelect
            label="Algorithm"
            parameter={algorithm}
            availableParameters={availableAlgorithms}
            onChange={handleAlgorithmChange}
          />
          <AlgorithmParameterSelect
            label="Move Method"
            parameter={moveMethod}
            availableParameters={availableMoveMethods}
            onChange={handleMoveMethodChange}
          />
        </Stack>
      </CollapsableDropdown>
      <CalculateTripButton />
    </Stack>
  );
};
