import React from 'react';
import Skeleton from '@material-ui/lab/Skeleton';
import { PostItemWrapper } from '../../styles';

export default function LoadingList() {
  const loadingList = [...Array(5)].map((_, index) => (
    // eslint-disable-next-line react/no-array-index-key
    <PostItemWrapper key={`loading-${index}`} className="skeleton-list">
      <Skeleton
        variant="circle"
        width={40}
        height={40}
        style={{ opacity: '0.8', margin: '4px 0' }}
      />
      <Skeleton
        animation="wave"
        variant="rect"
        height={88}
        style={{ opacity: '0.8', margin: '8px 0' }}
      />
    </PostItemWrapper>
  ));

  return <div>{loadingList}</div>;
}
