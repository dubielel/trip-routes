import { GridRenderCellParams } from '@mui/x-data-grid';
import { Slider } from '@mui/material';

import { sliderMarks } from '../../utils/sliderMarks';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const GridSliderCell = ({ value }: GridRenderCellParams<any, number | null>) => {
  return (
    <Slider
      value={value ?? 30}
      min={30}
      step={30}
      max={360}
      marks={sliderMarks}
      valueLabelDisplay="auto"
      slotProps={{ input: { readOnly: true } }}
      sx={{ width: '90%' }}
    />
  );
};
