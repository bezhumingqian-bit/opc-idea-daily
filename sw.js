// OPC IDEA Daily · Service Worker
// Strategy: stale-while-revalidate for fast perceived load, with offline fallback

const CACHE_NAME = 'opc-idea-v1';
const OFFLINE_URL = '/opc-idea-daily/';

const PRECACHE_URLS = [
  '/opc-idea-daily/',
  '/opc-idea-daily/index.html',
  '/opc-idea-daily/feed.xml',
  '/opc-idea-daily/manifest.json',
  '/opc-idea-daily/icon-192.png',
  '/opc-idea-daily/icon-512.png'
];

// Install: pre-cache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(PRECACHE_URLS).catch(err => {
        console.warn('[SW] Pre-cache partial:', err);
      });
    })
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(names => {
      return Promise.all(
        names
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Fetch: stale-while-revalidate for same-origin GET
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  if (url.origin !== location.origin) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(cache => {
      return cache.match(event.request).then(cached => {
        const fetchPromise = fetch(event.request)
          .then(response => {
            if (response && response.status === 200) {
              cache.put(event.request, response.clone());
            }
            return response;
          })
          .catch(() => {
            if (event.request.mode === 'navigate') {
              return cache.match(OFFLINE_URL);
            }
            return cached;
          });
        return cached || fetchPromise;
      });
    })
  );
});