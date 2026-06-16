#!/usr/bin/env python3
# Build Teacher Gladys' bilingual teaching portfolio.
# Content (text / videos / interactive embeds) is fixed here; photos are pulled
# dynamically from assets/img/ so the build is resilient to the download set.
import os, glob, html

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(ROOT, "assets", "img")

SITE   = "Teacher Glad"
SCHOOL = "Nanhsing Elementary School"

# Top navigation mirrors the original site: 5 items, with the four corners
# living under the Bilingual Initiative page.
NAV = [
    ("index.html",                "Home"),
    ("bilingual-initiative.html", "Bilingual Initiative"),
    ("about-me.html",             "About Me"),
    ("learning-activities.html",  "Learning Activities"),
    ("learning-outputs.html",     "Learning Outputs"),
]

# Sub-navigation for the four Bilingual-Initiative corners.
CORNERS_NAV = [
    ("bilingual-initiative.html",      "Overview"),
    ("english-club.html",              "English Club"),
    ("english-corner.html",            "English Corner"),
    ("international-sister-school.html","Sister School"),
    ("communication-arts.html",        "Communication Arts"),
]

def imgs(key):
    """Real images for a page key, sorted, web path list."""
    files = sorted(glob.glob(os.path.join(IMG, f"{key}_*.jpg")))
    out = []
    for f in files:
        try:
            if os.path.getsize(f) > 5000:
                out.append("assets/img/" + os.path.basename(f))
        except OSError:
            pass
    return out

def pick(key, n, fallback_key=None):
    """nth image of a page (0-based), with graceful fallback."""
    a = imgs(key)
    if n < len(a):
        return a[n]
    if fallback_key:
        b = imgs(fallback_key)
        if b:
            return b[0]
    return a[0] if a else "assets/img/placeholder.svg"

def nav_html(active):
    links = "".join(
        f'<a href="{href}"{" class=\"active\"" if href==active else ""}>{html.escape(label)}</a>'
        for href, label in NAV
    )
    return f'''<header class="nav"><div class="nav-in">
  <a class="brand" href="index.html"><span class="dot"></span>{SITE}</a>
  <button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
  <nav class="nav-links">{links}</nav>
</div></header>'''

def subnav(active):
    links = "".join(
        f'<a href="{href}"{" class=\"active\"" if href==active else ""}>{html.escape(label)}</a>'
        for href, label in CORNERS_NAV
    )
    return f'<div class="subnav"><div class="wrap"><div class="subnav-in">{links}</div></div></div>'

def hero(img, eyebrow, title, lead, short=False, orbs=True):
    o = '<span class="orb a"></span><span class="orb b"></span>' if orbs else ''
    return f'''<section class="hero{' short' if short else ''}">
  <div class="hero-bg"><img src="{img}" alt=""></div>{o}
  <div class="hero-scrim"></div>
  <div class="hero-in">
    <span class="eyebrow rvl">{eyebrow}</span>
    <h1 class="rvl d1">{title}</h1>
    <p class="lead rvl d2">{lead}</p>
  </div>
</section>'''

def gallery(key, limit=None):
    a = imgs(key)
    if limit:
        a = a[:limit]
    if not a:
        return ''
    cells = "".join(
        f'<figure class="gi rvl"><img loading="lazy" src="{src}" data-full="{src}" alt="Classroom moment"></figure>'
        for src in a
    )
    return f'<div class="gallery">{cells}</div>'

def gsec(key, head, tint=False, limit=None):
    """Gallery section that renders only when photos exist for the page."""
    g = gallery(key, limit=limit)
    return section(g, tint=tint, head=head) if g else ''

def video(src, cap):
    return f'<div class="video rvl"><iframe loading="lazy" src="{src}" allow="autoplay; fullscreen" allowfullscreen></iframe><div class="cap">{cap}</div></div>'

def yt(vid, cap):     return video(f"https://www.youtube.com/embed/{vid}", cap)
def drive(fid, cap):  return video(f"https://drive.google.com/file/d/{fid}/preview", cap)

def embed(src, kind, cap, minh=430):
    cls = {"Wordwall":"ww","Padlet":"pad","Canva":"canva"}[kind]
    return (f'<div class="embed rvl"><div class="cap"><span class="pill {cls}">{kind}</span>{cap}</div>'
            f'<iframe loading="lazy" src="{src}" style="min-height:{minh}px" allowfullscreen></iframe></div>')

