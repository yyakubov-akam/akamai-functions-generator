import { AutoRouter } from 'itty-router';
import { get as getVariable } from '@spinframework/spin-variables';

const router = AutoRouter();

// ---------------------------------------------------------------------------
// CORS — allow *.agenobarb.cloud (origin is reflected so cookies/auth work)
// ---------------------------------------------------------------------------
function getAllowedOrigin(request) {
    const origin = request.headers.get('Origin') || '';
    const ok =
        origin === 'https://agenobarb.cloud' ||
        origin === 'http://agenobarb.cloud' ||
        /^https?:\/\/[^/]+\.agenobarb\.cloud$/.test(origin);
    return ok ? origin : null;
}

function withCors(response, request) {
    const allowedOrigin = getAllowedOrigin(request);
    if (!allowedOrigin) return response;
    const headers = new Headers(response.headers);
    headers.set('Access-Control-Allow-Origin', allowedOrigin);
    headers.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
    headers.set('Access-Control-Allow-Headers', 'Content-Type');
    headers.set('Vary', 'Origin');
    return new Response(response.body, { status: response.status, headers });
}

// ---------------------------------------------------------------------------
// HTML → plain text extraction (no DOM APIs available in WASM sandbox)
// ---------------------------------------------------------------------------
function extractText(html) {
    // Remove <script>…</script> and <style>…</style> blocks (and their content)
    let text = html
        .replace(/<script[\s\S]*?<\/script>/gi, ' ')
        .replace(/<style[\s\S]*?<\/style>/gi, ' ')
        .replace(/<head[\s\S]*?<\/head>/gi, ' ')
        .replace(/<noscript[\s\S]*?<\/noscript>/gi, ' ')
        // Replace block-level tags with newlines for readability
        .replace(/<\/(p|div|section|article|h[1-6]|li|tr|td|th|blockquote|pre|header|footer|main|nav|aside)>/gi, '\n')
        // Strip all remaining tags
        .replace(/<[^>]+>/g, ' ')
        // Decode common HTML entities
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&nbsp;/g, ' ')
        .replace(/&[a-z]{2,6};/gi, ' ')
        // Collapse whitespace / blank lines
        .replace(/[ \t]+/g, ' ')
        .replace(/\n{3,}/g, '\n\n')
        .trim();

    return text;
}

// ---------------------------------------------------------------------------
// Route: OPTIONS /scrape  — CORS preflight
// ---------------------------------------------------------------------------
router.options('/scrape', (request) => {
    const allowedOrigin = getAllowedOrigin(request);
    if (!allowedOrigin) return new Response(null, { status: 204 });
    return new Response(null, {
        status: 204,
        headers: {
            'Access-Control-Allow-Origin': allowedOrigin,
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '86400',
            'Vary': 'Origin',
        },
    });
});

// ---------------------------------------------------------------------------
// Route: GET /scrape?url=<target>
// ---------------------------------------------------------------------------
router.get('/scrape', async (request, { ollamaUrl, model }) => {
    const targetUrl = new URL(request.url).searchParams.get('url');
    if (!targetUrl) {
        return withCors(
            new Response(
                JSON.stringify({ error: 'Missing required query parameter: url' }),
                { status: 400, headers: { 'content-type': 'application/json' } }
            ),
            request
        );
    }

    // --- 1. Fetch the target page ---
    let pageHtml;
    try {
        const pageRes = await fetch(targetUrl, {
            headers: { 'User-Agent': 'AkamaiScraper/1.0' },
        });
        if (!pageRes.ok) {
            return withCors(
                new Response(
                    JSON.stringify({ error: `Failed to fetch target URL: ${pageRes.status} ${pageRes.statusText}` }),
                    { status: 502, headers: { 'content-type': 'application/json' } }
                ),
                request
            );
        }
        pageHtml = await pageRes.text();
    } catch (err) {
        return withCors(
            new Response(
                JSON.stringify({ error: `Network error fetching target URL: ${String(err)}` }),
                { status: 502, headers: { 'content-type': 'application/json' } }
            ),
            request
        );
    }

    // --- 2. Extract and truncate text (keep within model context / 30s budget) ---
    const rawText = extractText(pageHtml);
    // Truncate to ~8 000 chars to stay well within the 30s request limit
    const pageText = rawText.length > 8000 ? rawText.slice(0, 8000) + '\n[...truncated]' : rawText;

    // --- 3. Call Ollama ---
    const prompt =
        `You are a helpful assistant. Below is the extracted text content of a web page at: ${targetUrl}\n\n` +
        `--- PAGE CONTENT START ---\n${pageText}\n--- PAGE CONTENT END ---\n\n` +
        `Please:\n` +
        `1. Briefly explain what this site / page is about.\n` +
        `2. Summarize the key information presented on the page.\n\n` +
        `Be concise and clear.`;

    let aiResponse;
    try {
        const aiRes = await fetch(`${ollamaUrl}/api/generate`, {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({
                model,
                prompt,
                stream: false,
                options: { num_predict: 512 },
            }),
        });
        if (!aiRes.ok) {
            const errBody = await aiRes.text();
            return withCors(
                new Response(
                    JSON.stringify({ error: `Ollama error: ${aiRes.status} ${aiRes.statusText}`, detail: errBody }),
                    { status: 502, headers: { 'content-type': 'application/json' } }
                ),
                request
            );
        }
        const aiJson = await aiRes.json();
        aiResponse = aiJson.response ?? JSON.stringify(aiJson);
    } catch (err) {
        return withCors(
            new Response(
                JSON.stringify({ error: `Network error calling Ollama: ${String(err)}` }),
                { status: 502, headers: { 'content-type': 'application/json' } }
            ),
            request
        );
    }

    return withCors(
        new Response(
            JSON.stringify({ url: targetUrl, summary: aiResponse }),
            { status: 200, headers: { 'content-type': 'application/json' } }
        ),
        request
    );
});

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------
addEventListener('fetch', async (event) => {
    const ollamaUrl = getVariable('ollama_url');
    const model = getVariable('model');

    if (!ollamaUrl || !model) {
        event.respondWith(new Response(
            JSON.stringify({ error: 'Function not configured: ollama_url or model variable missing' }),
            { status: 500, headers: { 'content-type': 'application/json' } }
        ));
        return;
    }

    event.respondWith(router.fetch(event.request, { ollamaUrl, model }));
});

