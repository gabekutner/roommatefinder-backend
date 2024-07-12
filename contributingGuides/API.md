# API Details
These are best practices related to the current API used for roommatefinder.

## Philosophy
- Each user action should generate at most 1 API call.
- Clients should be kept up-to-date with many small incremental changes to data.
- Creating data needs to be optimistic on every connection (offline, slow 3G, etc), eg. `CreateProfile` should work without waiting for a server response.

## Response Handling
1. ** HTTPs Response ** - Data that is returned with the HTTPS response is only sent to the client that initiated the request.

2. ** Async ** (web socket) - Data returned with a socket event is sent to all currently connected clients for the user that made the request, as well as any other necessary participants (eg. other users in a chat)