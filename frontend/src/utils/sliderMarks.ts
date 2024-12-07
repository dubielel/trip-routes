import { Mark } from '@mui/material/Slider/useSlider.types';

//prettier-ignore
export const sliderMarks: Mark[] = [
  { value:  30, label: '0.5h' },
  { value:  60, label:   '1h' },
  { value: 120, label:   '2h' },
  { value: 180, label:   '3h' },
  { value: 240, label:   '4h' },
  { value: 300, label:   '5h' },
  { value: 360, label:   '6h' },
] as const;
