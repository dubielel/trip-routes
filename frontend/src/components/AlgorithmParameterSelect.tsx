import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent, Skeleton } from '@mui/material';
import { pascalCaseToHumanReadable } from '../utils/pascalCaseToHumanReadable';
import { useMemo } from 'react';

type AlgorithmParameterSelectProps = {
  label: string;
  parameter: string | null;
  availableParameters: string[];
  onChange: (event: SelectChangeEvent) => void;
};

export const AlgorithmParameterSelect = ({
  label,
  parameter,
  availableParameters,
  onChange,
}: AlgorithmParameterSelectProps) => {
  const labelId = useMemo(() => `${label.toLowerCase()}-select-input-label`, [label]);

  if (availableParameters.length === 0 || parameter === null) {
    return (
      <Skeleton width={'50%'}>
        <FormControl fullWidth>
          <InputLabel id={labelId}>{label}</InputLabel>
          <Select
            labelId={labelId}
            label={label}
            value=""
            onChange={onChange}
            disabled
          >
            <MenuItem value="">
              <em>Loading...</em>
            </MenuItem>
          </Select>
        </FormControl>
      </Skeleton>
    );
  }

  return (
    <FormControl fullWidth>
      <InputLabel id={labelId}>{label}</InputLabel>
      <Select
        labelId={labelId}
        label={label}
        value={parameter}
        onChange={onChange}
      >
        {availableParameters.map((param) => (
          <MenuItem
            key={param}
            value={param}
          >
            {pascalCaseToHumanReadable(param)}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};