def wordwall(i, cap): return embed(f"https://wordwall.net/embed/{i}", "Wordwall", cap)
def padlet(i, cap):   return embed(f"https://padlet.com/embed/{i}", "Padlet", cap, 480)
def canva(i, cap):    return embed(f"https://www.canva.com/design/{i}/view?embed", "Canva", cap, 420)

def footer():
    cols = "".join(f'<a href="{h}">{html.escape(l)}</a>' for h,l in NAV[:6])
    return f'''<footer class="footer"><div class="wrap">
  <div class="col">
    <h4>{SITE}</h4>
    <p>A foreign English teacher's portfolio of building a global, bilingual campus at {SCHOOL} — through stories, songs, festivals, and friendships across borders.</p>
  </div>
  <div class="col">
    <h4>Explore</h4>
    <div class="links">{cols}</div>
  </div>
  <div class="col">
    <h4>About</h4>
    <div class="links">
      <span>Gladys Mabute · Teacher Glad</span>
      <span>{SCHOOL}</span>
      <span>Taiwan Foreign English Teacher Program (TFETP)</span>
    </div>
  </div>
  <div class="fine">© Teacher Glad · {SCHOOL}. Built as a living teaching portfolio. Photos &amp; student work belong to the teacher and school.</div>
</div></footer>'''

def page(fname, title, body, active=None, sub=None):
    active = active or fname
    sub_bar = subnav(sub) if sub else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · {SITE}</title>
<meta name="description" content="Teacher Glad — bilingual English teaching portfolio at {SCHOOL}, Taiwan.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{nav_html(active)}
{sub_bar}
{body}
{footer()}
<script src="assets/js/motion.js"></script>
</body>
</html>'''

# ---- shared intro texts ----
T_WELCOME = ("Welcome! I'm a foreign English teacher at " + SCHOOL + ", and I'm thrilled to share our "
  "journey toward becoming a truly global campus. This site is a living portfolio of our Bilingual "
  "Initiative — the vibrant ways our students meet English every single day.")

def section(inner, tint=False, head=None):
    h = ''
    if head:
        eye, t, sub = head
        sub_html = f'<p class="lead rvl d1">{sub}</p>' if sub else ''
        h = f'<div class="section-head rvl"><span class="eyebrow">{eye}</span><h2>{t}</h2>{sub_html}</div>'
    return f'<section class="{ "tint" if tint else "" }"><div class="wrap">{h}{inner}</div></section>'

# ================= PAGES =================
def build():
    os.makedirs(IMG, exist_ok=True)
    P = {}

    # ---------- HOME ----------
    corners = [
        ("english-club.html","English Club","Story to Stage","Reading comes alive through reader's theater, role-play, and performance.","03-english-club"),
        ("english-corner.html","English Corner","Everyday English","A daily practice corner and the morning-assembly Sentence of the Week.","04-english-corner"),
        ("international-sister-school.html","International Sister School","Bridges Across Borders","English as the key that opens doors to new people and cultures.","05-international-sister-school"),
        ("communication-arts.html","Communication Arts","Real-World Talk","Turning grammar and vocabulary into spontaneous, confident communication.","06-communication-arts"),
    ]
    cards = "".join(
        f'''<a class="card link-card rvl" href="{href}">
  <div class="thumb"><img loading="lazy" src="{pick(k,0)}" alt="{t}"></div>
  <div class="body"><span class="tag">{tag}</span><h3>{t}</h3><p>{d}</p>
  <span class="more">Explore <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>
</a>''' for href,t,tag,d,k in corners)
    stats = '''<div class="stats">
      <div class="stat rvl"><div class="n" data-to="13" data-suf="+">0</div><div class="l">Years Teaching</div></div>
      <div class="stat rvl d1"><div class="n" data-to="4">0</div><div class="l">Bilingual Corners</div></div>
      <div class="stat rvl d2"><div class="n">G4–6</div><div class="l">Young Learners</div></div>
      <div class="stat rvl d3"><div class="n">PH→TW</div><div class="l">Heart of Asia</div></div>
    </div>'''
    home_banner = imgs("01-home")
    banner_src = home_banner[0] if home_banner else pick("05-international-sister-school",0)
    home = (
      f'''<section class="hero brand-hero">
  <div class="hero-bg"><img src="{banner_src}" alt="Teacher Glad — Games, Language, Activities &amp; Development"></div>
  <span class="orb a"></span><span class="orb b"></span>
  <div class="hero-cue">Welcome to Teacher Glad's classroom — scroll to explore ↓</div>
