import React, { useEffect } from 'react';
import { Route, Switch, Redirect, useHistory } from 'react-router-dom';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import { useSelector, useDispatch } from 'react-redux';
import Login from './pages/Login';
import { GlobalStyle, MainWrapper, FeedWrapper } from './styles';
import Header from './components/Header';
import QuestionListWidget from './components/QuestionListWidget';
import FriendListWidget from './components/FriendListWidget';
import SignUp from './pages/SignUp';
import QuestionSelection from './pages/QuestionSelection';
import FriendFeed from './pages/FriendFeed';
import AnonymousFeed from './pages/AnonymousFeed';
import QuestionFeed from './pages/QuestionFeed';
import PrivateRoute from './components/PrivateRoute';
import QuestionDetail from './pages/QuestionDetail';
import PostDetail from './pages/PostDetail';
import FriendsPage from './pages/FriendsPage';
import SearchResults from './pages/SearchResults';
import NotificationPage from './pages/NotificationPage';
import PostEdit from './pages/PostEdit';
import UserPage from './pages/UserPage';
import { getNotifications } from './modules/notification';

const theme = createMuiTheme({
  palette: {
    primary: { main: '#ff395b' },
    secondary: { light: '#eee', main: '#777' }
  },
  typography: {
    fontFamily: ['Noto Sans KR', 'sans-serif']
  }
});

const App = () => {
  const currentUser = useSelector((state) => state.userReducer.currentUser);
  const dispatch = useDispatch();
  const history = useHistory();
  const selectQuestion = useSelector(
    (state) => state.userReducer.selectQuestion
  );
  const signUpRedirectPath = currentUser?.question_history
    ? '/friends'
    : 'select-questions';

  useEffect(() => {
    // eslint-disable-next-line no-unused-vars
    return history.listen((location) => {
      // console.log(`You changed the page to: ${location.pathname}`);
      if (currentUser) {
        dispatch(getNotifications());
      }
    });
  }, [history, dispatch, currentUser]);

  return (
    <MuiThemeProvider theme={theme}>
      <GlobalStyle />
      <Header />
      {currentUser == null ||
      (!selectQuestion && currentUser?.question_history === null) ? (
        <Switch>
          <Route exact path="/login" component={Login} />
          <Route exact path="/signup" component={SignUp} />
          <Route exact path="/select-questions" component={QuestionSelection} />
          <Redirect from="/" to="/login" />
        </Switch>
      ) : (
        <MainWrapper>
          <QuestionListWidget />
          <FeedWrapper>
            <Switch>
              <Redirect from="/login" to="/friends" />
              <Redirect from="/signup" to={signUpRedirectPath} />
              <Route
                exact
                path="/select-questions"
                component={QuestionSelection}
              />
              <PrivateRoute exact path="/friends" component={FriendFeed} />
              <PrivateRoute exact path="/anonymous" component={AnonymousFeed} />
              <PrivateRoute exact path="/questions" component={QuestionFeed} />
              <PrivateRoute exact path="/users/:id" component={UserPage} />
              <PrivateRoute
                exact
                path="/notifications"
                component={NotificationPage}
              />
              <PrivateRoute
                exact
                path="/notifications/friend-request"
                component={NotificationPage}
                tabType="FriendRequest"
              />
              <PrivateRoute
                exact
                path="/notifications/response-request"
                component={NotificationPage}
                tabType="ResponseRequest"
              />
              <PrivateRoute
                exact
                path="/questions/:id"
                component={QuestionDetail}
              />
              <PrivateRoute
                exact
                path="/:postType/:id/edit"
                component={PostEdit}
              />
              <Route exact path="/search" component={SearchResults} />

              <PrivateRoute path="/:postType/:id" component={PostDetail} />
              <PrivateRoute exact path="/my-friends" component={FriendsPage} />
              <Redirect exact path="/" to="/friends" />
            </Switch>
          </FeedWrapper>
          <FriendListWidget />
        </MainWrapper>
      )}
    </MuiThemeProvider>
  );
};

export default App;
