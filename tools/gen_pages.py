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
          "datePublished": "2026-09-12",
          "author": {"@type": "Person", "name": "Peter Edwards", "honorificSuffix": "ACMA CGMA"},
          "publisher": {"@type": "Organization", "name": "Granton Finance", "url": "https://granton.finance/"},
          "isPartOf": {"@type": "WebSite", "name": "Granton Finance", "url": "https://granton.finance/"}}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), s, 1, flags=re.S)
    doc = re.search(r'(<div class="doc">)(.*?)(  <div class="cta">)', s, re.S)
    new = '\n  <div class="eyebrow">Plainly explained</div>\n  <h1>%s</h1>\n  <p class="stand">%s</p>\n\n%s\n' % (title, stand, body)
    s = s[:doc.start(2)] + new + s[doc.start(3):]
    open(slug + '.html', 'w', encoding='utf-8').write(s)

BODY1 = """  <h2>The answer in forty words</h2>
  <p>A bridging loan is a short-term loan, secured on property, that covers the gap between a deadline you cannot move and money that is on its way. It runs for months rather than years, is priced monthly, and is repaid in one go from a defined exit — a sale, a refinance or a receipt.</p>

  <h2>What makes it different from a mortgage or a business loan</h2>
  <ul>
    <li><strong>Term</strong> — three to eighteen months is typical, twenty-four at the outside. A mortgage runs for decades; a business loan for years.</li>
    <li><strong>Speed</strong> — days to a few weeks. Lenders underwrite the security and the exit, not three years of trading history.</li>
    <li><strong>Pricing</strong> — quoted as a monthly rate, commonly between 0.6% and 1.2% a month for commercial bridging, plus fees. Dearer than term money, because it is faster and shorter.</li>
    <li><strong>Repayment</strong> — usually nothing monthly. Interest is retained or rolled up and the whole balance is repaid at the end from the exit.</li>
    <li><strong>Purpose</strong> — a timing problem. If the need is really long-term money, bridging is the wrong tool and will cost you a premium to find that out.</li>
  </ul>

  <h2>How it works, step by step</h2>
  <ol>
    <li><strong>You have a deadline</strong> — an auction completion, a purchase before your sale completes, a VAT bill on a commercial property, a refurbishment that has to finish before a mortgage lender will lend.</li>
    <li><strong>You have security</strong> — the property being bought, one you already own, or both. The lender takes a legal charge over it.</li>
    <li><strong>You have an exit</strong> — the specific, evidenced event that repays the loan. This is what the lender really underwrites.</li>
    <li><strong>The lender values the security</strong> and offers a loan-to-value, usually 65–75% for commercial property.</li>
    <li><strong>Funds are released</strong>, often with the interest for the expected term deducted up front, and the clock starts.</li>
    <li><strong>The exit happens</strong> and the loan, plus interest and any exit fee, is repaid in one payment.</li>
  </ol>

  <h2>What it costs</h2>
  <p>Three things: the monthly interest, an arrangement fee of around 2% of the loan, and the professional costs — valuation, the lender's solicitors and your own. Some lenders add an exit fee. The headline rate is only part of the picture; on a six-month bridge the fees can matter more than the rate, which is why we cost the whole loan over your realistic term before recommending anything. There is a fuller breakdown in <a href="/how-much-does-a-bridging-loan-cost">how much does a bridging loan cost</a>.</p>

  <h2>Regulated or unregulated?</h2>
  <p>If the security is a home you or a family member lives in, the loan is regulated consumer lending. If the borrower is a business and the security is commercial or investment property, it is unregulated commercial lending — the market we arrange in. We work with limited companies; we do not advise on or arrange consumer credit, and nothing on this page is regulated financial advice. More on this in <a href="/unregulated-bridging-loan">unregulated bridging loans</a>.</p>

  <h2>Who uses bridging, and for what</h2>
  <ul>
    <li><strong><a href="/auction-bridging-finance">Auction buyers</a></strong> — exchange on the hammer, complete in 28 days.</li>
    <li><strong><a href="/vat-bridging-loan">Commercial property buyers</a></strong> funding the VAT until HMRC repays it.</li>
    <li><strong><a href="/refurbishment-bridging-loan">Developers and landlords</a></strong> funding works before refinancing on the improved value.</li>
    <li><strong>Businesses buying before selling</strong> — new premises before the old ones complete.</li>
    <li><strong><a href="/land-bridging-loan">Landowners</a></strong> funding a purchase, a planning application or a tax bill against land.</li>
    <li><strong>Owners raising capital quickly</strong> against property they already hold, sometimes as a <a href="/second-charge-bridging-loan">second charge</a>.</li>
  </ul>

  <h2>The question to answer before anything else</h2>
  <p>How is it repaid? A credible exit is specific and evidenced — a sale in solicitors’ hands, a refinance with an agreement in principle, a VAT reclaim with the computation done. If you cannot answer that in one sentence, you are not ready to bridge, and an honest adviser will say so. If you can, a well-prepared case can be funded in days. The mechanics — interest types, timing, the exit in detail — are in <a href="/how-does-a-bridging-loan-work">how does a bridging loan work</a>.</p>
"""

