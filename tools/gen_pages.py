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
    doc = re.search(r'(<div class="doc">)(.*?)(  <div class="related">)', s, re.S)
    new = '\n  <div class="eyebrow">Plainly explained</div>\n  <h1>%s</h1>\n  <p class="stand">%s</p>\n\n%s\n' % (title, stand, body)
    s = s[:doc.start(2)] + new + s[doc.start(3):]
    rel = [('business-acquisition-loan', 'Business acquisition loans: how deals get funded'),
           ('management-buyout-funding', 'Management buyout funding'),
           ('mbo-calculator', 'Management buyout calculator'),
           ('buying-out-a-business-partner', 'Buying out a business partner'),
           ('small-business-invoice-finance', 'Invoice finance for a small business'),
           ('score', 'Fundability score: could your deal be funded?')]
    s = re.sub(r'(<div class="related">\s*<p class="rt">Related guides</p>\s*<ul>).*?(</ul>)',
               lambda m: m.group(1) + '\n' + ''.join('      <li><a href="/%s">%s</a></li>\n' % r for r in rel) + '    ' + m.group(2), s, 1, flags=re.S)
    open(slug + '.html', 'w', encoding='utf-8').write(s)

BODY = """  <h2>The answer in forty words</h2>
  <p>You buy a business with no money by making the business pay for itself: the seller defers part of the price, a lender advances money against the business\u2019s own assets and cash flow, and you put in effort and a personal guarantee instead of cash. It works when the business is profitable and the seller wants a clean exit more than a cheque on day one.</p>

  <h2>What "no money" actually means to a lender</h2>
  <p>No lender funds 100% of a purchase price for a buyer with nothing at stake. But "money" doesn\u2019t have to mean cash in your account. What a lender needs is <em>skin in the game</em> and a <em>repayment source</em>. The repayment source is the business you\u2019re buying. Skin in the game can be a personal guarantee, a charge over property you own, sweat equity that the seller recognises, or a seller who is so keen to sell that they finance you themselves. The buyers who succeed with little cash are the ones who assemble those pieces before they approach anyone.</p>

  <h2>The five pieces of the stack</h2>
  <ol>
    <li><strong>Deferred consideration.</strong> The seller accepts part of the price \u2014 commonly 20\u201350% \u2014 paid over one to three years from the business\u2019s profits. This is the single biggest lever and it is far more common than buyers assume, especially in retirement sales where there is no other buyer waiting. It also aligns the seller with the handover going well.</li>
    <li><strong>Earn-out.</strong> A further slice of the price paid only if the business hits agreed numbers after completion. Lets you pay for performance that hasn\u2019t happened yet without borrowing for it.</li>
    <li><strong>Cash-flow lending.</strong> A term loan, typically two to three times the business\u2019s sustainable annual profit, secured on the business and repaid from its cash flow. Lenders want three years of accounts, a buyer with relevant experience, and a plan that shows the loan serviced with headroom.</li>
    <li><strong>Asset finance.</strong> Money against what the business owns \u2014 <a href="/small-business-invoice-finance">invoice finance</a> against its debtor book, and refinancing of vehicles, plant or property. This often releases cash on completion that goes straight to the seller.</li>
    <li><strong>Your contribution.</strong> Anything from 5% to 20% of the price, sometimes as little as the professional fees. Where it doesn\u2019t exist in cash, it comes from a personal guarantee, a second charge on your home, or a family loan. Every lender will ask what you\u2019re putting in; "nothing" ends the conversation.</li>
  </ol>

  <h2>A worked example</h2>
  <p>A £600,000 business with £150,000 of sustainable annual profit and £120,000 of debtors:</p>
  <ul>
    <li>Cash-flow term loan at 2.5\u00d7 profit: <strong>£300,000</strong></li>
    <li>Invoice finance releasing 80% of debtors on completion: <strong>£96,000</strong></li>
    <li>Deferred consideration over three years: <strong>£150,000</strong></li>
    <li>Earn-out on hitting current profit for two years: <strong>£30,000</strong></li>
    <li>Buyer\u2019s contribution: <strong>£24,000</strong> \u2014 the fees, essentially</li>
  </ul>
  <p>The business services roughly £55,000 a year of term-loan repayments and £50,000 of deferred consideration from £150,000 of profit, leaving £45,000 of headroom before the buyer draws anything. That headroom is what the lender is actually underwriting.</p>

  <h2>Which sellers say yes</h2>
  <p>Owners retiring with no successor; businesses that have been on the market a while; sellers who care who takes the business on; any deal where the alternative is closing the doors. A seller who needs every pound on completion \u2014 to fund a purchase of their own, say \u2014 is the wrong seller for this structure, and it\u2019s better to find that out in the first conversation than the last.</p>

  <h2>What kills these deals</h2>
  <ul>
    <li><strong>Buying a business that doesn\u2019t make money.</strong> The whole structure rests on profit; a turnaround needs cash you don\u2019t have.</li>
    <li><strong>Overpaying.</strong> If the price is 5\u00d7 profit, no stack services it. Deferred consideration doesn\u2019t make an expensive business cheap; it only moves the bill.</li>
    <li><strong>No relevant experience.</strong> Lenders back people who\u2019ve run something like this before, or who are keeping the management team that has.</li>
    <li><strong>A plan that only works if everything goes right.</strong> Show the loan serviced at 80% of current profit and you\u2019re credible. Show it serviced at 120% and you\u2019re not.</li>
  </ul>

  <h2>Where a broker earns their keep</h2>
  <p>Assembling five sources of money around one deal, in the right order, with each lender comfortable about the others, is the job. As chartered accountants we pre-underwrite the case \u2014 sustainable profit, debt capacity, the sensible split between lender, seller and buyer \u2014 before it goes anywhere, so it arrives at the lender already answering the credit committee\u2019s questions. Our <a href="/business-acquisition-loan">acquisition-loan guide</a> covers the lending side in more depth, and the <a href="/mbo-calculator">buyout calculator</a> gives you rough numbers on your own deal in two minutes.</p>

  <h2>The honest disclaimer</h2>
  <p>We arrange commercial finance for limited companies; we do not advise on or arrange consumer credit. Personal guarantees and charges over your home put personal assets at risk, and the tax treatment of deferred consideration and earn-outs needs advice from your own accountant before you sign anything.</p>
"""

