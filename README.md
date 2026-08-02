# Granton Finance — granton.finance

Static site. No build step. `index.html` (homepage) + `score.html` (Deal Fundability Score, served at `/score` via cleanUrls).

## Deploy (Vercel)
1. vercel.com → Add New → Project → Import `Chadhauser/granton-site` → Deploy (framework: Other, no build command, output dir: root).
2. Project → Settings → Domains → add `granton.finance` and `www.granton.finance`.

## DNS (Namecheap → granton.finance → Advanced DNS)
| Type | Host | Value |
|------|------|-------|
| A | @ | 76.76.21.21 |
| CNAME | www | cname.vercel-dns.com |

## Email (choose one, then tell Claude which)
- Google Workspace: add Google's MX record (SMTP.GOOGLE.COM, priority 1), create `hello@granton.finance`.
- Namecheap Private Email: enable in Namecheap (MX auto-set), create `hello@granton.finance`.

After the mailbox exists, add SPF/DKIM/DMARC — exact records depend on the provider chosen; Claude supplies them on request.

Contact address is hard-coded as `hello@granton.finance` (one `CONTACT_EMAIL` const in `score.html`, mailto links in `index.html`).
