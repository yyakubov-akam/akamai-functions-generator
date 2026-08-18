import { AutoRouter } from 'itty-router';

const router = AutoRouter();

const REDIRECT_TARGET = 'https://example.com';

router.all('*', () => {
  return new Response(null, {
    status: 302,
    headers: {
      Location: REDIRECT_TARGET,
    },
  });
});

addEventListener('fetch', (event) => {
  event.respondWith(router.fetch(event.request));
});
