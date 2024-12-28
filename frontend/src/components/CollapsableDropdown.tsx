import { ReactNode, useMemo, useState } from 'react';

import { Checkbox, Collapse, FormControlLabel, useTheme } from '@mui/material';
import { ArrowDropDownIcon } from '@mui/x-date-pickers';

type CollapsableDropdownProps = {
  label: string | ReactNode;
  children?: ReactNode;
};

export const CollapsableDropdown = ({ children, label }: CollapsableDropdownProps) => {
  const theme = useTheme();
  const color = useMemo(() => theme.palette.primary.main, [theme.palette.primary.main]);

  const [enabled, setEnabled] = useState<boolean>(false);
  const handleChange = () => {
    setEnabled((prev) => !prev);
  };

  return (
    <>
      <FormControlLabel
        control={
          <Checkbox
            checked={enabled}
            onChange={handleChange}
            icon={
              <ArrowDropDownIcon
                sx={{
                  color: color,
                  transform: 'rotate(0deg)',
                  transition: 'transform 0.5s',
                }}
              />
            }
            checkedIcon={
              <ArrowDropDownIcon
                sx={{
                  color: color,
                  transform: 'rotate(180deg)',
                  transition: 'transform 0.5s',
                }}
              />
            }
          />
        }
        label={label}
        labelPlacement="start"
        sx={{
          alignSelf: 'start',
          color: color,
          marginBottom: 2,
        }}
      />
      <Collapse in={enabled}>{children}</Collapse>
    </>
  );
};
