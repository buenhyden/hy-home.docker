---
trigger: always_on
glob: "**/*.{js,ts,tsx}"
description: "Socket.IO: Namespaces, Rooms, TypeScript Types, and Reconnection."
---
# Socket.IO Standards

## 1. Initialization & Security

- **WSS**: Use `wss://` in production (never `ws://`).
- **Auth**: Pass authentication tokens via `auth` option.
- **CORS**: Configure `cors` on server for cross-origin clients.

### Example: Secure Init

**Good**

```typescript
const socket = io("wss://api.example.com", {
  transports: ["websocket", "polling"],
  auth: { token: "YOUR_AUTH_TOKEN" }
});
```

**Bad**

```typescript
const socket = io("http://localhost:3000"); // Insecure, no auth
```

## 2. Namespaces & Rooms

- **Namespaces**: Use for distinct features (`/chat`, `/admin`).
- **Rooms**: Use for grouping clients within a namespace.

### Example: Rooms

**Good**

```typescript
socket.on("joinRoom", (roomName) => {
  socket.join(roomName);
  io.to(roomName).emit("userJoined", socket.id);
});
```

## 3. TypeScript Types

- **Event Interfaces**: Define `ServerToClientEvents` and `ClientToServerEvents`.
- **Type Safety**: Use typed sockets for autocomplete and validation.

### Example: Types

**Good**

```typescript
interface ServerToClientEvents {
  newMessage: (data: { user: string; message: string }) => void;
}
interface ClientToServerEvents {
  sendMessage: (data: { room: string; message: string }) => void;
}

const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io("wss://...");
```

## 4. Error Handling & Reconnection

- **connect_error**: Handle auth failures gracefully.
- **Acknowledgements**: Use callbacks for guaranteed delivery.
