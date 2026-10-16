import * as net from 'node:net';
import * as nodemailer from 'nodemailer';

// DRAFT P03 capture contract. This source does not authorize connection/import.
export const POLICY = Object.freeze({
  host: 'mailpit', port: 1025,
  from: 'notifier@opsflow.invalid', to: 'manifest@opsflow.invalid',
  connectionTimeout: 3000, greetingTimeout: 3000, socketTimeout: 5000,
  totalTimeoutMs: 15000, ackReserveMs: 5000, clockSkewReserveMs: 5000, maxTextBytes: 512,
});
const CLAIM_KEYS = Object.freeze(['id', 'run_id', 'source', 'row_count', 'lease_token', 'lease_until']);
const CREDENTIAL_KEYS = Object.freeze(['host', 'port', 'secure', 'disableStartTls', 'user', 'password', 'hostName']);
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const SOURCES = Object.freeze(['hy-home.docker', 'hy-home.k8s', 'Project-Template', 'blog-data']);
export type Claim = Readonly<{ id: string | number; run_id: string; source: string; row_count: number; lease_token: string; lease_until: string }>;
export type Outcome = Readonly<{ run_id: string; state: 'accepted_by_smtp' | 'uncertain' | 'cancelled' }>;
export type CaptureTransport = { sendMail(message: ReturnType<typeof messageFor>): Promise<unknown>; close(): void };
export type TransportFactory = (options: ReturnType<typeof transportOptions>) => CaptureTransport;

function record(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

export function validateClaim(value: unknown): Claim {
  if (!record(value) || Object.keys(value).length !== CLAIM_KEYS.length ||
      !CLAIM_KEYS.every(key => Object.hasOwn(value, key))) throw new Error('OPSFLOW_INVALID_CLAIM');
  const validId = typeof value.id === 'number'
    ? Number.isSafeInteger(value.id) && value.id > 0
    : typeof value.id === 'string' && /^[1-9][0-9]{0,18}$/.test(value.id) && BigInt(value.id) <= 9223372036854775807n;
  if (!validId || typeof value.run_id !== 'string' || !/^[0-9a-f]{64}$/.test(value.run_id) ||
      typeof value.source !== 'string' || !SOURCES.includes(value.source) ||
      typeof value.row_count !== 'number' || !Number.isSafeInteger(value.row_count) || value.row_count < 1 || value.row_count > 5000 ||
      typeof value.lease_token !== 'string' || !UUID.test(value.lease_token) ||
      typeof value.lease_until !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value.lease_until) ||
      !Number.isFinite(Date.parse(value.lease_until)) || new Date(value.lease_until).toISOString() !== value.lease_until) {
    throw new Error('OPSFLOW_INVALID_CLAIM');
  }
  return Object.freeze({ id: value.id as string | number, run_id: value.run_id,
    source: value.source, row_count: value.row_count, lease_token: value.lease_token, lease_until: value.lease_until });
}

export function transportOptions(value: unknown) {
  if (!record(value) || Object.keys(value).some(key => !CREDENTIAL_KEYS.includes(key)) ||
      value.host !== POLICY.host || value.port !== POLICY.port || value.secure !== false ||
      value.disableStartTls !== true || value.user !== '' || value.password !== '' ||
      (value.hostName !== undefined && value.hostName !== '')) throw new Error('OPSFLOW_INVALID_CREDENTIAL');
  return Object.freeze({
    host: POLICY.host, port: POLICY.port, name: 'n8n-opsflow.invalid',
    secure: false, ignoreTLS: true, pool: false,
    connectionTimeout: POLICY.connectionTimeout, greetingTimeout: POLICY.greetingTimeout,
    socketTimeout: POLICY.socketTimeout, dnsTimeout: POLICY.connectionTimeout,
    disableFileAccess: true, disableUrlAccess: true, logger: false, debug: false,
  });
}

