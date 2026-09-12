import re

T = {
 'what-is-a-bridging-loan': 'What is a bridging loan?',
 'how-does-a-bridging-loan-work': 'How does a bridging loan work?',
 'how-much-does-a-bridging-loan-cost': 'How much does a bridging loan cost?',
 'how-long-does-a-bridging-loan-take': 'How long does a bridging loan take?',
 'auction-bridging-finance': 'Auction finance: 28 days to complete',
 'vat-bridging-loan': 'VAT bridging loans',
 'refurbishment-bridging-loan': 'Refurbishment bridging',
 'land-bridging-loan': 'Land bridging loans',
 'second-charge-bridging-loan': 'Second charge bridging',
 'unregulated-bridging-loan': '"Unregulated" bridging, explained',
 'business-acquisition-loan': 'Business acquisition loans: how deals get funded',
 'management-buyout-funding': 'Management buyout funding',
 'mbo-calculator': 'Management buyout calculator',
 'buying-out-a-business-partner': 'Buying out a business partner',
 'invoice-finance-broker': 'Invoice finance broker',
 'small-business-invoice-finance': 'Invoice finance for a small business',
 'accountants': 'For accountants: refer a client',
 'solicitors': 'For solicitors: the funding side, handled',
 'introducers': 'For introducers',
 'score': 'Fundability score: could your deal be funded?',
}

BRIDGE_BASICS = ['what-is-a-bridging-loan', 'how-does-a-bridging-loan-work', 'how-much-does-a-bridging-loan-cost', 'how-long-does-a-bridging-loan-take']
BRIDGE_USES = ['auction-bridging-finance', 'vat-bridging-loan', 'refurbishment-bridging-loan', 'land-bridging-loan', 'second-charge-bridging-loan', 'unregulated-bridging-loan']
DEALS = ['business-acquisition-loan', 'management-buyout-funding', 'mbo-calculator', 'buying-out-a-business-partner']
INVOICE = ['invoice-finance-broker', 'small-business-invoice-finance']
REFER = ['accountants', 'solicitors', 'introducers']

REL = {}
def ring(c, me, n):
    i = c.index(me); r = c[i+1:] + c[:i]; return r[:n]
for p in BRIDGE_BASICS:
    REL[p] = ring(BRIDGE_BASICS, p, 3) + ring(BRIDGE_USES, BRIDGE_USES[BRIDGE_BASICS.index(p) % len(BRIDGE_USES)], 2) + ['business-acquisition-loan']
for p in BRIDGE_USES:
    REL[p] = ring(BRIDGE_BASICS, BRIDGE_BASICS[BRIDGE_USES.index(p) % 4], 2) + ring(BRIDGE_USES, p, 3) + ['business-acquisition-loan']
for p in DEALS:
    REL[p] = [x for x in DEALS if x != p] + ['how-does-a-bridging-loan-work', 'small-business-invoice-finance', 'score']
for p in INVOICE:
    REL[p] = [x for x in INVOICE if x != p] + ['business-acquisition-loan', 'management-buyout-funding', 'what-is-a-bridging-loan', 'score']
for p in REFER:
    REL[p] = [x for x in REFER if x != p] + ['business-acquisition-loan', 'management-buyout-funding', 'score']

STYLE = '.related{margin:44px 0 8px;padding:22px 24px;border:1px solid rgba(0,0,0,.12);border-radius:6px;background:rgba(255,255,255,.55)}.related .rt{font-family:"Helvetica Neue",Arial,sans-serif;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--brass,#8a6d3b);margin:0 0 10px}.related ul{list-style:none;margin:0;padding:0;columns:2;column-gap:28px}.related li{break-inside:avoid;margin:0 0 8px;font-size:16px}.related a{text-decoration:none;border-bottom:1px solid rgba(0,0,0,.25)}@media(max-width:600px){.related ul{columns:1}}'

for slug, rel in REL.items():
    f = slug + '.html'
    s = open(f, encoding='utf-8').read()
    if 'class="related"' in s:
        continue
    block = '  <div class="related">\n    <p class="rt">Related guides</p>\n    <ul>\n' + ''.join('      <li><a href="/%s">%s</a></li>\n' % (r, T[r]) for r in rel) + '    </ul>\n  </div>\n\n'
    if '  <div class="cta">' in s:
        s = s.replace('  <div class="cta">', block + '  <div class="cta">', 1)
    elif '</main>' in s:
        s = s.replace('</main>', '<div class="wrap"><div class="doc">' + block + '</div></div>\n</main>', 1)
    else:
        continue
    s = s.replace('</style>', STYLE + '\n</style>', 1)
    open(f, 'w', encoding='utf-8').write(s)
