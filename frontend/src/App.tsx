import { MapProvider } from 'react-map-gl/maplibre';

import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

import { Provider as ReduxProvider } from 'react-redux';
import { reduxStore } from './store/reduxStore';

import './App.css';

import { CreateTripPage } from './pages/CreateTripPage';

const theme = createTheme({
  // palette: { mode: 'dark' },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <ReduxProvider store={reduxStore}>
          <MapProvider>
            <CreateTripPage />
          </MapProvider>
        </ReduxProvider>
      </LocalizationProvider>
    </ThemeProvider>
  );
}

export default App;
