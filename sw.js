const CACHE_NAME = 'vaspera-cache-v1';
const FILES_TO_CACHE = [
  '/',
  '/templates/index.html'
];

// Handles the background installation process
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
});

// Necessary fetch listener to trigger the native mobile download banner
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request);
    })
  );
});