BODY2 = """  <h2>The answer in forty words</h2>
  <p>A commercial bridging loan typically costs between 0.6% and 1.2% a month in interest, plus an arrangement fee of around 2%, a valuation, and legal fees on both sides. On a £300,000 loan over six months, expect a total cost in the region of £22,000–£34,000.</p>

  <h2>The four parts of the cost</h2>
  <ul>
    <li><strong>Interest</strong> — quoted monthly, not annually. 0.6–0.9% a month for straightforward commercial security at sensible loan-to-value; 1% or more for heavier LTV, unusual assets, weaker exits or the fastest completions.</li>
    <li><strong>Arrangement fee</strong> — commonly 2% of the loan, sometimes 1–1.5% on larger cases, usually added to the loan rather than paid up front.</li>
    <li><strong>Professional fees</strong> — the lender’s valuation (£1,000–£3,000 on commercial property), the lender’s solicitors (£1,500–£3,000) and your own solicitors. Some lenders charge an administration or exit fee of around 1%.</li>
    <li><strong>Broker fee</strong> — some brokers charge the borrower; we are remunerated by the lender on completion and tell you the amount, so our fee does not sit on top of the cost of the money.</li>
  </ul>

  <h2>A worked example</h2>
  <p>£300,000 bridge, six months, 0.85% a month, 2% arrangement fee, interest retained:</p>
  <ul>
    <li>Interest: £300,000 × 0.85% × 6 = <strong>£15,300</strong></li>
    <li>Arrangement fee: <strong>£6,000</strong></li>
    <li>Valuation and legals, both sides: roughly <strong>£5,000</strong></li>
    <li><strong>Total: about £26,300</strong>, or 8.8% of the loan for six months’ money.</li>
  </ul>
  <p>If the exit slips by three months, add another £7,650 of interest plus any extension fee. This is why the exit is the number that actually sets the cost.</p>

  <h2>Retained, rolled up or serviced — which is cheapest?</h2>
  <p><strong>Serviced</strong> interest (paid monthly) is cheapest overall because nothing compounds, but the lender has to be satisfied you can afford the payments. <strong>Retained</strong> interest is deducted from the advance on day one, so you receive less but pay nothing monthly. <strong>Rolled-up</strong> interest accrues onto the balance and compounds, so it is the dearest if the term runs long. For most commercial borrowers with a firm exit, retained is the practical choice.</p>

  <h2>What pushes the price up</h2>
  <ul>
    <li><strong>Loan-to-value</strong> — above 65–70% the rate steps up quickly.</li>
    <li><strong>The exit</strong> — a sale in solicitors’ hands prices better than “we’ll refinance”.</li>
    <li><strong>The asset</strong> — offices and industrial units price better than land without planning, licensed premises or part-built schemes.</li>
    <li><strong>Speed</strong> — a five-day completion costs more than a three-week one.</li>
    <li><strong>The file</strong> — a case that arrives pre-underwritten, with valuation access, solicitors instructed and the exit evidenced, avoids the delays that turn into extension fees.</li>
  </ul>

  <h2>How to compare two offers</h2>
  <p>Never compare headline rates. Compare the total cost of the money over your realistic term, including every fee, and then ask what happens to that number if the exit slips three months. A 0.75% offer with a 2% fee and a 1% exit fee is frequently dearer over six months than a 0.9% offer with no exit fee. We run that arithmetic on every case before anything is recommended — it is the part of the job a chartered accountant is for.</p>

  <h2>Is it worth it?</h2>
  <p>Bridging earns its cost when the profit or the saving it unlocks clearly exceeds the price of the money — an auction bargain, a VAT reclaim, a purchase that would otherwise be lost, works that lift a property’s value. It does not earn its cost as a substitute for long-term finance or as a way to fund trading losses. If the honest need is three-year money, we will say so. Start with <a href="/what-is-a-bridging-loan">what a bridging loan is</a> or the mechanics in <a href="/how-does-a-bridging-loan-work">how a bridging loan works</a>.</p>
"""

make('what-is-a-bridging-loan', 'What is a bridging loan?',
     'A bridging loan is short-term, property-secured finance that covers the gap between a fixed deadline and money that is on its way. What it is, what it costs, who uses it and the one question to answer first.',
     'Short-term, secured, repaid in one go from a defined exit. Here is what a bridging loan actually is, how it differs from a mortgage or business loan, and when it is the right tool.',
     BODY1)

make('how-much-does-a-bridging-loan-cost', 'How much does a bridging loan cost?',
     'Commercial bridging costs 0.6–1.2% a month plus a ~2% arrangement fee, valuation and legals. A worked £300,000 example, what pushes the price up, and how to compare two offers properly.',
     'Interest, arrangement fee, valuation, legals, and the exit that quietly decides the total. A worked example and the honest way to compare offers.',
     BODY2)

s = open('sitemap.xml').read()
old = '  <url><loc>https://granton.finance/how-does-a-bridging-loan-work</loc>'
if 'what-is-a-bridging-loan' not in s:
    s = s.replace(old, '  <url><loc>https://granton.finance/what-is-a-bridging-loan</loc><lastmod>2026-09-12</lastmod><priority>0.9</priority></url>\n  <url><loc>https://granton.finance/how-much-does-a-bridging-loan-cost</loc><lastmod>2026-09-12</lastmod><priority>0.9</priority></url>\n' + old)
    open('sitemap.xml', 'w').write(s)

s = open('index.html', encoding='utf-8').read()
old = '      <a href="/how-does-a-bridging-loan-work">How does a bridging loan work?</a>'
if 'what-is-a-bridging-loan' not in s:
    s = s.replace(old, '      <a href="/what-is-a-bridging-loan">What is a bridging loan?</a>\n      <a href="/how-much-does-a-bridging-loan-cost">How much does a bridging loan cost?</a>\n' + old)
    open('index.html', 'w', encoding='utf-8').write(s)
