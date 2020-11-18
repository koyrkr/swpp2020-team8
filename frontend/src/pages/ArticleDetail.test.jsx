import React from 'react';
import { mount } from 'enzyme';
import { Provider } from 'react-redux';
import { Router } from 'react-router-dom';
import { composeWithDevTools } from 'redux-devtools-extension';
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import ArticleDetail from './ArticleDetail';
import PostItem from '../components/posts/PostItem';
import rootReducer from '../modules';
import { mockStore } from '../mockStore';
import 'jest-styled-components';
import history from '../history';

const mockArticle = {
  id: 4756,
  'content-type': 'Article', // or const int e.g. (1: Article, 2: Response...)
  author_detail: {
    id: 123,
    username: 'curious',
    profile_pic:
      'https://www.publicdomainpictures.net/pictures/260000/velka/dog-face-cartoon-illustration.jpg'
  }, // blank or null if anonymous
  created_at: '2020-09-23T10:38:47.975019+08:00',
  content:
    '안녕하세요 반가워요 잘있어요 다시만나요 이거는 질문없이 쓰는 그냥 뻘글이에요 이쁘죠?????',
  comments: [
    {
      id: 1272,
      post_id: 383,
      content: '재밌네요',
      author: 1,
      author_detail: {
        id: 123,
        username: 'curious',
        profile_pic:
          'https://www.publicdomainpictures.net/pictures/260000/velka/dog-face-cartoon-illustration.jpg'
      },
      referenced_comments: 1272,
      is_reply: false,
      replies: [
        {
          id: 1273,
          post_id: 383,
          content: '같이하고싶어요',
          author: 2,
          author_detail: {
            id: 2,
            profile_pic:
              'https://www.publicdomainpictures.net/pictures/260000/velka/dog-face-cartoon-illustration.jpg',
            username: '아이폰'
          },
          is_poster_owner: false,
          referenced_comments: 1272,
          is_reply: true,
          is_private: false,
          create_dt: '2020-09-23T10:40:24.421000+08:00',
          update_dt: '2020-09-23T10:40:24.428734+08:00'
        }
      ],
      is_private: false,
      create_dt: '2020-09-23T10:38:47.975019+08:00',
      update_dt: '2020-09-23T10:39:35.849029+08:00'
    },

    {
      id: 1274,
      post_id: 383,
      content: '퍼가요!!!!',
      author: 3,
      author_detail: {
        id: 2,
        profile_pic:
          'https://images.vexels.com/media/users/3/144928/isolated/preview/ebbccaf76f41f7d83e45a42974cfcd87-dog-illustration-by-vexels.png',
        username: '아이폰'
      },
      referenced_comments: 1274,
      is_reply: false,
      is_private: true,
      create_dt: '2020-09-23T10:40:42.268355+08:00',
      update_dt: '2020-09-23T10:40:42.268384+08:00'
    }
  ]
};

describe('Article Detail Page', () => {
  const store = createStore(
    rootReducer,
    mockStore,
    composeWithDevTools(applyMiddleware(thunk))
  );

  const getWrapper = () =>
    mount(
      <Provider store={store}>
        <Router history={history}>
          <ArticleDetail />
        </Router>
      </Provider>
    );

  it('should render without errors', () => {
    jest.mock('react-redux', () => ({
      useDispatch: () => jest.fn()
    }));
    const wrapper = getWrapper();
    const postDetail = wrapper.find('ArticleDetail');
    expect(postDetail.length).toBe(1);
  });

  it('should render article without errors', () => {
    const getWrapperTest = () =>
      mount(
        <Provider store={store}>
          <Router history={history}>
            <ArticleDetail>
              <PostItem postObj={mockArticle} />
            </ArticleDetail>
          </Router>
        </Provider>
      );
    jest.mock('react-redux', () => ({
      useDispatch: () => jest.fn()
    }));
    const wrapper = getWrapperTest();
    const postDetail = wrapper.find('PostItemWrapper');
    expect(postDetail.length).toBe(1);
  });
});
