#!/usr/bin/env node
/**
 * 本地静态服务器 —— 还原线上 mimo.xiaomi.com 的路由行为：
 *   /coder/index.html[?...]  -> 301 /coder/index     （query 剥离，线上实测）
 *   /coder/index[?...]       -> 301 /coder
 *   /coder                   -> 200 coder/index.html（保留 query，?lang= 生效）
 *   /mimocode, /, /index.html-> 200 壳页（iframe src=/coder/index.html?lang=en）
 *   /coder/assets/*          -> 静态资产
 * 用法: node tools/serve.mjs [port]   （默认 8123，根目录=site/）
 */
import http from "node:http";
import { createReadStream, existsSync, statSync } from "node:fs";
import { extname, join, posix } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("../site", import.meta.url));
const PORT = Number(process.argv[2] || 8123);

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
  ".ico": "image/x-icon",
};

function send(res, code, body, headers = {}) {
  res.writeHead(code, headers);
  res.end(body);
}

function serveFile(res, abs) {
  if (!existsSync(abs) || !statSync(abs).isFile()) return send(res, 404, "not found");
  res.writeHead(200, { "Content-Type": MIME[extname(abs)] || "application/octet-stream" });
  createReadStream(abs).pipe(res);
}

http
  .createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${PORT}`);
    // URL 路径统一使用正斜杠，避免 Windows normalize 将其转成反斜杠。
    const path = posix.normalize(decodeURIComponent(url.pathname)).replace(/^(\.\.[/\\])+/, "");

    // 线上 301 链：/coder/index.html -> /coder/index -> /coder（丢 query）
    if (path === "/coder/index.html") return send(res, 301, "", { Location: "/coder/index" });
    if (path === "/coder/index") return send(res, 301, "", { Location: "/coder" });

    if (path === "/coder" || path === "/coder/") return serveFile(res, join(ROOT, "coder/index.html"));
    if (path === "/mimocode" || path === "/" || path === "/index.html")
      return serveFile(res, join(ROOT, "index.html"));

    return serveFile(res, join(ROOT, path));
  })
  .listen(PORT, () => console.log(`mimo-code-homepage-replica serving http://localhost:${PORT}/mimocode`));
