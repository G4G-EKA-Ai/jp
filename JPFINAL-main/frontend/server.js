/**
 * JAYTI Frontend Proxy Server
 * Proxies all requests to Django backend on port 8001
 * Runs on port 3000 for the Emergent platform
 */
const http = require('http');
const httpProxy = require('http-proxy');

const BACKEND_PORT = process.env.BACKEND_PORT || 8001;
const FRONTEND_PORT = process.env.PORT || 3000;

const proxy = httpProxy.createProxyServer({
  target: `http://localhost:${BACKEND_PORT}`,
  changeOrigin: true,
  ws: true,
});

proxy.on('error', (err, req, res) => {
  console.error(`[Proxy Error] ${err.message}`);
  if (res && !res.headersSent) {
    res.writeHead(502, { 'Content-Type': 'text/html' });
    res.end(`
      <html>
        <head><title>Loading...</title>
        <meta http-equiv="refresh" content="3">
        <style>
          body { font-family: 'Lato', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #FFF5F7; color: #4A4A4A; }
          .loader { text-align: center; }
          h2 { color: #D4A5A5; }
        </style>
        </head>
        <body>
          <div class="loader">
            <h2>jayti</h2>
            <p>Starting up... Please wait a moment.</p>
          </div>
        </body>
      </html>
    `);
  }
});

const server = http.createServer((req, res) => {
  proxy.web(req, res);
});

server.on('upgrade', (req, socket, head) => {
  proxy.ws(req, socket, head);
});

server.listen(FRONTEND_PORT, '0.0.0.0', () => {
  console.log(`[JAYTI] Frontend proxy running on port ${FRONTEND_PORT} -> Django on port ${BACKEND_PORT}`);
});