</section>'''
      + section(f'<div class="prose rvl"><p class="lead">{T_WELCOME}</p></div>'
                + f'<p class="rvl d1" style="font-size:21px;color:var(--ink-soft);max-width:780px">Our mission is to move beyond the textbook. By weaving English into international partnerships, the creative arts, and daily school life, we give students authentic chances to listen, speak, read, and write — and to fall in love with learning.</p>',
                head=("Welcome","A living, breathing English classroom", None))
      + section('<div class="grid g4">'+cards+'</div>',
                tint=True, head=("The Bilingual Initiative","Four corners of a global campus","Explore the four specialized corners where confidence and curiosity grow."))
      + section(stats, head=("By the Numbers","A teacher's journey to Taiwan", None))
      + (section(gallery("08-learning-activities", 8) +
                '<div class="btn-row rvl"><a class="btn primary" href="learning-activities.html">See more moments</a></div>',
                tint=True, head=("In the Classroom","Learning by doing", None)) if imgs("08-learning-activities") else '')
      + '<section><div class="wrap"><div class="band rvl"><h2>“You learn by doing — and by falling over.”</h2>'
        '<p>Every drill, song, festival, and performance is a chance to try, stumble, and grow braver in English.</p>'
        '<div class="btn-row" style="justify-content:center"><a class="btn ghost" href="about-me.html">Meet Teacher Glad</a></div></div></div></section>'
    )
    P["index.html"] = page("index.html","Home",home)

    # ---------- BILINGUAL INITIATIVE ----------
    bi_cards = "".join(
        f'''<a class="card link-card rvl" href="{href}">
  <div class="thumb"><img loading="lazy" src="{pick(k,0)}" alt="{t}"></div>
  <div class="body"><span class="tag">{tag}</span><h3>{t}</h3><p>{d}</p>
  <span class="more">Explore <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>
