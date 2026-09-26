// api/enquiry.js — receives commercial mortgage calculator enquiries
// Set these environment variables in Vercel project settings:
//   RESEND_API_KEY       from resend.com (free tier: 3,000 emails/month)
//   NOTIFY_EMAIL         where enquiries land, e.g. hello@granton.finance
//   FROM_EMAIL           a verified sender on the domain
//   ALLOWED_ORIGIN       https://granton.finance
//   SUPABASE_URL         optional — if set, enquiries are also stored
//   SUPABASE_SERVICE_KEY optional — service role key, server-side only

const RATE = new Map();
const WINDOW_MS = 60 * 60 * 1000;
const MAX_PER_IP = 5;

function clean(v, max) {
  return String(v == null ? '' : v).replace(/[\u0000-\u001F\u007F]/g, '').trim().slice(0, max);
}
function validEmail(e) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e) && e.length <= 254;
}
function money(v) {
  const n = Number(v);
  return Number.isFinite(n) && n >= 0 && n < 1e10 ? n : 0;
}

export default async function handler(req, res) {
  const origin = process.env.ALLOWED_ORIGIN || 'https://granton.finance';
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  const now = Date.now();
  const hits = (RATE.get(ip) || []).filter(t => now - t < WINDOW_MS);
  if (hits.length >= MAX_PER_IP) {
    return res.status(429).json({ error: 'Too many enquiries. Please email hello@granton.finance instead.' });
  }
  hits.push(now);
  RATE.set(ip, hits);

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { return res.status(400).json({ error: 'Bad request' }); }
  }
  if (!body || typeof body !== 'object') return res.status(400).json({ error: 'Bad request' });

  // Honeypot — hidden field that only bots fill in
  if (clean(body.website, 50)) return res.status(200).json({ ok: true });

  const name = clean(body.name, 100);
  const email = clean(body.email, 254);
  const phone = clean(body.phone, 40);

  if (!name) return res.status(400).json({ error: 'Name is required' });
  if (!validEmail(email)) return res.status(400).json({ error: 'A valid email is required' });

  const enquiry = {
    name, email, phone,
    loan: money(body.loan),
    property_value: money(body.value),
    rate: Number(body.rate) || 0,
    term_years: Number(body.term) || 0,
    annual_rent: money(body.rent),
    repayment_type: body.repayment === 'interest' ? 'interest_only' : 'repayment',
    monthly_payment: clean(body.monthly, 40),
    ltv: clean(body.ltv, 20),
    cover: clean(body.cover, 20),
    cover_stressed: clean(body.coverStressed, 20),
    source: clean(body.source, 200),
    ip,
    user_agent: clean(req.headers['user-agent'], 300),
    created_at: new Date().toISOString()
  };

  const results = { emailed: false, stored: false };

  if (process.env.RESEND_API_KEY && process.env.NOTIFY_EMAIL && process.env.FROM_EMAIL) {
    const lines = [
      `Name:    ${enquiry.name}`,
      `Email:   ${enquiry.email}`,
      `Phone:   ${enquiry.phone || '-'}`,
      ``,
      `Loan:    GBP ${enquiry.loan.toLocaleString('en-GB')}`,
      `Value:   GBP ${enquiry.property_value.toLocaleString('en-GB')}`,
      `Rate:    ${enquiry.rate}%`,
      `Term:    ${enquiry.term_years} years`,
      `Basis:   ${enquiry.repayment_type === 'interest_only' ? 'Interest only' : 'Capital & interest'}`,
      `Rent:    GBP ${enquiry.annual_rent.toLocaleString('en-GB')}`,
      ``,
      `Monthly: ${enquiry.monthly_payment}`,
      `LTV:     ${enquiry.ltv}`,
      `Cover:   ${enquiry.cover}  (stressed ${enquiry.cover_stressed})`,
      ``,
      `Page:    ${enquiry.source}`,
      `Time:    ${enquiry.created_at}`
    ].join('\n');

    try {
      const r = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from: process.env.FROM_EMAIL,
          to: process.env.NOTIFY_EMAIL,
          reply_to: enquiry.email,
          subject: `Commercial mortgage enquiry - ${enquiry.name}, GBP ${enquiry.loan.toLocaleString('en-GB')}`,
          text: lines
        })
      });
      results.emailed = r.ok;
    } catch (e) {
      results.emailed = false;
    }
  }

  if (process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_KEY) {
    try {
      const r = await fetch(`${process.env.SUPABASE_URL}/rest/v1/enquiries`, {
        method: 'POST',
        headers: {
          'apikey': process.env.SUPABASE_SERVICE_KEY,
          'Authorization': `Bearer ${process.env.SUPABASE_SERVICE_KEY}`,
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify(enquiry)
      });
      results.stored = r.ok;
    } catch (e) {
      results.stored = false;
    }
  }

  if (!results.emailed && !results.stored) {
    console.error('ENQUIRY NOT CAPTURED', enquiry);
    return res.status(502).json({ error: 'Could not send. Please email hello@granton.finance directly.' });
  }

  return res.status(200).json({ ok: true });
}
