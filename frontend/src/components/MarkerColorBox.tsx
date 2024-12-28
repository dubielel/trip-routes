import { Box } from '@mui/material';

type MarkerColorBoxProps = {
  color: string;
};

export const MarkerColorBox = ({ color }: MarkerColorBoxProps) => (
  <Box
    sx={{
      width: '24px',
      height: '24px',
      borderRadius: '4px',
      backgroundColor: color,
      boxShadow: '0 4px 6px rgba(50, 50, 93, 0.11),0 1px 3px rgba(0, 0, 0, 0.08)',
    }}
  />
);
