import React from 'react';
import { Route, Switch } from 'react-router-dom';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import { GlobalStyle } from './styles';
import StyledComponentExample from './components/StyledComponentExample';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import QuestionSelection from './pages/QuestionSelection';

const theme = createMuiTheme({
  palette: {
    primary: { main: '#ff395b' },
    secondary: { light: '#eee', main: '#777' }
  },
  typography: {
    fontFamily: ['Noto Sans KR', 'sans-serif']
  }
});

function App() {
  return (
    <MuiThemeProvider theme={theme}>
      <GlobalStyle />
      <Switch>
        <Route exact path="/login" component={Login} />
        <Route exact path="/signup" component={SignUp} />
        <Route exact path="/select-questions" component={QuestionSelection} />
        <Route path="/style-example" component={StyledComponentExample} />
      </Switch>
    </MuiThemeProvider>
  );
}

export default App;
