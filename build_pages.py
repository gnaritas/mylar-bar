#!/usr/bin/env python3
"""Mylar Bar — Philadelphia PA (South Philly, Ninth & Morris). Template-v2 multi-page build.
Every claim traced in evidence.json. Unknowns (phone, prices, parking) omitted — never guessed.
Hours from the shop's own IG bio (5pm-2am daily, kitchen till 1am). Zip from OSM geocode.
Zero JS. Hand-rolled HTML/CSS. noindex on demo host per lane doctrine.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, 'public')
os.makedirs(PUB, exist_ok=True)

ORIGIN = 'https://mylar-bar-demo.up.railway.app'
BRAND = 'Mylar Bar'
CITY = 'Philadelphia, PA'
STREET = '1638 S. Ninth St.'
FULL_ADDR = '1638 S. Ninth St., Philadelphia, PA 19148'
EMAIL = 'info@mylarbar.com'
IG = 'https://www.instagram.com/mylarbar/'
MAPQ = 'https://www.google.com/maps?q=1638%20S%209th%20St%2C%20Philadelphia%2C%20PA%2019148'
LAT, LON = 39.9282865, -75.1604136  # Nominatim/OSM geocode of 1638 S 9th St — exact address match, see evidence.json
SOCIALS = [IG]

def head(title, desc, path):
    u = ORIGIN + path
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{u}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{ORIGIN}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ORIGIN}/og.png">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/style.css">
<link rel="preconnect" href="https://www.google.com">
</head>
<body>'''

def nav():
    return '''<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="brand" href="/">Mylar&nbsp;Bar <span>South&nbsp;Philly &middot; 9th&nbsp;&amp;&nbsp;Morris</span></a>
  <input type="checkbox" id="navtoggle" class="navtoggle" aria-label="Show navigation">
  <label for="navtoggle" class="navbtn" aria-hidden="true"><i></i></label>
  <nav aria-label="Main" class="links">
    <a href="/cocktails">Drinks</a>
    <a href="/late-night">Late-Night</a>
    <a href="/art">Art</a>
    <a href="/our-story">Our&nbsp;Story</a>
    <a href="/visit">Visit</a>
    <a class="btn btn-sm" href="/contact">Contact&nbsp;Us</a>
  </nav>
</header>'''

def footer():
    return f'''<footer class="site">
  <div class="footgrid">
    <div class="footnap">
      <p class="fbrand">{BRAND}</p>
      <address>{STREET}<br>Philadelphia, PA 19148<br>South Philadelphia</address>
      <p class="fmail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div class="footcta">
      <p class="bunrule" aria-hidden="true"></p>
      <p class="fline">Named for balloon film.<br>Open every night.</p>
      <p class="fsocial"><a href="{IG}" rel="noopener">Instagram</a></p>
      <p class="fline2">The building where Dino&rsquo;s Party Center sold balloons for decades — now martinis, punches and late-night plates.</p>
    </div>
  </div>
  <p class="footline">&copy; 2026 {BRAND} &middot; {CITY}</p>
</footer>'''

def breadcrumbs(name, path):
    items = [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': ORIGIN + '/'},
    ]
    if path != '/':
        items.append({'@type': 'ListItem', 'position': 2, 'name': name, 'item': ORIGIN + path})
    return json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}, ensure_ascii=False)

HOURS_SPEC = [{
    '@type': 'OpeningHoursSpecification',
    'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'opens': '17:00', 'closes': '02:00',
}]

def ld_home():
    obj = {
        '@context': 'https://schema.org', '@type': 'BarOrPub',
        'name': BRAND,
        'image': ORIGIN + '/og.png',
        'url': ORIGIN + '/',
        'email': EMAIL,
        'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'addressLocality': 'Philadelphia', 'addressRegion': 'PA', 'postalCode': '19148', 'addressCountry': 'US'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': LAT, 'longitude': LON},
        'hasMap': MAPQ,
        'openingHoursSpecification': HOURS_SPEC,
        'sameAs': SOCIALS,
    }
    return json.dumps(obj, ensure_ascii=False)

def ld_service(name, path, desc):
    obj = {
        '@context': 'https://schema.org', '@type': 'Service',
        'name': name,
        'description': desc,
        'areaServed': {'@type': 'City', 'name': 'Philadelphia', 'addressRegion': 'PA'},
        'provider': {'@type': 'BarOrPub', 'name': BRAND, 'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'addressLocality': 'Philadelphia', 'addressRegion': 'PA', 'postalCode': '19148', 'addressCountry': 'US'}},
    }
    return json.dumps(obj, ensure_ascii=False)

PAGES = {}

# ---------- HOME ----------
PAGES['index.html'] = (head(f'{BRAND} — Cocktail Bar &amp; Late-Night Kitchen, {CITY}',
    'Cocktail bar in the old Dino&rsquo;s Party Center building at Ninth and Morris, South Philly — martinis, punches, drafts and late-night desserts. Open daily 5pm-2am.',
    '/'), f'''{nav()}
<main id="main">
<section class="hero">
  <p class="kicker">South Philly &middot; Ninth &amp; Morris</p>
  <h1>The party store became<br><em>the party.</em></h1>
  <p class="lead">Martinis, punches and cold drafts. Shareable plates and late-night desserts. Mylar Bar is open every day from 5 until 2 — in the building on Ninth Street where Dino&rsquo;s sold balloons for decades.</p>
  <p class="cta">
    <a class="btn btn-big" href="/cocktails">See the Drinks</a>
    <a class="btn btn-ghost btn-big" href="{MAPQ}" rel="noopener">Get Directions</a>
  </p>
</section>
<section class="awards" id="hoursband">
  <p class="award"><b>Open every day, 5 pm&ndash;2 am</b> &middot; kitchen until 1 am</p>
  <p class="award"><b>&ldquo;A festive neighborhood bar&rdquo;</b> — The Philadelphia Inquirer</p>
  <p class="award">Rotating <b>neighborhood art</b> on the walls</p>
</section>
<section class="cards">
  <h2 class="sr-only">What we serve</h2>
  <a class="card" href="/cocktails">
    <span class="dot" aria-hidden="true"></span>
    <h3>Martinis &amp; Punches</h3>
    <p>Shaken martinis, punches built for a table of friends, and draft beer poured cold — the backbone of the bar.</p>
    <span class="more">See the drinks &rsaquo;</span>
  </a>
  <a class="card" href="/late-night">
    <span class="dot" aria-hidden="true"></span>
    <h3>Late-Night Kitchen</h3>
    <p>Shareable plates until 1 am, late-night desserts after that — the kitchen runs on bar hours, every night.</p>
    <span class="more">See the plates &rsaquo;</span>
  </a>
  <a class="card" href="/art">
    <span class="dot" aria-hidden="true"></span>
    <h3>Art on the Walls</h3>
    <p>Rotating shows from neighborhood artists, tied to Blah Blah Gallery in Bella Vista. Different walls every visit.</p>
    <span class="more">See the art &rsaquo;</span>
  </a>
</section>
<section class="strip">
  <div class="stripin">
    <p class="bigquote">&ldquo;Keeps the spirit of Dino&rsquo;s Party Center alive in South Philly, with a festive atmosphere, fun cocktails, and lots of finger food.&rdquo;</p>
    <p class="attrib">— The Philadelphia Inquirer, November 2026</p>
  </div>
</section>
<section class="storyteaser">
  <div class="sttext">
    <p class="kicker">The story so far</p>
    <h2>A party store, a party, and a bar named after balloon film</h2>
    <p>Liv Arterbridge and Gina Piccari — two South Philly hospitality veterans who met in 2016 — bought the old Dino&rsquo;s Party Center building in October 2024. What opened in November 2026 is Mylar Bar: named for the shiny film party balloons are made of, built for the neighborhood that bought them.</p>
    <p><a class="more" href="/our-story">Read the full story &rsaquo;</a></p>
  </div>
  <div class="stfig" aria-hidden="true">
    <p class="bunrule"></p>
    <p class="figline">Open every day<br><b>5 pm &ndash; 2 am</b></p>
    <p class="figsub">Kitchen until 1 am.<br>Ninth &amp; Morris, South Philly.</p>
    <p class="bunrule"></p>
  </div>
</section>
</main>
{footer()}
<script type="application/ld+json">{ld_home()}</script>
<script type="application/ld+json">{breadcrumbs('Home', '/')}</script>
</body>
</html>''')

# ---------- COCKTAILS (drinks hub) ----------
PAGES['cocktails.html'] = (head(f'Martinis, Punches &amp; Draft Beer — {BRAND}, {CITY}',
    'Shaken martinis, big-batch punches and cold drafts at Mylar Bar — the cocktail bar in South Philly&rsquo;s old party store, open daily 5pm-2am at Ninth and Morris.',
    '/cocktails'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">The Bar</p>
  <h1>Martinis, punches,<br>and cold drafts</h1>
  <p class="lead">Mylar Bar pours the two things a party needs: a drink you can build a night on, and drinks made to share. The bar list leans martinis and punches, with draft beer on tap to keep things easy.</p>
  <p class="cta"><a class="btn" href="/visit">Plan your visit</a> <a class="btn btn-ghost" href="{MAPQ}" rel="noopener">Get Directions</a></p>
</section>
<div class="menuwrap">
  <section class="menu-sec">
    <h2>Martinis <span>— the backbone</span></h2>
    <dl class="items">
      <div><dt>Gin or Vodka</dt><dd>The classics, built to your order — the drink the bar is known for.</dd></div>
      <div><dt>Ask the Bartender</dt><dd>Tell them how you like it: strong, dry, extra cold. This is a martini bar first.</dd></div>
    </dl>
  </section>
  <section class="menu-sec">
    <h2>Punches <span>— made to share</span></h2>
    <dl class="items">
      <div><dt>Punch for the Table</dt><dd>Batches made for a group — the reason tables order round two.</dd></div>
      <div><dt>Come With Friends</dt><dd>Punch plays best with a full table. Pull up a chair; the night is long.</dd></div>
    </dl>
  </section>
  <section class="menu-sec">
    <h2>Draft Beer <span>— easy all night</span></h2>
    <dl class="items">
      <div><dt>Drafts on Tap</dt><dd>Cold, simple, always there — the palate-cleanser between punches.</dd></div>
    </dl>
  </section>
  <section class="menu-note">
    <p class="bunrule" aria-hidden="true"></p>
    <h2>Eating alongside <span>— plates until 1 am</span></h2>
    <p class="newitems">Shareable plates &middot; Late-night desserts</p>
    <p class="fineprint">The kitchen runs on bar hours — shareable plates until 1 am and desserts to close the night. <a href="/late-night">Read about the kitchen &rsaquo;</a></p>
  </section>
  <p class="fineprint center">The bar is open 5 pm to 2 am every day. Follow <a href="{IG}" rel="noopener">Instagram</a> for what&rsquo;s on tonight.</p>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Martinis, Punches and Draft Beer', '/cocktails', 'Martinis, shared punches and draft beer served at Mylar Bar, 1638 S. Ninth St., Philadelphia, PA.')}</script>
<script type="application/ld+json">{breadcrumbs('Drinks', '/cocktails')}</script>
</body>
</html>''')

# ---------- LATE-NIGHT ----------
PAGES['late-night.html'] = (head(f'Late-Night Kitchen &amp; Desserts — {BRAND}, {CITY}',
    'Shareable plates until 1am and late-night desserts after — Mylar Bar&rsquo;s kitchen runs on bar hours every night, led by chef Colin White, at Ninth and Morris.',
    '/late-night'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">After Dinner</p>
  <h1>Plates until 1.<br>Desserts after.</h1>
  <p class="lead">The kitchen runs on bar hours: shareable plates until 1 am and late-night desserts to close the night — every day of the week.</p>
  <p class="cta"><a class="btn" href="/visit">Plan your visit</a> <a class="btn btn-ghost" href="/cocktails">Back to the bar</a></p>
</section>
<div class="detailwrap">
  <section class="roll">
    <h2><span class="num" aria-hidden="true">1</span>Shareable plates</h2>
    <p>The menu was built for groups: finger food that comes out while the punch bowl is still going. No courses, no clock — pass the plate, order another round.</p>
  </section>
  <section class="roll">
    <h2><span class="num" aria-hidden="true">2</span>Late-night desserts</h2>
    <p>Something sweet after 1 — the last round, worth ordering. The kitchen keeps the sweet stuff going while the bar goes to 2.</p>
  </section>
  <aside class="panel">
    <h2>A real chef on the line</h2>
    <p>The kitchen is run by chef Colin White — named when Mylar Bar was first announced in The Philadelphia Inquirer&rsquo;s fall 2026 outlook.</p>
    <p class="cta"><a class="btn" href="/visit">Come get a plate</a></p>
  </aside>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Late-Night Kitchen and Desserts', '/late-night', 'Shareable plates until 1am and late-night desserts, served every night at Mylar Bar, 1638 S. Ninth St., Philadelphia, PA.')}</script>
<script type="application/ld+json">{breadcrumbs('Late-Night', '/late-night')}</script>
</body>
</html>''')

# ---------- ART ----------
PAGES['art.html'] = (head(f'Rotating Neighborhood Art — {BRAND}, {CITY}',
    'Rotating neighborhood art shows at Mylar Bar, tied to Blah Blah Gallery in Bella Vista — new walls every visit at Ninth and Morris, South Philly.',
    '/art'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">The Walls</p>
  <h1>The art rotates.<br>The party doesn&rsquo;t.</h1>
  <p class="lead">Mylar Bar hangs rotating work from neighborhood artists, tied to Blah Blah Gallery in Bella Vista. Walk in twice in a row and you&rsquo;ll see two different shows.</p>
  <p class="cta"><a class="btn" href="/visit">Plan your visit</a> <a class="btn btn-ghost" href="/contact">Artists: get in touch</a></p>
</section>
<div class="detailwrap narrow">
  <section class="roll">
    <h2>Tied to Blah Blah Gallery</h2>
    <p>The rotation runs through Blah Blah Gallery, the artist-run space in nearby Bella Vista — so the work on Mylar&rsquo;s walls comes from the scene that lives around the bar, not from a stock-art crate.</p>
  </section>
  <section class="roll">
    <h2>Why it fits</h2>
    <p>A room that started life as a party store deserves changing walls. Balloons and streamers used to cover these walls; now it&rsquo;s paintings and prints from the neighborhood — same idea, better company.</p>
  </section>
  <aside class="panel">
    <h2>Painting? Making something?</h2>
    <p>The bar wants local work on the walls. Send us a note through the <a href="/contact">contact form</a> — include a couple of links and the gallery crew will see it.</p>
    <p class="cta"><a class="btn" href="/contact">Send your work</a></p>
  </aside>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Rotating Neighborhood Art Shows', '/art', 'Rotating local art shows tied to Blah Blah Gallery, hung on the walls of Mylar Bar, 1638 S. Ninth St., Philadelphia, PA.')}</script>
<script type="application/ld+json">{breadcrumbs('Art', '/art')}</script>
</body>
</html>''')

# ---------- OUR STORY ----------
PAGES['our-story.html'] = (head(f'Our Story — {BRAND}, {CITY}',
    'Liv Arterbridge and Gina Piccari turned the old Dino&rsquo;s Party Center building at Ninth & Morris into Mylar Bar — named for balloon film, opened November 2026.',
    '/our-story'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">Our Story</p>
  <h1>From party store<br>to party.</h1>
  <p class="lead">Mylar Bar took over the South Philadelphia building where Dino&rsquo;s Party Center sold balloons, decorations and party supplies for decades — before Dino&rsquo;s itself moved across the street. The Inquirer called what rose in its place &ldquo;a festive neighborhood bar&rdquo;. We like that description.</p>
  <p class="cta"><a class="btn" href="/visit">See where we are</a> <a class="btn btn-ghost" href="/cocktails">Try the menu</a></p>
</section>
<div class="story">
  <section class="tl">
    <div class="trow"><p class="tyr">2016</p><div class="tbody"><h2>Two cooks, one kitchen</h2><p>Gina Piccari hired Liv Arterbridge into the kitchen at Boot &amp; Saddle. The two South Philadelphians have worked hospitality side by side ever since.</p></div></div>
    <div class="trow"><p class="tyr">Oct 2024</p><div class="tbody"><h2>The building</h2><p>Liv and Gina bought the former Dino&rsquo;s Party Center at Ninth and Morris — the hall where the neighborhood bought balloons and party supplies for decades, right up until Dino&rsquo;s moved across the street.</p></div></div>
    <div class="trow"><p class="tyr">2026</p><div class="tbody"><h2>Almost in summer</h2><p>When fall opened, the Inquirer&rsquo;s food writers already had Mylar Bar on their list of new Philadelphia restaurants to watch. The doors took a little longer than planned — worth the wait.</p></div></div>
    <div class="trow"><p class="tyr">Nov 2026</p><div class="tbody"><h2>Open</h2><p>Mylar Bar opened in mid-November 2026, after a friends-and-family weekend. Now: open every day, 5 pm to 2 am, kitchen until 1.</p></div></div>
  </section>
  <aside class="panel wide">
    <h2>The name</h2>
    <p class="bigquote">&ldquo;Mylar&rdquo; — the shiny film party balloons are made of.</p>
    <p class="attrib">the bar is named for the material Dino&rsquo;s built a business on</p>
    <p>The kitchen is led by chef Colin White. The drink list leans martinis and punches. The art changes every visit. Everything else — the neighborhood feeling — came free with the building.</p>
    <p class="cta"><a class="btn" href="/visit">Visit Ninth &amp; Morris</a></p>
  </aside>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Our Story', '/our-story')}</script>
</body>
</html>''')

# ---------- VISIT ----------
faq_jsonld = json.dumps({
    '@context': 'https://schema.org', '@type': 'FAQPage',
    'mainEntity': [
        {'@type': 'Question', 'name': 'What are Mylar Bar&rsquo;s hours?',
         'acceptedAnswer': {'@type': 'Answer', 'text': 'Open every day from 5 pm to 2 am. The kitchen serves until 1 am.'}},
        {'@type': 'Question', 'name': 'Do you serve food?',
         'acceptedAnswer': {'@type': 'Answer', 'text': 'Yes — shareable plates until 1 am and late-night desserts after.'}},
        {'@type': 'Question', 'name': 'Where exactly is Mylar Bar?',
         'acceptedAnswer': {'@type': 'Answer', 'text': '1638 S. Ninth St., at Ninth and Morris in South Philadelphia (19148), in the former Dino&rsquo;s Party Center building.'}},
    ]
}, ensure_ascii=False)

PAGES['visit.html'] = (head(f'Visit — {BRAND}, {CITY}',
    'Mylar Bar at 1638 S. Ninth St, Philadelphia PA 19148, at Ninth and Morris. Open every day 5pm-2am, kitchen until 1am. Directions, hours and FAQs.',
    '/visit'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">Now Open</p>
  <h1>Ninth &amp; Morris,<br>every night.</h1>
  <p class="lead">We&rsquo;re at 1638 S. Ninth Street, on the corner at Ninth and Morris, in the old Dino&rsquo;s Party Center building. The bar is open 5 pm to 2 am every day; the kitchen serves until 1.</p>
  <p class="cta"><a class="btn btn-big" href="{MAPQ}" rel="noopener">Get Directions</a> <a class="btn btn-ghost btn-big" href="/contact">Ask Us Anything</a></p>
</section>
<div class="visitgrid">
  <section class="visitinfo">
    <h2>Where</h2>
    <address class="bigaddr">{STREET}<br>Philadelphia, PA 19148<br>South Philadelphia</address>
    <p>At Ninth and Morris — the building that housed Dino&rsquo;s Party Center for decades.</p>
    <h2>When</h2>
    <p>Open every day, 5 pm to 2 am.<br>Kitchen open until 1 am every day.</p>
    <h2>Questions before you come</h2>
    <div class="faqlist">
      <p class="faq-q">What are your hours?</p>
      <p class="faq-a">Every day, 5 pm to 2 am. Kitchen until 1 am.</p>
      <p class="faq-q">Do you serve food?</p>
      <p class="faq-a">Yes — shareable plates until 1 am, late-night desserts after. <a href="/late-night">See the kitchen &rsaquo;</a></p>
      <p class="faq-q">How do I see what&rsquo;s on tonight?</p>
      <p class="faq-a">Follow <a href="{IG}" rel="noopener">Instagram</a> — hours, what&rsquo;s poured and the current art rotation all go up there.</p>
    </div>
    <p class="cta"><a class="btn btn-ghost" href="/cocktails">What we pour</a></p>
  </section>
  <section class="visitmap">
    <div class="mapbox">
      <iframe title="Map to Mylar Bar, 1638 S 9th St, Philadelphia, PA" src="https://www.google.com/maps?q=1638%20S%209th%20St%2C%20Philadelphia%2C%20PA%2019148&output=embed" loading="eager" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
    <p class="fineprint">Can&rsquo;t load the map? <a href="{MAPQ}" rel="noopener">Open it in Google Maps</a> or <a href="mailto:{EMAIL}">email us</a> and we&rsquo;ll talk you in.</p>
  </section>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Visit Mylar Bar', '/visit', 'Cocktail bar and late-night kitchen at 1638 S. Ninth St. (Ninth and Morris), Philadelphia, PA 19148. Open daily 5pm-2am, kitchen till 1am.')}</script>
<script type="application/ld+json">{faq_jsonld}</script>
<script type="application/ld+json">{breadcrumbs('Visit', '/visit')}</script>
</body>
</html>''')

# ---------- CONTACT ----------
PAGES['contact.html'] = (head(f'Contact — {BRAND}, {CITY}',
    'Contact Mylar Bar, the cocktail bar in South Philly&rsquo;s old party store — email, contact form, and directions to 1638 S. Ninth St at Ninth and Morris.',
    '/contact'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">Talk to Us</p>
  <h1>Contact Mylar&nbsp;Bar</h1>
  <p class="lead">Questions about the bar, a table for a crowd, or the art on the walls? Email us or use the form — it lands straight in the shop&rsquo;s inbox.</p>
</section>
<div class="contactgrid">
  <form class="cform" method="post" action="/contact">
    <h2>Send a message</h2>
    <p><label for="f-name">Your name</label><input id="f-name" name="name" type="text" required maxlength="120" autocomplete="name"></p>
    <p><label for="f-email">Email</label><input id="f-email" name="email" type="email" required maxlength="160" autocomplete="email"></p>
    <p><label for="f-msg">Message</label><textarea id="f-msg" name="message" rows="5" required maxlength="4000"></textarea></p>
    <p><button class="btn btn-big" type="submit">Send Message</button></p>
    <p class="fineprint">This form emails the shop directly. We never share your address.</p>
  </form>
  <section class="cinfo">
    <h2>Direct lines</h2>
    <p class="clabel">Email</p>
    <p class="cbig"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p class="clabel">Walk in</p>
    <address class="bigaddr">{STREET}<br>Philadelphia, PA 19148</address>
    <p class="clabel">Instagram — hours &amp; what&rsquo;s on</p>
    <p class="cbig"><a href="{IG}" rel="noopener">@mylarbar</a></p>
  </section>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Contact', '/contact')}</script>
</body>
</html>''')

# ---------- PRIVACY ----------
PAGES['privacy.html'] = (head(f'Privacy Policy — {BRAND}, {CITY}',
    'Privacy policy for the Mylar Bar website: what the contact form collects, and the site&rsquo;s cookie and tracking practices. No trackers, no cookies.',
    '/privacy'), f'''{nav()}
<main id="main">
<section class="pagehead narrow">
  <p class="kicker">Privacy</p>
  <h1>Privacy Policy</h1>
</section>
<div class="prose">
  <p>This site belongs to {BRAND} ({FULL_ADDR}).</p>
  <h2>What we collect</h2>
  <p>The contact form on this site collects only the information you type into it — your name, your email address and your message — and sends it to the shop&rsquo;s own email address so the owners can answer you. That is the entire purpose of the data. It is not sold, shared or used for advertising.</p>
  <h2>Cookies and tracking</h2>
  <p>This site sets no cookies and uses no advertising trackers or analytics pixels of its own. The embedded Google map may set its own cookies once you interact with it, governed by Google&rsquo;s privacy policy.</p>
  <h2>Your choices</h2>
  <p>Want your message deleted from the shop&rsquo;s mailbox records? Email <a href="mailto:{EMAIL}">{EMAIL}</a> and ask. Questions about this policy go to the same address.</p>
  <p class="fineprint">This policy covers this website only.</p>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Privacy', '/privacy')}</script>
</body>
</html>''')

# ---------- 404 ----------
PAGES['404.html'] = (head(f'Page not found — {BRAND}',
    'Page not found at the Mylar Bar site. Back to the bar, or straight to the drinks page.',
    '/404'), f'''{nav()}
<main id="main">
<section class="pagehead center">
  <p class="kicker">404</p>
  <h1>That balloon floated away.</h1>
  <p class="lead">This page doesn&rsquo;t exist — but the bar does, every day from 5 pm.</p>
  <p class="cta"><a class="btn btn-big" href="/">Back to Home</a> <a class="btn btn-ghost btn-big" href="/cocktails">See the Drinks</a></p>
</section>
</main>
{footer()}
</body>
</html>''')

# ---------- THANKS ----------
PAGES['thanks.html'] = (head(f'Message sent — {BRAND}',
    'Thanks for reaching out to Mylar Bar — the owners read every message.',
    '/thanks'), f'''{nav()}
<main id="main">
<section class="pagehead center">
  <p class="kicker">Received</p>
  <h1>Your message is in.</h1>
  <p class="lead">Thank you — Liv and Gina read the shop&rsquo;s inbox themselves. Meanwhile, the drinks and the map are one click away.</p>
  <p class="cta"><a class="btn btn-big" href="/cocktails">See the Drinks</a> <a class="btn btn-ghost btn-big" href="/visit">Plan your visit</a></p>
</section>
</main>
{footer()}
</body>
</html>''')

for fname, (h, body) in PAGES.items():
    with open(os.path.join(PUB, fname), 'w', encoding='utf-8') as f:
        f.write(h + '\n' + body)
    print('wrote', fname, len(h + body), 'bytes')

# ---------- sitemap / robots / favicon ----------
pages_order = ['/', '/cocktails', '/late-night', '/art', '/our-story', '/visit', '/contact', '/privacy']
today = '2026-11-24'
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'<url><loc>{ORIGIN}{p}</loc><lastmod>{today}</lastmod></url>\n' for p in pages_order) + '</urlset>\n'
open(os.path.join(PUB, 'sitemap.xml'), 'w').write(sitemap)
open(os.path.join(PUB, 'robots.txt'), 'w').write(f'''User-agent: *
Allow: /

Sitemap: {ORIGIN}/sitemap.xml
''')
favicon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#141021"/><ellipse cx="32" cy="26" rx="13" ry="16" fill="#ff4d8f"/><ellipse cx="27" cy="20" rx="4" ry="6" fill="#ffd3e4"/><line x1="32" y1="42" x2="32" y2="52" stroke="#cfd3e6" stroke-width="2.4"/><path d="M28 42 L32 38 L36 42 Z" fill="#cfd3e6"/></svg>
'''
open(os.path.join(PUB, 'favicon.svg'), 'w').write(favicon)
print('wrote sitemap.xml robots.txt favicon.svg')
print('PAGES:', len([f for f in PAGES if f.endswith('.html')]))
