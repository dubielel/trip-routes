import { Stack, Typography } from '@mui/material';
import { TimePicker } from '@mui/x-date-pickers';

import dayjs from 'dayjs';

import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/reduxStore';
import { setDayStartTimestamp, setDayEndTimestamp } from '../store/reducers/tripSlice';

export const TravelTime = () => {
  const {
    dayStartTimestamp,
    dayEndTimestamp,
    routeCalculations: { isCalculating: isRouteCalculating },
  } = useSelector((state: RootState) => state.trip);
  const dispatch = useDispatch();

  return (
    <Stack
      direction="column"
      spacing={2}
    >
      <Typography variant="h5">Travel time</Typography>
      <Stack
        direction="row"
        spacing={2}
      >
        <TimePicker
          label="At what time do you want to start each day?"
          value={dayStartTimestamp ? dayjs(dayStartTimestamp) : null}
          onChange={(newDate) => dispatch(setDayStartTimestamp({ dayStartTimestamp: newDate?.valueOf() ?? null }))}
          ampm={false}
          slotProps={{
            field: { clearable: true },
            textField: { fullWidth: true },
          }}
          disabled={isRouteCalculating}
        />
        <TimePicker
          label="At what time do you want to be back each day?"
          value={dayEndTimestamp ? dayjs(dayEndTimestamp) : null}
          onChange={(newDate) => dispatch(setDayEndTimestamp({ dayEndTimestamp: newDate?.valueOf() ?? null }))}
          ampm={false}
          slotProps={{
            field: { clearable: true },
            textField: { fullWidth: true },
          }}
          disabled={isRouteCalculating}
        />
      </Stack>
    </Stack>
  );
};
