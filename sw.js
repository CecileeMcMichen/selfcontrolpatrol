const CACHE='self-control-patrol-v5-squad-2';
importScripts('./data/patrol-squad.js');
const SQUAD_FILES=((self.PATROL_SQUAD&&self.PATROL_SQUAD.runtimeFiles)||[]).map(file=>'./'+file);
const FILES=['./','./index.html','./styles.css','./patrol-squad.css','./game.js','./patrol-squad.js','./data/cards.js','./data/cards.json','./data/spaces.js','./data/patrol-squad.js','./assets/board.png','./assets/icon.svg','./assets/patrol-squad/manifest.json','./AI_SESSION_ANALYSIS_TEMPLATE.md',...SQUAD_FILES];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(Promise.all([self.clients.claim(),caches.keys().then(keys=>Promise.all(keys.filter(key=>key!==CACHE).map(key=>caches.delete(key))))])));
self.addEventListener('fetch',event=>{if(event.request.method!=='GET')return;event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request)))});
