export interface ButtonProps {
  /** Button text. */
  label: string;
  /** `primary` is the single main action of a view; everything else is `secondary`. */
  variant?: 'primary' | 'secondary';
  /** Control height and text size. */
  size?: 'small' | 'medium' | 'large';
  /** Native button type; forms submit only with `submit`. */
  type?: 'button' | 'submit';
  /** Unavailable action. */
  disabled?: boolean;
  /** Action in progress; the button is busy and does not repeat the action. */
  loading?: boolean;
  /** Click handler. */
  onClick?: () => void;
}

/** Action button styled only through the design tokens in styles.css. */
export const Button = ({
  label,
  variant = 'secondary',
  size = 'medium',
  type = 'button',
  disabled = false,
  loading = false,
  onClick,
}: ButtonProps) => (
  <button
    type={type}
    className={`hy-button hy-button--${variant} hy-button--${size}`}
    disabled={disabled || loading}
    aria-busy={loading || undefined}
    onClick={onClick}
  >
    {loading && <span className="hy-spinner" aria-hidden="true" />}
    {label}
  </button>
);
