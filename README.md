# Granton Finance — granton.finance

Static site. No build step. `index.html` (homepage) + `score.html` (Deal Fundability Score, served at `/score` via cleanUrls).

## Deploy (Vercel)
1. vercel.com → Add New → Project → Import `Chadhauser/granton-site` → Deploy (framework: Other, no build command, output dir: root).
2. Project → Settings → Domains → add `granton.finance` and `www.granton.finance`.

## DNS (Namecheap → granton.finance → Advanced DNS)

### Site (Vercel)
| Type | Host | Value |
|------|------|-------|
| A | @ | 76.76.21.21 |
| CNAME | www | cname.vercel-dns.com |

### Email (Namecheap Private Email — mailbox name: `hello`)
| Type | Host | Value | Priority |
|------|------|-------|----------|
| MX | @ | mx1.privateemail.com | 10 |
| MX | @ | mx2.privateemail.com | 10 |
| TXT | @ | v=spf1 include:spf.privateemail.com ~all | — |
| TXT | _dmarc | v=DMARC1; p=none; rua=mailto:hello@granton.finance | — |
| TXT | default._domainkey | (DKIM key — copy from Private Email dashboard after enabling) | — |

DMARC starts at `p=none` (monitor mode); tighten to `quarantine` after a few clean weeks of sending.

Contact address is hard-coded as `hello@granton.finance` (one `CONTACT_EMAIL` const in `score.html`, mailto links in `index.html`).
