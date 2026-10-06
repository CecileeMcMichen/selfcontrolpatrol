const CACHE='self-control-patrol-v4-master';
const FILES=['./','./index.html','./styles.css','./game.js','./data/cards.js','./data/cards.json','./data/spaces.js','./assets/board.png','./assets/icon.svg','./AI_SESSION_ANALYSIS_TEMPLATE.md'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(Promise.all([self.clients.claim(),caches.keys().then(keys=>Promise.all(keys.filter(key=>key!==CACHE).map(key=>caches.delete(key))))])));
self.addEventListener('fetch',event=>{if(event.request.method!=='GET')return;event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request)))});
