import type { ReactNode } from 'react';

import { Button } from './Button.js';

export type AsyncStatus = 'loading' | 'empty' | 'error' | 'forbidden' | 'timeout' | 'ready';

export interface AsyncStateProps {
  /** Which request state to show; `ready` renders the children. */
  status: AsyncStatus;
  /** Heading; each status has a default. */
  title?: string;
  /** Supporting text under the heading. */
  message?: string;
  /** Retry action, offered only for `error` and `timeout`. */
  onRetry?: () => void;
  /** Retry button text. */
  retryLabel?: string;
  /** Content shown when `status` is `ready`. */
  children?: ReactNode;
}

const TITLES: Record<Exclude<AsyncStatus, 'ready'>, string> = {
  loading: 'Loading',
  empty: 'Nothing here yet',
  error: 'Something went wrong',
  forbidden: 'You do not have access',
  timeout: 'The request timed out',
};

/** One place for the loading, empty, error, 403 and timeout states of a request. */
export const AsyncState = ({
  status,
  title,
  message,
  onRetry,
  retryLabel = 'Try again',
  children,
}: AsyncStateProps) => {
  if (status === 'ready') return <>{children}</>;
  // Failures interrupt; progress and empty results are announced politely.
  const failure = status === 'error' || status === 'timeout' || status === 'forbidden';
  const retry = onRetry && (status === 'error' || status === 'timeout');
  return (
    <section
      className={`hy-async-state hy-async-state--${status}`}
      role={failure ? 'alert' : 'status'}
      aria-busy={status === 'loading' || undefined}
    >
      {status === 'loading' && <span className="hy-spinner" aria-hidden="true" />}
      <h2 className="hy-async-state__title">{title ?? TITLES[status]}</h2>
      {message && <p className="hy-async-state__message">{message}</p>}
      {retry && <Button label={retryLabel} onClick={onRetry} />}
    </section>
  );
};
