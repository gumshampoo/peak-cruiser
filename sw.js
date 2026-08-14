// Cache-first tile cache for Peak Cruiser. Persists OpenTopoMap imagery and
// ArcGIS elevation terrain responses in Cache Storage indefinitely (no TTL,
// no eviction logic) so a previously-visited area loads instantly on repeat
// visits instead of re-fetching from the network every time.
const CACHE_NAME = 'peak-cruise-tiles-v1';
// endsWith, not exact match: OpenTopoMap uses lettered subdomains
// (a/b/c.tile.opentopomap.org) for the same tiles.
const CACHEABLE_HOST_SUFFIXES = [
  'tile.opentopomap.org',       // 3D globe imagery
  'cyberjapandata.gsi.go.jp',   // GSI relief / hillshade / photo / pale / std
  'tile.openstreetmap.org',     // minimap imagery
  'elevation3d.arcgis.com',     // terrain elevation
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (!CACHEABLE_HOST_SUFFIXES.some((h) => url.hostname === h || url.hostname.endsWith('.' + h))) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(async (cache) => {
      const cached = await cache.match(event.request);
      if (cached) return cached;
      const response = await fetch(event.request);
      // Opaque (no-cors, cross-origin) responses are still cacheable and
      // replayable even though their contents aren't readable here.
      if (response.ok || response.type === 'opaque') {
        cache.put(event.request, response.clone());
      }
      return response;
    })
  );
});