export function messageFor(claim: Claim) {
  const text = `Manifest published\nrun=${claim.run_id}\nsource=${claim.source}\nrows=${claim.row_count}\n`;
  if (Buffer.byteLength(text, 'utf8') > POLICY.maxTextBytes) throw new Error('OPSFLOW_INVALID_CLAIM');
  return Object.freeze({
    from: POLICY.from, to: POLICY.to,
    envelope: Object.freeze({ from: POLICY.from, to: [POLICY.to] }),
    subject: 'DEV manifest publication', text,
    messageId: `<opsflow.${claim.run_id}@opsflow.invalid>`,
    disableFileAccess: true, disableUrlAccess: true,
  });
}

// Own the socket: Nodemailer's nonpool close() is not a socket-cancellation contract.
// Injected constructors are an offline-test seam; the node exposes no such parameters.
export function createCaptureTransport(
  options: ReturnType<typeof transportOptions>,
  createSocket = net.createConnection,
  createMailer = nodemailer.createTransport,
): CaptureTransport {
  let socket: net.Socket | undefined;
  let closed = false;
  const mailer = createMailer({ ...options, getSocket: (_unused: unknown, callback: (error: Error | null, result?: { connection: net.Socket }) => void) => {
    if (closed) { callback(new Error('OPSFLOW_TRANSPORT_CLOSED')); return; }
    socket = createSocket({ host: POLICY.host, port: POLICY.port });
    const owned = socket;
    const timer = setTimeout(() => { owned.destroy(new Error('OPSFLOW_CONNECT_TIMEOUT')); }, POLICY.connectionTimeout);
    const cleanup = () => { clearTimeout(timer); owned.removeListener('error', onError); owned.removeListener('connect', onConnect); };
    const onError = () => { cleanup(); callback(new Error('OPSFLOW_CONNECT_FAILED')); };
    const onConnect = () => { cleanup(); callback(null, { connection: owned }); };
    owned.once('error', onError);
    owned.once('connect', onConnect);
    owned.once('close', cleanup);
  } });
  return {
    sendMail: message => mailer.sendMail(message),
    close: () => {
      if (closed) return;
      closed = true;
      socket?.destroy();
      mailer.close();
    },
  };
}

function accepted(info: unknown): boolean {
  return record(info) && Array.isArray(info.accepted) && info.accepted.length === 1 &&
    info.accepted[0] === POLICY.to && Array.isArray(info.rejected) && info.rejected.length === 0;
}

export async function sendClaim(
  rawClaim: unknown, credential: unknown, signal?: AbortSignal,
  createTransport: TransportFactory = createCaptureTransport,
): Promise<Outcome> {
  const claim = validateClaim(rawClaim);
  const options = transportOptions(credential);
  const result = (state: Outcome['state']): Outcome => Object.freeze({ run_id: claim.run_id, state });
  const currentLease = () => Date.parse(claim.lease_until) - Date.now() >
    POLICY.totalTimeoutMs + POLICY.ackReserveMs + POLICY.clockSkewReserveMs;
  if (signal?.aborted || !currentLease()) return result('cancelled');
  let transport: CaptureTransport | undefined;
  let timer: ReturnType<typeof setTimeout> | undefined;
  let cancellation: (() => void) | undefined;
  let state: Outcome['state'] = 'uncertain';
  try {
    transport = createTransport(options);
    const stopped = new Promise<'uncertain'>(resolve => {
      cancellation = () => resolve('uncertain');
      signal?.addEventListener('abort', cancellation, { once: true });
      timer = setTimeout(() => resolve('uncertain'), POLICY.totalTimeoutMs);
    });
    if (signal?.aborted || !currentLease()) state = 'cancelled';
    else {
      const sending = Promise.resolve(transport.sendMail(messageFor(claim))).then(
        info => accepted(info) ? 'accepted_by_smtp' as const : 'uncertain' as const,
        () => 'uncertain' as const,
      );
      state = await Promise.race([sending, stopped]);
      if (signal?.aborted) state = 'uncertain';
    }
  } catch { state = 'uncertain'; }
  finally {
    clearTimeout(timer);
    if (cancellation) signal?.removeEventListener('abort', cancellation);
    try { transport?.close(); } catch { state = 'uncertain'; }
  }
  return result(state);
}
