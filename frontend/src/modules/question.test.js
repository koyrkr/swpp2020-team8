import axios from '../apis';
import store from '../store';
import { mockQuestionFeed } from '../constants';
import * as actionCreators from './question';

describe('questionActions', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it(`'getDailyQuestions' should get daily questions correctly`, (done) => {
    jest.mock('axios');

    const spy = jest.spyOn(axios, 'get').mockImplementation(() => {
      return new Promise((resolve) => {
        const res = {
          data: {
            results: mockQuestionFeed
          }
        };
        resolve(res);
      });
    });

    store.dispatch(actionCreators.getDailyQuestions()).then(() => {
      const newState = store.getState();
      expect(spy).toHaveBeenCalled();
      expect(newState.questionReducer.dailyQuestions).toMatchObject(
        mockQuestionFeed
      );
      done();
    });
  });

  it('should dispatch question/GET_DAILY_QUESTIONS_FAILURE when api returns error', async () => {
    jest.mock('axios');
    const spy = jest.spyOn(axios, 'get').mockImplementation(() => {
      return Promise.reject(new Error('error'));
    });

    store.dispatch(actionCreators.getDailyQuestions()).then(() => {
      const newState = store.getState();
      expect(spy).toHaveBeenCalled();
      expect(newState.questionReducer.dailyQuestions).toMatchObject(
        mockQuestionFeed
      );
    });
  });
});