</a>''' for href,t,tag,d,k in corners)
    bi = (
      hero(pick("02-bilingual-initiative",0,"04-english-corner"),
           "The Bilingual Initiative","A truly global campus",
           "Moving beyond the textbook — integrating English into partnerships, the arts, and everyday school life.", short=True)
      + section(f'<div class="prose rvl"><p class="lead">{T_WELCOME}</p>'
                '<p>By integrating English into various school contexts — from international partnerships to creative arts — we give our students authentic opportunities to develop their listening, speaking, reading, and writing skills. Explore our four specialized corners below.</p></div>',
                head=("Our Mission","Confidence and curiosity, every day", None))
      + section('<div class="grid g4">'+bi_cards+'</div>', tint=True,
                head=("Four Corners","Where English comes alive", None))
      + section('<div class="video-grid">' + yt("ysQEfmGlHGI","Our Bilingual Initiative — in motion")
                + drive("1X__0bmU6zgD7Z3qzQiIv6qblhjZW21Yr","Campus highlight")
                + drive("1yRppSUxExk5p-uEkZb9079EeNE-A1hSE","Students in action") + '</div>',
                head=("Watch","See it in motion", None))
    )
    P["bilingual-initiative.html"] = page("bilingual-initiative.html","Bilingual Initiative",bi,sub="bilingual-initiative.html")

    # ---------- ENGLISH CLUB ----------
    ec_videos = "".join(drive(f,c) for f,c in [
        ("1lfs3yu-xrctjTwDl8mXV92U1q3Znqora","Reader's Theater"),
        ("19mlmpfr6kDmvO7edqBqhRmM22jOL7eF0","Story performance"),
        ("11K7O7Sdexl3SYQxHGSmdUPoMtzMTcShL","Role-play in action"),
        ("1uv27WgA6HX-S9AAcI8gwnGCUSYa2y9iw","On stage together"),
    ])
    eclub = (
      hero(pick("03-english-club",0),"English Club","From story to stage",
           "Taking literary works and making them dynamic, interactive, and unforgettable.", short=True)
      + section('<div class="prose rvl"><p class="lead">Our English Club isn\'t just about reading; it\'s about experiencing language through story.</p>'
                '<p>This class takes literary works and makes them dynamic and interactive. Our goal is to move from reading to understanding, and from understanding to performing — building a love for literature and performance along the way.</p></div>',
                head=("English Club","Reading, understanding, performing", None))
      + section('<div class="video-grid">'+ec_videos+'</div>', tint=True,
                head=("Performances","Reader's theater & role-play", None))
      + gsec("03-english-club", ("Gallery","Moments from the club", None))
    )
    P["english-club.html"] = page("english-club.html","English Club",eclub,active="bilingual-initiative.html",sub="english-club.html")

    # ---------- ENGLISH CORNER ----------
    corner_games = "".join(wordwall(i,c) for i,c in [
        ("637433f0bb7148cf863abd1d876a7e88","Vocabulary game"),
        ("faced900b78f4e27980e7c49bc0a8017","Word practice"),
        ("00285e3b5384430dab9e4d89807ffe8c","Sentence builder"),
        ("bf6a32c0b57f4b389af6ca7d71495344","Quick review"),
    ])
    corner = (
      hero(pick("04-english-corner",0),"English Corner & Morning Assembly","Everyday English",
           "A daily practice corner and the morning-assembly Sentence of the Week — English woven into the school day.", short=True)
      + section('<div class="prose rvl"><p class="lead">The daily English Practice Corner and “Sentence of the Week” turn passive knowledge into active use.</p>'
                '<p>It\'s about building a consistent, habitual practice — making English an unavoidable and enjoyable part of every student\'s daily routine.</p></div>',
                head=("English Corner","A consistent daily habit", None))
      + section('<div class="grid g2">'+corner_games+'</div>'
                + '<div style="margin-top:26px">'+padlet("1yiljuk5s0x8yjxd","Sentence of the Week — student wall")+'</div>',
                tint=True, head=("Play & Practice","Interactive Wordwall games and a Padlet wall", "Tap a game to play right here."))
      + gsec("04-english-corner", ("Gallery","Morning English in action", None))
    )
    P["english-corner.html"] = page("english-corner.html","English Corner",corner,active="bilingual-initiative.html",sub="english-corner.html")

    # ---------- INTERNATIONAL SISTER SCHOOL ----------
    iss_videos = '<div class="video-grid">' + yt("lJToF8D9bdU","International exchange") + "".join(drive(f,c) for f,c in [
        ("1nQrKFTLcQOceu3bIDpcAEbmW6uL-vPHA","Greetings across borders"),
        ("1vrOJVUq7VuP6CCokw3AYXorSI4Jk1aiS","Sharing our culture"),
        ("1cJZM9wTixlUTGAOXSAHigfb4CyBDsmb2","Sister-school moment"),
        ("11jz8akmXQbGuEW5l3NK2d5b3Wp_FZyUJ","Meeting new friends"),
        ("1GrVp3FqtU7wNlV2cMXIvpklzR_x4Qc4_","A global hello"),
        ("182YPy0_Hz9oJpdf3PfeopOjTX4EuH2wz","Cultural exchange"),
    ]) + '</div>'
    iss_pad = '<div class="grid g3">' + "".join(padlet(i,c) for i,c in [
        ("ummnh169ngf7cqya","Exchange wall"),
        ("klbkpfvmwqqe0ect","Our global friends"),
        ("alqqht0p8za1bkp4/slideshow","Culture slideshow"),
    ]) + '</div>'
    iss_canva = '<div class="grid g2">' + "".join(canva(i,c) for i,c in [
        ("DAG4jVzL07o/TfrWGan8Kw8ZDyCgZwzeDQ","Country spotlight"),
        ("DAG7F0sl92s/4PfaUmeVChqe7R1caa6XBQ","World cultures"),
        ("DAHFsF-iRe8/okI9IaUpn9mj9XrvLqNY4w","Festivals of the world"),
        ("DAHHWsEvVMU/8477APv1xAuous3l303qGg","Global friends"),
        ("DAHIyL3tMsc/vy1AAkO5j9wIC220umMDlQ","Passport journal"),
    ]) + '</div>'
    iss = (
      hero(pick("05-international-sister-school",0),"International Sister School","Bridges across borders",
           "A borderless approach to education — English as the global key that opens doors to new people and cultures.", short=True)
      + section('<div class="prose rvl"><p class="lead">We believe in a “borderless” approach to education.</p>'
                '<p>This corner is dedicated to making English the bridge that connects our students with the wider world — expanding their horizons and showing them that English opens doors to new people, cultures, and understanding.</p></div>',
                head=("Sister School","English as a global key", None))
      + section(iss_videos, tint=True, head=("Watch","Exchanges in motion", None))
      + section(iss_pad, head=("Student Walls","Padlet collaborations", None))
      + section(iss_canva, tint=True, head=("Culture Decks","Made in Canva", None))
      + gsec("05-international-sister-school", ("Gallery","Around the world, together", None))
    )
    P["international-sister-school.html"] = page("international-sister-school.html","International Sister School",iss,active="bilingual-initiative.html",sub="international-sister-school.html")

    # ---------- COMMUNICATION ARTS ----------
    ca_canva = '<div class="grid g3">' + "".join(canva(i,c) for i,c in [
        ("DAGx-6aFtpU/45EP_jPiryrZwEjWchsA9g","Communicative function"),
        ("DAHI9ccHQIM/fzN9mAwA6LdJr1ha55KYTg","Real-world dialogue"),
        ("DAHI9nzGhDU/aMzZjRpmZU2qq2nPbC9Obg","Speaking practice"),
    ]) + '</div>'
    ca = (
      hero(pick("06-communication-arts",0),"Communication Arts Class","Real-world talk",
           "Where all the skills come together — turning grammar and vocabulary into spontaneous communication.", short=True)
      + section('<div class="prose rvl"><p class="lead">This is where all the skills come together.</p>'
                '<p>Communication Arts is our structured class focused on specific communicative functions, designed for real-world application — transforming abstract grammar and vocabulary into practical, spontaneous communication so students are ready to use English in the real world.</p></div>',
                head=("Communication Arts","Built for the real world", None))
      + section(ca_canva, tint=True, head=("Lesson Decks","Made in Canva", None))
      + gsec("06-communication-arts", ("Gallery","Talking, listening, connecting", None))
    )
    P["communication-arts.html"] = page("communication-arts.html","Communication Arts",ca,active="bilingual-initiative.html",sub="communication-arts.html")

    # ---------- ABOUT ME ----------
    bio = [
      "Growing up in a multilingual nation with more than 170 languages — where English is the second language of more than 76% of the population — I learned that education can bridge the cultural and communication barriers between people. The ability to communicate effectively is one of the most essential life skills, and that belief became a roadmap to the profession dearest to my heart, and later took me to the Heart of Asia, Taiwan.",
      "From Ma'am Gladys Mabute in the Philippines, " + SCHOOL + " — through the Taiwan Foreign English Teacher Program (TFETP) — helped me find a better version of myself in Teacher Glad. My 13-year teaching career back home shaped me as a learning facilitator who helps young minds blossom into well-rounded, innovative individuals. But teaching as a Foreign English Teacher in Taiwan is a different story: I had to unlearn old methods and discover new approaches for my new students, and I learned to embrace the beauty of teaching basic English — witnessing students grow each day with the simple words, phrases, and sentences from every class.",
      "At Nanhsing, almost every teaching material is readily available, so I maximize them to develop my students' macro skills. In English Club, students read English books to build reading comprehension, with role-play and reader's theater to boost confidence. I introduced Drills on BELLS (Basic English Language and Literacy Skills) for Grades 4–6 — daily conversation bingo, snake-and-ladder games, and more.",
      "My role doesn't end with communication skills — I'm committed to building global competitiveness through cultural diversity. In International Education, I integrate world festivals, food, art, and literature. It's amazing to see students enjoy foreign celebrations like the Easter Egg Hunt, keep a passport-mockup journal of the countries we 'visit', and of course experience a little Filipino culture too.",
      "Teaching in Taiwan is truly a rewarding experience — empowering children's lives while enjoying work-life balance in a nation of unique cultural fusion, picturesque scenery, and friendly people. I look forward to more exciting stories, and to impacting more students' lives here.",
    ]
    bio_html = "".join(f'<p class="rvl">{p}</p>' for p in bio)
    about = (
      hero(pick("07-about-me",0),"About Me","Hello, I'm Teacher Glad",
           "Gladys Mabute — from the Philippines to the Heart of Asia, through the Taiwan Foreign English Teacher Program.", short=True)
      + '<section><div class="wrap"><div class="split">'
        f'<div class="media rvl"><img loading="lazy" src="{pick("07-about-me",1,"05-international-sister-school")}" alt="Teacher Glad"></div>'
        f'<div class="text"><span class="eyebrow rvl">My Story</span><h2 class="rvl">Education that bridges people</h2>'
        f'<div class="prose">{bio_html}</div></div>'
        '</div></div></section>'
      + gsec("07-about-me", ("Gallery","Life at Nanhsing", None), tint=True)
    )
    P["about-me.html"] = page("about-me.html","About Me",about)

    # ---------- LEARNING ACTIVITIES ----------
    la = (
      hero(pick("08-learning-activities",0),"Learning Activities","Learning by doing",
           "Drills, games, festivals, and performances — the joyful, hands-on heart of the classroom.", short=True)
      + '<section><div class="wrap"><blockquote class="quote-big rvl">“You learn by doing and by falling over.”'
        '<span class="by">— Richard Branson</span></blockquote></div></section>'
      + section('<div class="video-grid">' + drive("1NWGmTy_acIrg98HmYCkofjH2OovX2a-I","Activity highlight")
                + drive("1CfmW_k5G56NQuRHmkPfDrkAdQJe4bX8T","Hands-on learning") + '</div>',
                head=("Watch","Activities in motion", None))
      + gsec("08-learning-activities", ("Photo Wall","Every moment counts", None), tint=True)
    )
    P["learning-activities.html"] = page("learning-activities.html","Learning Activities",la)

    # ---------- LEARNING OUTPUTS ----------
    lo_games = "".join(wordwall(i,c) for i,c in [
        ("c2458931067b48ef90f17cadc5809688","Review game 1"),
        ("f46541e367904e038861172e086e8514","Review game 2"),
        ("072d4e31828840029a631f280769adff","Review game 3"),
        ("0137d8677815424994e8cc7cfb0b7f7f","Review game 4"),
        ("a0183ec946144e378995399142c4b1bf","Review game 5"),
    ])
    lo_canva = "".join(canva(i,c) for i,c in [
        ("DAGnM2uR7ZM/bdGfpIa3-j6Q2sw8WfADdg","Teaching material 1"),
        ("DAGfC7tJrSE/c1f_Fxxx2Xp4zf8FsO5ZNA","Teaching material 2"),
        ("DAGlnWPHcCw/DcwDjYYbsgh3ee10KYCDDg","Teaching material 3"),
        ("DAGmRqez9Dw/zr9fwZvp_MUcJV8jwp_y8Q","Teaching material 4"),
        ("DAGfghm9fAg/vwsJ19N7sND0u-Q8Sq8gVQ","Teaching material 5"),
        ("DAGlcJshM2c/pphZMCBg2RalQTSpuobzVQ","Teaching material 6"),
        ("DAGnltvWcPk/6wH3DYaE30VtPMk_PqqtOw","Teaching material 7"),
    ])
    lo = (
      hero(pick("09-learning-outputs",0),"Learning Outputs & Teaching Materials","Made by learners",
           "Student work and the interactive materials that power our lessons.", short=True)
      + '<section><div class="wrap"><blockquote class="quote-big rvl">“Learning is not the product of teaching. Learning is the product of the activity of learners.”'
        '<span class="by">— John Holt</span></blockquote></div></section>'
      + section('<div class="grid g2">'+lo_games+'</div>', tint=True,
                head=("Play to Learn","Interactive Wordwall games","Tap any game to play it right here."))
      + section('<div class="grid g3">'+lo_canva+'</div>', head=("Teaching Materials","Made in Canva", None))
      + gsec("09-learning-outputs", ("Gallery","Outputs & creations", None), tint=True)
    )
    P["learning-outputs.html"] = page("learning-outputs.html","Learning Outputs",lo)

    # write
    for fn, htmls in P.items():
        with open(os.path.join(ROOT, fn), "w") as f:
            f.write(htmls)
    counts = {k: len(imgs(k)) for _,_ in [(0,0)] for k in [n[0] for n in []]}
    print("Built", len(P), "pages.")
    for key in ["01-home","02-bilingual-initiative","03-english-club","04-english-corner",
                "05-international-sister-school","06-communication-arts","07-about-me",
                "08-learning-activities","09-learning-outputs"]:
        print(f"  {key}: {len(imgs(key))} photos")

if __name__ == "__main__":
    build()
