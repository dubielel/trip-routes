import { Stack, Typography } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';

import dayjs from 'dayjs';

import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/reduxStore';
import { setFirstDayTimestamp, setLastDayTimestamp } from '../store/reducers/tripSlice';

export const TravelDates = () => {
  const { firstDayTimestamp, lastDayTimestamp } = useSelector((state: RootState) => state.trip);
  const { isCalculating } = useSelector((state: RootState) => state.route);
  const dispatch = useDispatch();

  return (
    <Stack
      direction="column"
      spacing={2}
    >
      <Typography variant="h5">Travel dates</Typography>
      <Stack
        direction="row"
        spacing={2}
      >
        <DatePicker
          label="What day should be the first day of your trip?"
          value={firstDayTimestamp ? dayjs(firstDayTimestamp) : null}
          onChange={(newDate) => dispatch(setFirstDayTimestamp({ firstDayTimestamp: newDate?.valueOf() ?? null }))}
          slotProps={{
            field: { clearable: true },
            textField: { fullWidth: true },
          }}
          disabled={isCalculating}
        />
        <DatePicker
          label="What day should be the last day of your trip?"
          value={lastDayTimestamp ? dayjs(lastDayTimestamp) : null}
          onChange={(newDate) => dispatch(setLastDayTimestamp({ lastDayTimestamp: newDate?.valueOf() ?? null }))}
          slotProps={{
            field: { clearable: true },
            textField: { fullWidth: true },
          }}
          disabled={isCalculating}
        />
      </Stack>
    </Stack>
  );
};
