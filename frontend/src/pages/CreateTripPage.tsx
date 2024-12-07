import { Divider, Stack, Grid2 as Grid } from '@mui/material';

import { TravelDates } from '../components/TravelDates';
import { Accommodation } from '../components/Accommodation';
import { TravelTime } from '../components/TravelTime';
import { Map } from '../components/Map';
import { PlacesToVisit } from '../components/PlacesToVisit';
import { CalculateTripButton } from '../components/CalculateTripButton';

export const CreateTripPage = () => {
  return (
    <Grid
      container
      spacing={4}
    >
      <Grid size={6}>
        <Stack
          direction="column"
          spacing={4}
        >
          <TravelDates />
          <Divider />
          <Accommodation />
          <Divider />
          <TravelTime />
          <Divider />
        </Stack>
      </Grid>
      <Grid size={6}>
        <Map />
      </Grid>
      <Grid size={12}>
        <Stack
          direction="column"
          spacing={4}
        >
          <PlacesToVisit />
          <CalculateTripButton />
        </Stack>
      </Grid>
    </Grid>
  );
};
