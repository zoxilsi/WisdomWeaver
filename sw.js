const CACHE_NAME = 'wisdom-weaver-v1.0.0';
const urlsToCache = [
  '/',
  '/manifest.json',
  '/static/icon-72.png',
  '/static/icon-96.png',
  '/static/icon-128.png',
  '/static/icon-144.png',
  '/static/icon-152.png',
  '/static/icon-192.png',
  '/static/icon-384.png',
  '/static/icon-512.png',
  '/bhagavad_gita_verses.csv',
  '/Public/Images/WhatsApp Image 2024-11-18 at 11.40.34_076eab8e.jpg'
];

// Install event - cache resources
self.addEventListener('install', function(event) {
  console.log('[ServiceWorker] Install');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('[ServiceWorker] Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .then(function() {
        console.log('[ServiceWorker] Skip waiting');
        return self.skipWaiting();
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', function(event) {
  console.log('[ServiceWorker] Activate');
  event.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        if (key !== CACHE_NAME) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    }).then(function() {
      console.log('[ServiceWorker] Claiming clients');
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', function(event) {
  console.log('[ServiceWorker] Fetch', event.request.url);
  
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          console.log('[ServiceWorker] Found in cache', event.request.url);
          return response;
        }

        // Clone the request
        var fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(
          function(response) {
            // Check if we received a valid response
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response
            var responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        ).catch(function() {
          // Network failed, try to get from cache
          return caches.match(event.request);
        });
      })
  );
});

// Background sync for offline actions
self.addEventListener('sync', function(event) {
  console.log('[ServiceWorker] Background sync', event.tag);
  if (event.tag === 'wisdom-sync') {
    event.waitUntil(
      // Sync offline actions when back online
      Promise.resolve()
    );
  }
});

// Push notifications (for future daily wisdom feature)
self.addEventListener('push', function(event) {
  console.log('[ServiceWorker] Push received');
  
  const options = {
    body: event.data ? event.data.text() : 'New wisdom from Bhagavad Gita awaits you!',
    icon: '/static/icon-192.png',
    badge: '/static/icon-72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Read Wisdom',
        icon: '/static/icon-128.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/icon-72.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Wisdom Weaver', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', function(event) {
  console.log('[ServiceWorker] Notification click received.');

  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});