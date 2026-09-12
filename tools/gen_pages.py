import re, json, html

TPL = 'how-does-a-bridging-loan-work.html'

def make(slug, title, desc, stand, body):
    s = open(TPL, encoding='utf-8').read()
    url = 'https://granton.finance/' + slug
    s = re.sub(r'<title>.*?</title>', '<title>%s | Granton Finance</title>' % html.escape(title), s, 1)
    s = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="%s">' % html.escape(desc, quote=True), s, 1)
    s = re.sub(r'<link rel="canonical" href=".*?">', '<link rel="canonical" href="%s">' % url, s, 1)
    s = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="%s">' % html.escape(title + ' | Granton Finance', quote=True), s, 1)
    s = re.sub(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="%s">' % html.escape(desc, quote=True), s, 1)
    s = re.sub(r'<meta property="og:url" content=".*?">', '<meta property="og:url" content="%s">' % url, s, 1)
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "url": url,
          "datePublished": "2026-09-13",
          "author": {"@type": "Person", "name": "Peter Edwards", "honorificSuffix": "ACMA CGMA"},
          "publisher": {"@type": "Organization", "name": "Granton Finance", "url": "https://granton.finance/"},
          "isPartOf": {"@type": "WebSite", "name": "Granton Finance", "url": "https://granton.finance/"}}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), s, 1, flags=re.S)
    doc = re.search(r'(<div class="doc">)(.*?)(  <div class="cta">)', s, re.S)
    new = '\n  <div class="eyebrow">Plainly explained</div>\n  <h1>%s</h1>\n  <p class="stand">%s</p>\n\n%s\n' % (title, stand, body)
    s = s[:doc.start(2)] + new + s[doc.start(3):]
    open(slug + '.html', 'w', encoding='utf-8').write(s)

BODY = """  <h2>The answer in forty words</h2>
  <p>A commercial bridging loan typically completes in two to four weeks. A well-prepared case on a straightforward property can complete in five to ten working days; a genuinely fast bridge in under a week is possible but costs more. The file, not the lender, sets the speed.</p>

  <h2>Where the time actually goes</h2>
  <p>Lenders are not slow. What is slow is everything they wait for. A bridging application passes through five gates, and each one can take a day or a fortnight depending on how prepared you are:</p>
  <ol>
    <li><strong>Terms</strong> — one to two days. With a clear summary of the deal, the security and the exit, an indicative offer comes back quickly.</li>
    <li><strong>Valuation</strong> — three days to two weeks. The single biggest variable. A surveyor has to be instructed, get access, inspect and report. Access problems and unusual assets add a week.</li>
    <li><strong>Underwriting</strong> — two to five days once the valuation is in. Identity, source of funds, the borrowing company’s position, and the exit evidence.</li>
    <li><strong>Legals</strong> — one to three weeks. The lender’s solicitors and yours: title, searches, the charge, and the legal advice the lender requires the borrower to have taken. Solicitors who don’t do bridging regularly are the commonest cause of a slow completion.</li>
    <li><strong>Completion</strong> — a day. Funds are released once the charge is ready to register.</li>
  </ol>

  <h2>How to make it fast</h2>
  <ul>
    <li><strong>Arrive with the file done.</strong> Company accounts, bank statements, ID for the directors, a schedule of the security, and the exit evidenced in writing. A pre-underwritten case skips the query-and-wait cycles that add weeks. This is what we prepare as standard.</li>
    <li><strong>Sort valuation access before instructing.</strong> Keys, a tenant who’ll open the door, a contact number the surveyor can actually reach.</li>
    <li><strong>Use solicitors who do this every week.</strong> Ask them how many bridging completions they’ve done this year. If the answer is vague, use someone else — we can suggest firms who turn these round in days.</li>
    <li><strong>Consider a desktop or automated valuation</strong> where the lender will accept one. On standard residential or simple commercial property it removes the longest step.</li>
    <li><strong>Choose the lender for the deadline, not the rate.</strong> Some lenders have in-house legal teams and a five-day track record; they charge for it. On a 28-day auction completion, that premium is cheaper than losing the deposit.</li>
  </ul>

  <h2>What "fast bridging loan" really means</h2>
  <p>Advertised "24-hour" and "48-hour" bridging exists, but read the small print: it usually means terms within 24 hours, not money. Real completions in under five working days happen when the security is simple, the loan-to-value is modest, a desktop valuation is acceptable, both sets of solicitors are bridging specialists, and the borrower answers every question the same day. Expect to pay a higher monthly rate and a larger arrangement fee for that speed. If you have three weeks, you don’t need a fast bridge — you need a well-run ordinary one, and it will be cheaper.</p>

  <h2>Timescales by situation</h2>
  <ul>
    <li><strong><a href="/auction-bridging-finance">Auction purchase</a></strong> — 28 days to complete, so the bridge must be arranged in three weeks. Achievable if you start the day the hammer falls, or better, before the auction.</li>
    <li><strong><a href="/vat-bridging-loan">VAT on a commercial purchase</a></strong> — usually aligned to the completion date of the main purchase; two to three weeks.</li>
    <li><strong><a href="/refurbishment-bridging-loan">Refurbishment</a></strong> — two to four weeks; lenders want to see the schedule of works and costings.</li>
    <li><strong><a href="/land-bridging-loan">Land</a></strong> — three to six weeks; valuation and title are slower on land, especially with agricultural tenancies or planning in play.</li>
    <li><strong><a href="/second-charge-bridging-loan">Second charge</a></strong> — add a week for the first-charge lender’s consent.</li>
  </ul>

  <h2>The realistic plan</h2>
  <p>Count back from your deadline. Allow a week for legals at the end, a week for valuation in the middle, and two days at the start for terms. Whatever’s left is your margin — and if there’s none, tell your broker on day one, because that changes which lender we go to. What the money costs is in <a href="/how-much-does-a-bridging-loan-cost">how much does a bridging loan cost</a>; the mechanics are in <a href="/how-does-a-bridging-loan-work">how a bridging loan works</a>.</p>
"""

make('how-long-does-a-bridging-loan-take', 'How long does a bridging loan take?',
     'Commercial bridging usually completes in two to four weeks; a prepared case can complete in five to ten working days. Where the time goes, how to make it fast, what "24-hour bridging" really means, and timescales by situation.',
     'Two to four weeks is normal, under two is achievable, under one is possible at a price. Here is where the time actually goes, how to compress it, and what a genuinely fast bridging loan involves.',
     BODY)

s = open('sitemap.xml').read()
old = '  <url><loc>https://granton.finance/how-does-a-bridging-loan-work</loc>'
if 'how-long-does-a-bridging-loan-take' not in s:
    s = s.replace(old, '  <url><loc>https://granton.finance/how-long-does-a-bridging-loan-take</loc><lastmod>2026-09-13</lastmod><priority>0.9</priority></url>\n' + old)
    open('sitemap.xml', 'w').write(s)

s = open('index.html', encoding='utf-8').read()
old = '      <a href="/how-does-a-bridging-loan-work">How does a bridging loan work?</a>'
if 'how-long-does-a-bridging-loan-take' not in s:
    s = s.replace(old, '      <a href="/how-long-does-a-bridging-loan-take">How long does a bridging loan take?</a>\n' + old)
    open('index.html', 'w', encoding='utf-8').write(s)
