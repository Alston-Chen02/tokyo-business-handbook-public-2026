const CACHE='tokyo-business-2026-public-62cc524a5015';
const FILES=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install',event=>event.waitUntil((async()=>{
 const cache=await caches.open(CACHE);
 for(const file of FILES){const r=await fetch(file,{cache:'reload'});if(!r.ok)throw Error('Cannot cache app');if(file==='./'||file==='./index.html'){if(!(await r.clone().text()).includes('東京出差電子手冊'))throw Error('Not authenticated app')}else if(file.endsWith('.png')){if(!r.headers.get('content-type')?.startsWith('image/'))throw Error('Not app icon')}else{const data=await r.clone().json();if(!data.start_url)throw Error('Not app manifest')}await cache.put(file,r)}
 await self.skipWaiting();
})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{
 for(const key of await caches.keys())if(key.startsWith('tokyo-business-2026-')&&key!==CACHE)await caches.delete(key);
 await self.clients.claim();
})()));
self.addEventListener('fetch',event=>{
 const url=new URL(event.request.url);if(url.origin!==location.origin||event.request.method!=='GET')return;
 if(event.request.mode==='navigate'&&url.pathname.startsWith(new URL(self.registration.scope).pathname)){
  if(url.pathname.includes('signin')||url.pathname.includes('signout')||url.pathname.includes('callback'))return;
  event.respondWith((async()=>{try{const response=await fetch(event.request);if(response.ok&&!response.redirected&&response.headers.get('content-type')?.includes('text/html')){const copy=response.clone();if((await copy.text()).includes('東京出差電子手冊')){const c=await caches.open(CACHE);await c.put('./index.html',response.clone())}}return response}catch{return (await caches.match('./index.html'))||Response.error()}})());
 }else if(FILES.some(f=>new URL(f,self.registration.scope).href===url.href))event.respondWith(caches.match(event.request).then(r=>r||fetch(event.request)));
});
