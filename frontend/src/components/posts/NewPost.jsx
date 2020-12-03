import React, { useState } from 'react';
import styled from 'styled-components';
import { TextareaAutosize } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import ShareSettings from './ShareSettings';

const NewPostWrapper = styled.div`
  width: 100%;
  margin: 0 auto;
  border: 1px solid #eee;
  padding: 10px;
  border-radius: 4px;
  box-sizing: border-box;
  background: #fff;
`;

const useStyles = makeStyles({
  textarea: {
    padding: '5px',
    borderRadius: '2px',
    color: 'rgb(50, 50, 50)',
    fontSize: '14px',
    outline: 'none !important',
    width: '100%',
    height: 'auto',
    boxSizing: 'border-box',
    border: 'none',
    margin: '4px 0',
    background: '#fff',
    cursor: 'auto',
    resize: 'none',
    overflow: 'hidden',
    fontFamily: 'Noto Sans KR, sans-serif'
  }
});

export default function NewPost() {
  const classes = useStyles();
  const [postInfo, setPostInfo] = useState({
    content: '',
    type: 'Article'
  });

  const onInputChange = (e) => {
    const { name, value } = e.target;
    setPostInfo((prev) => ({ ...prev, [name]: value }));
  };

  const resetContent = () => {
    setPostInfo((prev) => ({ ...prev, content: '' }));
  };

  return (
    <NewPostWrapper>
      <TextareaAutosize
        id="new-post-input"
        name="content"
        placeholder="떠오르는 생각을 공유해주세요."
        value={postInfo.content}
        onChange={onInputChange}
        className={classes.textarea}
      />
      <ShareSettings newPost={postInfo} resetContent={resetContent} />
    </NewPostWrapper>
  );
}