make('how-to-buy-a-business-with-no-money-uk', 'How to buy a business with no money (UK)',
     'You buy a business with no money by making it pay for itself: seller-deferred consideration, an earn-out, cash-flow lending, asset finance and a small contribution of your own. The five-piece stack, a worked £600k example, which sellers say yes, and what kills the deal.',
     'It is done more often than you would think, and almost never with a lender funding 100%. Here is the structure that actually works \u2014 the seller, the business\u2019s own assets and its cash flow doing the paying \u2014 with a worked example and the reasons deals like this fall over.',
     BODY)

f = 'buying-out-a-business-partner.html'
s = open(f, encoding='utf-8').read()
if 'Tax implications of buying out a business partner' not in s:
    tax = """  <h2>Tax implications of buying out a business partner</h2>
  <p>The structure you choose sets the tax, and the two obvious routes are taxed very differently:</p>
  <ul>
    <li><strong>You buy the shares personally.</strong> You pay stamp duty at 0.5% on the price. The departing partner pays capital gains tax on their gain \u2014 potentially at the reduced Business Asset Disposal Relief rate if they qualify. You get no tax relief on the purchase price, and if you borrow personally to fund it, relief on the interest is limited.</li>
    <li><strong>The company buys back the shares.</strong> The company pays the departing partner directly, so no money has to come out of the business through your hands first. For the seller, HMRC treats the payment as a distribution (taxed like a dividend) unless the buyback meets the conditions for capital treatment \u2014 broadly a trading company, a five-year holding, a substantial reduction in their stake, and the purchase benefiting the trade. Get advance clearance from HMRC before completing; it is routine and it is the difference between dividend and capital rates for the seller.</li>
    <li><strong>A holding company buys the shares.</strong> Sometimes the cleanest route for a bank-funded buyout: the new company borrows, buys the shares, and repays the loan from dividends flowing up. Interest relief is available at the corporate level, but the structure needs setting up properly.</li>
  </ul>
  <p>Deferred consideration and earn-outs add their own wrinkles \u2014 the seller may be taxed on money they haven\u2019t received yet unless the deal is structured with that in mind. None of this is a reason to avoid a buyout; it is a reason to have your accountant and the seller\u2019s in the room before the price is agreed, because the tax-efficient route for the seller is often the one that lets you pay less up front. We arrange the finance; the tax advice needs to come from your own adviser.</p>

"""
    s = s.replace('  <h2>What lenders want to see</h2>', tax + '  <h2>What lenders want to see</h2>', 1)
    open(f, 'w', encoding='utf-8').write(s)

s = open('sitemap.xml').read()
old = '  <url><loc>https://granton.finance/management-buyout-funding</loc>'
if 'how-to-buy-a-business-with-no-money-uk' not in s:
    s = s.replace(old, '  <url><loc>https://granton.finance/how-to-buy-a-business-with-no-money-uk</loc><lastmod>2026-09-13</lastmod><priority>0.9</priority></url>\n' + old, 1)
s = re.sub(r'(<loc>https://granton.finance/buying-out-a-business-partner</loc><lastmod>)[^<]+', r'\g<1>2026-09-13', s, 1)
open('sitemap.xml', 'w').write(s)

s = open('index.html', encoding='utf-8').read()
old = '      <a href="/business-acquisition-loan">Acquisition loans: how deals get funded</a>'
if 'how-to-buy-a-business-with-no-money-uk' not in s:
    s = s.replace(old, old + '\n      <a href="/how-to-buy-a-business-with-no-money-uk">How to buy a business with no money</a>', 1)
    open('index.html', 'w', encoding='utf-8').write(s)
