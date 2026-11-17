"""SNAP SURF TRIPS · genera la web estática EN + ES.
Uso:  python3 -I src/build.py https://www.tu-dominio.com   → dist/public (producción) y dist/preview (para abrir en local)
Todo el contenido vive aquí. Fotos, logos, CSS, JS y PHP en src/static. Ningún nombre de partner en ningún archivo."""
import sys, os, re, json, shutil, pathlib, datetime

SRC = pathlib.Path(__file__).resolve().parent
DIST = SRC.parent / "dist"
DOMAIN = (sys.argv[1] if len(sys.argv) > 1 else "https://TU-DOMINIO.com").rstrip("/")
GA_ID = os.environ.get("SNAP_GA_ID", "")            # ID de Google Analytics 4. Vacío = la web no usa ninguna cookie ni muestra banner.
LISTING = "sagres-surf-house-01"
TODAY = datetime.date.today().isoformat()
DIMS = json.load(open(SRC / "dims.json"))
import hashlib
VER = hashlib.md5(b"".join((SRC / "static/assets" / f).read_bytes() for f in ("site.css", "site.js"))).hexdigest()[:8]
ORG = {"name": "Associació Carving's Maresme", "nif": "G66143009",
       "addr": "C/ Mossèn Cinto Verdaguer 13-15, 08329 Teià (Barcelona), Spain",
       "email": os.environ.get("SNAP_CONTACT_EMAIL", "info@" + DOMAIN.split("//")[-1].removeprefix("www.")), "tel": "+34 618 649 171"}
# Redes: pon la URL cuando exista la cuenta. Vacío = icono visible como «próximamente», sin enlace.
SOCIAL = {"instagram": "https://www.instagram.com/snap_surftrips/"}
IG_HANDLE = "@snap_surftrips"
WA = "https://wa.me/34618649171"
FLAG = {
    "en": '<svg viewBox="0 0 60 30" width="24" height="12" aria-hidden="true"><clipPath id="fl-a"><path d="M0 0v30h60V0z"/></clipPath><clipPath id="fl-b"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath><g clip-path="url(#fl-a)"><path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30m0-30L0 30" clip-path="url(#fl-b)" stroke="#C8102E" stroke-width="4"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></g></svg>',
    "es": '<svg viewBox="0 0 30 20" width="18" height="12" aria-hidden="true"><path fill="#AA151B" d="M0 0h30v20H0z"/><path fill="#F1BF00" d="M0 5h30v10H0z"/></svg>',
}
ICON = {
    "instagram": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1.2-1.4-2-.9-.8.8a4 4 0 0 1-2.4-2.4l.8-.8-.9-2z" fill="currentColor" stroke="none"/></svg>',
}
LANG = "en"
PREVIEW = False
CUR = ""


def L(en, es):
    return en if LANG == "en" else es


# clave: (ruta EN, ruta ES)
PATHS = {
    "home": ("", "es/"),
    "sagres": ("surf-trips/sagres/", "es/viajes-surf/sagres/"),
    "groups": ("group-surf-trips/", "es/viajes-surf-grupos/"),
    "camps": ("for-surf-camps/", "es/para-surf-camps/"),
    "contact": ("contact/", "es/contacto/"),
    "faq": ("faq/", "es/preguntas-frecuentes/"),
    "notice": ("legal/legal-notice/", "es/legal/aviso-legal/"),
    "privacy": ("legal/privacy-policy/", "es/legal/privacidad/"),
    "cookies": ("legal/cookie-policy/", "es/legal/cookies/"),
    "terms": ("legal/terms/", "es/legal/condiciones/"),
}


def path(key, lang=None):
    return PATHS[key][0 if (lang or LANG) == "en" else 1]


def rel(target):
    """URL interna: absoluta desde la raíz en producción; relativa (con index.html) en la vista previa."""
    if not PREVIEW:
        return "/" + target
    r = os.path.relpath(target or ".", CUR or ".").replace(os.sep, "/")
    if "." in target.rsplit("/", 1)[-1]:
        return r
    return ("" if r == "." else r + "/") + "index.html"


def url(key, anchor=""):
    return rel(path(key)) + anchor


PRELOAD = []
OG = {"bali": "og-bali.jpg"}


def pic(name, alt, cls="ph", eager=False, sizes="(max-width:860px) 100vw, 50vw"):
    w, h = DIMS[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    b = rel("img/" + name + ".jpg")[:-4]
    if eager and not PRELOAD:
        PRELOAD.append(f'<link rel="preload" as="image" type="image/webp" imagesrcset="{b}-560.webp 640w, {b}.webp {w}w, {b}-1800.webp 1800w" imagesizes="{sizes}" fetchpriority="high">')
    return (f'<div class="{cls}"><picture><source type="image/webp" srcset="{b}-560.webp 640w, {b}.webp {w}w, {b}-1800.webp 1800w" sizes="{sizes}">'
            f'<img src="{b}.jpg" alt="{alt}" width="{w}" height="{h}" {load}></picture></div>')


def field(label, name, typ="text", req=False, extra=""):
    ac = {"name": "name", "email": "email", "phone": "tel", "country": "country-name", "organisation": "organization"}.get(name)
    a = f' autocomplete="{ac}"' if ac else ""
    return f'<label>{label}{" *" if req else ""}<input type="{typ}" name="{name}"{" required" if req else ""}{a} {extra}></label>'


def select(label, name, opts):
    return f'<label>{label}<select name="{name}">' + "".join(f"<option>{x}</option>" for x in [""] + opts) + "</select></label>"


def levels():
    return L(["Never surfed", "Beginner", "Intermediate", "Advanced", "Mixed levels"],
             ["Nunca he surfeado", "Principiante", "Intermedio", "Avanzado", "Niveles mixtos"])


def form(kind, fields, cta, hidden=""):
    return f'''<form class="enq" data-type="{kind}" novalidate>
{fields}
<label class="full">{L("Anything else we should know?", "¿Algo más que debamos saber?")}<textarea name="message" rows="4"></textarea></label>
<input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{hidden}
<p class="small full">{L(f"Data controller: {ORG['name']} (SNAP SURF TRIPS). Purpose: to answer your enquiry and prepare your proposal. Legal basis: steps taken at your request before a contract. Recipients: the accommodation and surf school only if you ask for a proposal or booking, and our technology providers. You can access, rectify or erase your data at {ORG['email']}.",
 f"Responsable: {ORG['name']} (SNAP SURF TRIPS). Finalidad: responder a tu solicitud y preparar tu propuesta. Base jurídica: medidas precontractuales a petición tuya. Destinatarios: el alojamiento y la escuela de surf solo si pides propuesta o reserva, y nuestros proveedores tecnológicos. Puedes acceder, rectificar o suprimir tus datos en {ORG['email']}.")} <a href="{url("privacy")}">{L("More information", "Más información")}</a>.</p>
<label class="check full"><input type="checkbox" name="consent" required><span>{L("I have read and accept the", "He leído y acepto la")} <a href="{url("privacy")}">{L("privacy policy", "política de privacidad")}</a> *</span></label>
<label class="check full"><input type="checkbox" name="marketing"><span>{L("I want to receive surf trip news and offers by email (optional).", "Quiero recibir novedades y ofertas de viajes de surf por email (opcional).")}</span></label>
<p class="err full" role="alert" hidden></p>
<button class="btn btn-ink full" type="submit">{cta}</button>
<p class="small full">{L("Sending an enquiry is not a booking. We reply with a personalised proposal.", "Enviar una solicitud no es una reserva. Te respondemos con una propuesta personalizada.")}</p>
</form>'''


def f_ind():
    return (field(L("Name", "Nombre"), "name", req=True) + field("Email", "email", "email", True)
            + field(L("Phone / WhatsApp", "Teléfono / WhatsApp"), "phone", "tel") + field(L("Country", "País"), "country")
            + field(L("How many people?", "¿Cuántas personas?"), "people", "number", extra='min="1" max="19"')
            + field(L("Preferred dates", "Fechas preferidas"), "dates", extra=f'placeholder="{L("e.g. 10–17 May, or just June", "p. ej. 10–17 mayo, o solo junio")}"')
            + select(L("Nights", "Noches"), "nights", ["3", "5", "7", L("Other", "Otra")])
            + select(L("Surf level", "Nivel de surf"), "level", levels())
            + f'<label class="check full"><input type="checkbox" name="flexible"><span>{L("My dates are flexible", "Mis fechas son flexibles")}</span></label>')


def f_group():
    return (field(L("Organisation", "Organización"), "organisation") + field(L("Contact person", "Persona de contacto"), "name", req=True)
            + field("Email", "email", "email", True) + field(L("Phone / WhatsApp", "Teléfono / WhatsApp"), "phone", "tel")
            + select(L("Type of group", "Tipo de grupo"), "groupType",
                     L(["School (16+)", "University / Erasmus", "Club / association", "Private group", "Company / team building", "Travel agency"],
                       ["Instituto o colegio (16+)", "Universidad / Erasmus", "Club / asociación", "Grupo privado", "Empresa / team building", "Agencia de viajes"]))
            + field(L("Participants (approx.)", "Participantes (aprox.)"), "people", "number", extra='min="2"')
            + select(L("Ages", "Edades"), "ages", L(["All 18+", "16–17 with accompanying adults", "Mixed"], ["Todos +18", "16–17 con adultos acompañantes", "Mixto"]))
            + field(L("Preferred destination", "Destino preferido"), "destination", extra='value="Sagres, Algarve"')
            + field(L("Preferred dates", "Fechas preferidas"), "dates") + field(L("Nights", "Noches"), "nights")
            + select(L("Surf level", "Nivel de surf"), "level", levels()) + field(L("Approx. budget per person", "Presupuesto aprox. por persona"), "budget")
            + field(L("Accommodation, meals, transport, activities…", "Alojamiento, comidas, transporte, actividades…"), "needs").replace("<label>", "<label class=\"full\">", 1)
            + f'<label class="check full"><input type="checkbox" name="flexible"><span>{L("Our dates are flexible", "Nuestras fechas son flexibles")}</span></label>')


def f_camp():
    return (field(L("Surf camp / surf house", "Surf camp / surf house"), "organisation", req=True) + field(L("Contact person", "Persona de contacto"), "name", req=True)
            + field("Email", "email", "email", True) + field(L("Phone / WhatsApp", "Teléfono / WhatsApp"), "phone", "tel")
            + field(L("Location", "Ubicación"), "destination") + field(L("Website", "Web"), "campWebsite") + field(L("Beds / capacity", "Camas / capacidad"), "people"))


def f_gen():
    return field(L("Name", "Nombre"), "name", req=True) + field("Email", "email", "email", True) + field(L("Phone / WhatsApp", "Teléfono / WhatsApp"), "phone", "tel")


def mini():
    s = L(["You send your enquiry", "We check availability", "You get your proposal"], ["Envías tu solicitud", "Comprobamos la disponibilidad", "Recibes tu propuesta"])
    return '<ol class="mini">' + "".join(f"<li><b>0{i+1}</b>{x}</li>" for i, x in enumerate(s)) + "</ol>"


def disclaimer():
    return L("Every trip is quoted personally: the price depends on your dates, room type, number of people and services. You receive it in your proposal, with no commitment.",
             "Cada viaje se presupuesta de forma personalizada: el precio depende de las fechas, el tipo de habitación, el número de personas y los servicios. Lo recibes en tu propuesta, sin compromiso.")


# ---------- preguntas frecuentes (también alimentan los datos estructurados) ----------
def faqs():
    return [
        (L("What is SNAP SURF TRIPS?", "¿Qué es SNAP SURF TRIPS?"),
         L("SNAP SURF TRIPS is a commercial agent for surf camps and surf houses around the world, starting in Sagres, Portugal. We present their surf trips to individual travellers and groups and manage your enquiry: you send one request, we check availability with the accommodation and the surf school, and you receive one personalised proposal. The services are provided by the accommodation and the surf school.",
           "SNAP SURF TRIPS es un agente comercial de surf camps y surf houses de todo el mundo, empezando por Sagres (Portugal). Presentamos sus viajes de surf a viajeros particulares y a grupos y gestionamos tu solicitud: envías una petición, comprobamos la disponibilidad con el alojamiento y la escuela de surf, y recibes una propuesta personalizada. Los servicios los prestan el alojamiento y la escuela de surf.")),
        (L("Is sending an enquiry a booking?", "¿Enviar una solicitud es hacer una reserva?"),
         L("No. An enquiry only asks for availability and price. Nothing is booked or charged until you accept the proposal we send you.",
           "No. La solicitud solo pide disponibilidad y precio. No se reserva ni se cobra nada hasta que aceptas la propuesta que te enviamos.")),
        (L("How much does a surf trip to Sagres cost?", "¿Cuánto cuesta un viaje de surf a Sagres?"),
         L("Every trip is quoted personally. The price depends on your dates, room type, number of people and surf days. Send an enquiry and you receive a proposal with the exact price, with no commitment.",
           "Cada viaje se presupuesta de forma personalizada. El precio depende de las fechas, el tipo de habitación, el número de personas y los días de surf. Envía una solicitud y recibes una propuesta con el precio exacto, sin compromiso.")),
        (L("What is included in the surf packages?", "¿Qué incluyen los packs de surf?"),
         L("The 3-night package includes 3 breakfasts, 1 day of surf and transport to the spot. The 5-night package includes 5 breakfasts, 2 days of surf and transport. The 7-night package includes 7 breakfasts, 5 days of surf with 2 sessions of 1 h 30 a day, transport, equipment, picnic and insurance. Flights and airport transfers are not part of the packages.",
           "El pack de 3 noches incluye 3 desayunos, 1 día de surf y transporte al spot. El de 5 noches, 5 desayunos, 2 días de surf y transporte. El de 7 noches, 7 desayunos, 5 días de surf con 2 sesiones de 1 h 30 al día, transporte, material, picnic y seguro. Los vuelos y los traslados desde el aeropuerto no forman parte de los packs.")),
        (L("When can I go?", "¿Cuándo puedo ir?"),
         L("Sagres: the surf house is open from March to December. Bali: open all year.", "Sagres: la surf house abre de marzo a diciembre. Bali: abierto todo el año.")),
        (L("Where exactly is the accommodation?", "¿Dónde está exactamente el alojamiento?"),
         L("In the destination you choose: Sagres, in the Algarve (Portugal), or the Bukit peninsula in Bali (Indonesia). You receive the exact details together with your proposal and booking confirmation.",
           "En el destino que elijas: Sagres, en el Algarve (Portugal), o la península de Bukit en Bali (Indonesia). Recibes los datos exactos junto con tu propuesta y la confirmación de la reserva.")),
        (L("Do you organise surf trips for groups?", "¿Organizáis viajes de surf para grupos?"),
         L("Yes. Together with the surf camp we prepare closed proposals for schools, universities and Erasmus groups, clubs and associations, private groups and companies. Group prices are always quoted on request. School groups are for students aged 16 and over and are organised through the school.",
           "Sí. Junto con el surf camp preparamos propuestas cerradas para institutos y colegios, universidades y grupos Erasmus, clubs y asociaciones, grupos privados y empresas. El precio para grupos siempre se presupuesta a medida. Los grupos escolares son para alumnos de 16 años o más y se organizan a través del centro.")),
        (L("How do I pay?", "¿Cómo se paga?"),
         L("Payment terms are detailed in your proposal before you confirm anything.", "Las condiciones de pago se detallan en tu propuesta antes de que confirmes nada.")),
    ]


# ---------- páginas ----------
def home():
    return f'''
<section class="hero rule">
<div class="hero-txt">
<h1 class="kicker">{L("Surf trips and surf camps around the world", "Viajes de surf y surf camps por todo el mundo")}</h1>
<p class="mega">{L("You surf.<br>We handle<br><mark>the rest.</mark>", "Tú surfeas.<br>Nosotros,<br><mark>el resto.</mark>")}</p>
<p class="lead">{L("Curated surf camps and surf houses for travellers and groups. Tell us when, who and your surf level: we check availability and send you one personalised proposal.",
                    "Surf camps y surf houses seleccionados para viajeros y grupos. Dinos cuándo, quiénes y vuestro nivel: comprobamos la disponibilidad y te enviamos una propuesta personalizada.")}</p>
<div class="row"><a class="btn btn-accent" href="{url("sagres")}">{L("Find my surf trip", "Buscar mi viaje de surf")}</a><a class="btn" href="{url("groups")}">{L("I'm organising a group", "Organizo un grupo")}</a></div>
</div>
{pic("sagres-surf-carve", L("Surfer carving a turquoise wave below a sea cliff", "Surfista surcando una ola turquesa bajo un acantilado"), "ph hero-ph", True)}
</section>

<section class="ticker" aria-hidden="true"><div>{L("<span>Surf trips</span><span>Surf camps</span><span>Surf houses</span><span>Group trips</span><span>Sagres</span><span>Bali</span><span>Coming soon: more destinations</span>","<span>Viajes de surf</span><span>Surf camps</span><span>Surf houses</span><span>Grupos</span><span>Sagres</span><span>Bali</span><span>Pronto: más destinos</span>")}{L("<span>Surf trips</span><span>Surf camps</span><span>Surf houses</span><span>Group trips</span><span>Sagres</span><span>Bali</span><span>Coming soon: more destinations</span>","<span>Viajes de surf</span><span>Surf camps</span><span>Surf houses</span><span>Grupos</span><span>Sagres</span><span>Bali</span><span>Pronto: más destinos</span>")}</div></section>

<section class="three rule">
<a href="{url("sagres")}"><span class="kicker">A /</span><span class="h3">{L("I want to surf", "Quiero surfear")}</span><span>{L("Solo, as a couple or with friends. Surf packages of 3, 5 and 7 nights. →", "Por tu cuenta, en pareja o con amigos. Packs de surf de 3, 5 y 7 noches. →")}</span></a>
<a class="accent" href="{url("groups")}"><span class="kicker">B /</span><span class="h3">{L("I'm organising a group", "Organizo un grupo")}</span><span>{L("Schools, universities, clubs, companies. A closed proposal built for your group. →", "Institutos, universidades, clubs, empresas. Una propuesta cerrada para vuestro grupo. →")}</span></a>
<a href="{url("camps")}"><span class="kicker">C /</span><span class="h3">{L("I run a surf camp", "Tengo un surf camp")}</span><span>{L("Join the SNAP partner network. →", "Únete a la red de partners de SNAP. →")}</span></a>
</section>

<section class="pad rule">
<div class="head"><h2 class="big">{L("Surf destinations", "Destinos de surf")}</h2><p class="kicker">{L("Where we surf", "Dónde surfeamos")}</p></div>
<a class="feature" href="{url("sagres")}">
{pic("sagres-coast", L("Beach and cliffs near Sagres, Algarve", "Playa y acantilados cerca de Sagres, Algarve"), "ph pano", sizes="100vw")}
<div class="feature-meta"><span class="h2">Sagres</span><span class="kicker">Portugal · Algarve</span></div>
<p>{L("Surf house with pool · surf packages of 3, 5 and 7 nights", "Surf house con piscina · packs de surf de 3, 5 y 7 noches")}</p>
</a>
{home_more()}
</section>

<section class="split dark rule">
<div class="pad"><p class="kicker accent-t">{L("How it works", "Cómo funciona")}</p><h2 class="big">{L("One enquiry.<br>One proposal.", "Una solicitud.<br>Una propuesta.")}</h2></div>
<ol class="steps pad">
<li><b>01</b><span>{L("You choose a trip and send us your dates, group size and surf level.", "Eliges un viaje y nos envías fechas, número de personas y nivel de surf.")}</span></li>
<li><b>02</b><span>{L("We check availability and conditions with the accommodation.", "Comprobamos disponibilidad y condiciones con el alojamiento.")}</span></li>
<li><b>03</b><span>{L("You receive a personalised proposal with the final price.", "Recibes una propuesta personalizada con el precio final.")}</span></li>
<li><b>04</b><span>{L("You confirm. We coordinate the booking until you arrive.", "Confirmas. Coordinamos la reserva hasta tu llegada.")}</span></li>
</ol>
</section>

<section class="split rule">
{pic("sagres-surf-group", L("Surf group warming up on the beach in the Algarve", "Grupo de surf calentando en la playa en el Algarve"), "ph tall")}
<div class="pad bl">
<p class="kicker">{L("Group surf trips", "Viajes de surf para grupos")}</p>
<h2 class="big">{L("Bring the whole crew", "Tráete a todo el grupo")}</h2>
<p class="lead">{L("Accommodation, surf lessons, meals and activities in one closed budget for your group. Not sure about dates or numbers yet? Send what you know.",
                    "Alojamiento, clases de surf, comidas y actividades en un presupuesto cerrado para vuestro grupo. ¿Aún sin fechas ni número exacto? Envía lo que sepas.")}</p>
<div class="tags"><span>{L("Schools", "Institutos")}</span><span>{L("Universities &amp; Erasmus", "Universidades y Erasmus")}</span><span>{L("Clubs &amp; associations", "Clubs y asociaciones")}</span><span>{L("Private groups", "Grupos privados")}</span><span>{L("Companies", "Empresas")}</span></div>
<a class="btn btn-ink" href="{url("groups")}">{L("Request a group proposal", "Pedir propuesta de grupo")}</a>
</div>
</section>

<section class="pad rule cta-line">
<div><p class="kicker">{L("For surf camps", "Para surf camps")}</p><h2 class="h2">{L("Do you run a surf camp or surf house?", "¿Tienes un surf camp o una surf house?")}</h2></div>
<a class="btn" href="{url("camps")}">{L("Join the SNAP network", "Únete a la red SNAP")}</a>
</section>

{match_cta()}
{home_guides()}
{ig_block()}
<section class="pad accent closing">
<h2 class="mega">{L("Ready when<br>you are.", "Cuando<br>tú digas.")}</h2>
<a class="btn btn-ink" href="{url("contact")}">{L("Send an enquiry", "Enviar solicitud")}</a>
<p class="small">{disclaimer()}</p>
</section>'''


def sagres():
    ask = L("Ask for this one →", "Pedir este →")
    return f'''
<section class="pad rule">
<p class="kicker">Portugal · Algarve</p>
<h1 class="mega">{L("Surf trip<br>to <mark>Sagres</mark>", "Viaje de surf<br>a <mark>Sagres</mark>")}</h1>
<p class="lead">{L("A surf house with pool in Sagres, at the south-western tip of the Algarve, with its own surf school. Surf packages of 3, 5 and 7 nights, quoted for your dates.",
                    "Una surf house con piscina en Sagres, en el extremo suroeste del Algarve, con escuela de surf propia. Packs de surf de 3, 5 y 7 noches, presupuestados para tus fechas.")}</p>
</section>
{pic("sagres-cliffs-van", L("Van parked on the cliffs near Sagres", "Furgoneta en los acantilados cerca de Sagres"), "ph pano rule", True, "100vw")}

<section class="split rule">
<div class="pad">
<p class="kicker">{L("The stay", "El alojamiento")}</p>
<h2 class="big">{L("Surf house with pool", "Surf house con piscina")}</h2>
<p class="lead">{L("Private and shared rooms, breakfast included and a surf school on site. Open from March to December.", "Habitaciones privadas y compartidas, desayuno incluido y escuela de surf en la casa. Abierta de marzo a diciembre.")}</p>
<ul class="facts">
<li>{L("Swimming pool", "Piscina")}</li><li>{L("Breakfast included", "Desayuno incluido")}</li><li>{L("Bar-restaurant", "Bar-restaurante")}</li><li>{L("Shared kitchen", "Cocina compartida")}</li><li>{L("Coworking space", "Espacio coworking")}</li><li>Yoga</li>
</ul>
<a class="btn btn-accent" href="#enquire">{L("Get my proposal", "Pedir mi propuesta")}</a>
</div>
{pic("sagres-house-pool", L("Swimming pool of the surf house in Sagres", "Piscina de la surf house en Sagres"), "ph tall bl")}
</section>

<section class="gallery rule" aria-label="{L("Photos", "Fotos")}">
{pic("sagres-house-room", L("Private room in the surf house", "Habitación privada de la surf house"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("sagres-house-dorm", L("Shared room with bunk beds", "Habitación compartida con literas"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("sagres-house-dinner", L("Guests sharing dinner at the surf house", "Huéspedes cenando juntos en la surf house"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("sagres-house-yoga", L("Yoga session at the surf house", "Sesión de yoga en la surf house"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("sagres-surf-lesson", L("Surf lesson on the beach near Sagres", "Clase de surf en la playa cerca de Sagres"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("sagres-coast", L("Beach and cliffs near Sagres", "Playa y acantilados cerca de Sagres"), sizes="(max-width:860px) 50vw, 33vw")}
</section>

<section class="pad rule">
<div class="head"><h2 class="big">{L("Surf packages in Sagres", "Packs de surf en Sagres")}</h2><p class="kicker">{L("Pick your length", "Elige duración")}</p></div>
<div class="packs">
<article><p class="kicker">{L("3 nights", "3 noches")}</p><h3 class="h3">{L("1 surf day", "1 día de surf")}</h3><p>{L("3 breakfasts, 1 day of surf and transport to the spot.", "3 desayunos, 1 día de surf y transporte al spot.")}</p><a href="#enquire" data-pack="3n-1surf">{ask}</a></article>
<article><p class="kicker">{L("5 nights", "5 noches")}</p><h3 class="h3">{L("2 surf days", "2 días de surf")}</h3><p>{L("5 breakfasts, 2 days of surf and transport to the spot.", "5 desayunos, 2 días de surf y transporte al spot.")}</p><a href="#enquire" data-pack="5n-2surf">{ask}</a></article>
<article class="accent"><p class="kicker">{L("7 nights", "7 noches")}</p><h3 class="h3">{L("5 surf days", "5 días de surf")}</h3><p>{L("7 breakfasts, 5 days of surf with 2 sessions of 1 h 30 a day, transport to the spot, equipment, picnic and insurance.", "7 desayunos, 5 días de surf con 2 sesiones de 1 h 30 al día, transporte al spot, material, picnic y seguro.")}</p><a href="#enquire" data-pack="7n-5surf">{ask}</a></article>
<article><p class="kicker">{L("Tailor-made", "A medida")}</p><h3 class="h3">{L("Your own mix", "Tu propia mezcla")}</h3><p>{L("Surf + yoga, retreats, team building and student groups.", "Surf + yoga, retiros, team building y grupos de estudiantes.")}</p><a href="{url("groups")}">{L("Group proposal →", "Propuesta de grupo →")}</a></article>
</div>
<p class="small">{disclaimer()} {L("Flights and airport transfers are not part of the packages.", "Los vuelos y los traslados desde el aeropuerto no forman parte de los packs.")}</p>
</section>

<section class="split rule" id="enquire">
<div class="pad dark"><p class="kicker accent-t">{L("Enquire", "Solicitud")}</p><h2 class="big">{L("Tell us about your trip", "Cuéntanos tu viaje")}</h2><p class="lead">{L("No payment now. We check availability and come back with your proposal.", "Sin pagar nada ahora. Comprobamos la disponibilidad y te enviamos tu propuesta.")}</p><p><a href="{url("faq")}">{L("Questions? Read the FAQ", "¿Dudas? Lee las preguntas frecuentes")}</a></p>{mini()}</div>
<div class="pad bl">{form("individual", f_ind(), L("Send my enquiry", "Enviar mi solicitud"), f'<input type="hidden" name="listingId" value="{LISTING}"><input type="hidden" name="packageId" value="">')}</div>
</section>'''


def groups():
    def block(h, p, k=None):
        if k:
            return f'<a href="{url(k)}"><h2 class="kicker">{h}</h2><span>{p} →</span></a>'
        return f'<div><h2 class="kicker">{h}</h2><span>{p}</span></div>'
    return f'''
<section class="split rule">
<div class="pad">
<p class="kicker">{L("Group surf trips · Europe and beyond", "Viajes de surf para grupos · Europa y más allá")}</p>
<h1 class="mega">{L("Group<br>surf <mark>trips</mark>", "Viajes de surf<br>para <mark>grupos</mark>")}</h1>
<p class="lead">{L("One closed proposal for your group: accommodation, surf lessons, meals and activities. One contact from the first email to the last wave.",
                    "Una propuesta cerrada para vuestro grupo: alojamiento, clases de surf, comidas y actividades. Un único contacto desde el primer email hasta la última ola.")}</p>
<a class="btn btn-accent" href="#enquire">{L("Request a group proposal", "Pedir propuesta de grupo")}</a>
</div>
{pic("sagres-surf-lesson", L("Group surf lesson on the beach in the Algarve", "Clase de surf en grupo en la playa en el Algarve"), "ph tall bl", True)}
</section>
<section class="three rule">
{block(L("School surf trips", "Viajes de surf para institutos y colegios"), L("End-of-year and sports trips for students aged 16 and over, always organised with the school and its teachers.", "Viajes de fin de curso y deportivos para alumnos de 16 años o más, siempre organizados con el centro y su profesorado."), "school")}
{block(L("University &amp; Erasmus surf trips", "Viajes de surf para universidades y Erasmus"), L("Student associations, university sports services and Erasmus groups.", "Asociaciones de estudiantes, servicios de deportes universitarios y grupos Erasmus."), "uni")}
{block(L("Clubs &amp; associations", "Clubs y asociaciones"), L("Sports clubs, surf clubs and youth associations.", "Clubs deportivos, clubs de surf y asociaciones juveniles."))}
</section>
<section class="three rule">
{block(L("Private groups", "Grupos privados"), L("Friends, families and celebrations.", "Amigos, familias y celebraciones."))}
{block(L("Company retreats &amp; team building", "Empresas y team building"), L("Surf, yoga and a place to work together.", "Surf, yoga y un espacio para trabajar en equipo."), "team")}
{block(L("Travel agencies", "Agencias de viajes"), L("A surf product for your group catalogue.", "Un producto de surf para vuestro catálogo de grupos."))}
</section>
<section class="split rule" id="enquire">
<div class="pad dark"><p class="kicker accent-t">{L("Group proposal", "Propuesta de grupo")}</p><h2 class="big">{L("Send what you know", "Envía lo que sepas")}</h2><p class="lead">{L("Only a name and an email are required. Group prices are always quoted on request.", "Solo hacen falta un nombre y un email. El precio para grupos siempre se presupuesta a medida.")}</p>{mini()}</div>
<div class="pad bl">{form("group", f_group(), L("Request a group proposal", "Pedir propuesta de grupo"))}</div>
</section>'''


def camps():
    return f'''
<section class="pad rule">
<h1 class="kicker">{L("Partner network for surf camps and surf houses", "Red de partners para surf camps y surf houses")}</h1>
<p class="mega">{L("Join the<br>SNAP <mark>network</mark>", "Únete a la<br>red <mark>SNAP</mark>")}</p>
<p class="lead">{L("SNAP SURF TRIPS brings groups and individual travellers to partner surf camps and surf houses. We handle the enquiry, the proposal and the coordination of each booking.",
                    "SNAP SURF TRIPS lleva grupos y viajeros particulares a surf camps y surf houses asociados. Gestionamos la solicitud, la propuesta y la coordinación de cada reserva.")}</p>
</section>
<section class="split rule" id="enquire">
<div class="pad dark"><p class="kicker accent-t">Partners</p><h2 class="big">{L("Tell us about your camp", "Háblanos de tu camp")}</h2><p class="lead">{L("We will get in touch to talk about how we could work together.", "Nos pondremos en contacto para ver cómo podemos trabajar juntos.")}</p>{mini()}</div>
<div class="pad bl">{form("partner", f_camp(), L("Send", "Enviar"))}</div>
</section>'''


def contact():
    return f'''
<section class="split rule" id="enquire">
<div class="pad"><h1 class="kicker">{L("Contact SNAP SURF TRIPS", "Contacto SNAP SURF TRIPS")}</h1><p class="mega">{L("Say<br><mark>hello</mark>", "Di<br><mark>hola</mark>")}</p>
<p class="lead">{L("Questions about a surf trip? Write to us here, by email or on WhatsApp.", "¿Dudas sobre un viaje de surf? Escríbenos aquí, por email o por WhatsApp.")}</p>
<p>Email: <a href="mailto:{ORG["email"]}">{ORG["email"]}</a><br>WhatsApp: <a href="https://wa.me/34618649171" rel="noopener">{ORG["tel"]}</a></p>{mini()}</div>
<div class="pad bl">{form("general", f_gen(), L("Send", "Enviar"))}</div>
</section>'''


def faq():
    items = "".join(f'<details><summary><h2>{q}</h2></summary><p>{a}</p></details>' for q, a in faqs())
    return f'''
<section class="pad rule">
<h1 class="kicker">{L("Surf trip FAQ: prices, packages and bookings", "Preguntas frecuentes sobre viajes de surf")}</h1>
<p class="mega">{L("Questions,<br><mark>answered</mark>", "Preguntas<br><mark>frecuentes</mark>")}</p>
</section>
<section class="pad rule faq">{items}
<a class="btn btn-ink" href="{url("contact")}">{L("Ask us something else", "Pregúntanos otra cosa")}</a>
</section>'''


def legal(title, html):
    return f'''<section class="pad rule"><p class="kicker">Legal</p><h1 class="big">{title}</h1><p class="small">{L("Last updated", "Última actualización")}: {TODAY}{L(" · The Spanish version prevails.", "")}</p></section>
<section class="pad prose">{html}</section>'''


def notice():
    o = ORG
    return legal(L("Legal notice", "Aviso legal"), L(f'''
<h2>1. Owner of the website</h2>
<p>In compliance with article 10 of Spanish Law 34/2002 on Information Society Services and Electronic Commerce (LSSI-CE):</p>
<ul><li>Owner: {o["name"]} (trade name: SNAP SURF TRIPS)</li><li>Tax ID (NIF): {o["nif"]}</li><li>Registered address: {o["addr"]}</li><li>Email: {o["email"]}</li><li>Telephone: {o["tel"]}</li><li>Registration: [REGISTRY OF ASSOCIATIONS AND REGISTRATION NUMBER]</li></ul>
<h2>2. Purpose</h2>
<p>This website provides information about surf trips and allows users to send enquiries. SNAP SURF TRIPS manages each enquiry and coordinates the booking with the accommodation and activity providers. Sending an enquiry does not create a booking.</p>
<h2>3. Use of the website</h2>
<p>Users agree to use the website lawfully, to provide truthful information in the forms and not to damage the website or the rights of third parties.</p>
<h2>4. Intellectual property</h2>
<p>Texts, design, logos and photographs belong to the owner or are used with authorisation. They may not be reproduced, distributed or transformed without prior written permission.</p>
<h2>5. Liability</h2>
<p>The information is kept up to date with reasonable care. No prices are published on this website; the binding price and conditions are those of the proposal accepted by the customer. The owner is not responsible for interruptions of the service or for the content of external websites linked from this site.</p>
<h2>6. Applicable law</h2>
<p>This notice is governed by Spanish law. Consumers may bring claims before the courts of their place of residence.</p>''', f'''
<h2>1. Titular del sitio web</h2>
<p>En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE):</p>
<ul><li>Titular: {o["name"]} (nombre comercial: SNAP SURF TRIPS)</li><li>NIF: {o["nif"]}</li><li>Domicilio: {o["addr"].replace("Spain", "España")}</li><li>Email: {o["email"]}</li><li>Teléfono: {o["tel"]}</li><li>Inscripción: [REGISTRO DE ASOCIACIONES Y NÚMERO DE INSCRIPCIÓN]</li></ul>
<h2>2. Objeto</h2>
<p>Este sitio web ofrece información sobre viajes de surf y permite enviar solicitudes. SNAP SURF TRIPS gestiona cada solicitud y coordina la reserva con los proveedores de alojamiento y actividades. El envío de una solicitud no constituye una reserva.</p>
<h2>3. Uso del sitio</h2>
<p>La persona usuaria se compromete a utilizar el sitio de forma lícita, a facilitar datos veraces en los formularios y a no dañar el sitio ni los derechos de terceros.</p>
<h2>4. Propiedad intelectual e industrial</h2>
<p>Los textos, el diseño, los logotipos y las fotografías pertenecen al titular o se utilizan con autorización. No pueden reproducirse, distribuirse ni transformarse sin permiso previo y por escrito.</p>
<h2>5. Responsabilidad</h2>
<p>La información se mantiene actualizada con una diligencia razonable. En este sitio no se publican precios; el precio y las condiciones vinculantes son los de la propuesta aceptada por el cliente. El titular no responde de las interrupciones del servicio ni del contenido de sitios externos enlazados.</p>
<h2>6. Legislación aplicable</h2>
<p>Este aviso se rige por la legislación española. Las personas consumidoras pueden reclamar ante los tribunales de su domicilio.</p>'''))


def privacy():
    o = ORG
    return legal(L("Privacy policy", "Política de privacidad"), L(f'''
<h2>1. Data controller</h2>
<p>{o["name"]} (SNAP SURF TRIPS), NIF {o["nif"]}, {o["addr"]}. Contact for privacy matters: {o["email"]}.</p>
<h2>2. What data we collect</h2>
<p>The data you give us in the forms: name, email, telephone, country, organisation, and the details of your trip (dates, number of people, ages of a group, surf level, needs and budget). We also record the page from which you send the enquiry, its language and, if present in the link you followed, the campaign parameters (UTM). We do not ask for special categories of data.</p>
<h2>3. Purposes and legal bases</h2>
<ul><li>To answer your enquiry and prepare and manage your proposal and booking: steps prior to a contract at your request and performance of the contract (art. 6.1.b GDPR).</li>
<li>To send you news and offers by email, only if you tick the optional box: your consent (art. 6.1.a GDPR), which you can withdraw at any time.</li>
<li>To comply with legal obligations (accounting, tax, attending to your rights): art. 6.1.c GDPR.</li></ul>
<h2>4. How long we keep it</h2>
<p>Enquiries that do not become a booking: up to 24 months after the last contact. Bookings: the periods required by tax and commercial law. Marketing: until you unsubscribe; after that we keep only your email on an exclusion list so that we do not write to you again.</p>
<h2>5. Who receives your data</h2>
<p>The accommodation and the surf school that would provide the service, only when you ask for a proposal or a booking. Providers acting on our behalf as processors: website hosting, email and office tools (Google), CRM tools (HubSpot) and AI-assisted management tools (Anthropic). Some of them may process data outside the European Economic Area under the EU-US Data Privacy Framework or standard contractual clauses. We do not sell your data.</p>
<h2>6. Your rights</h2>
<p>You can exercise your rights of access, rectification, erasure, objection, restriction and portability, and withdraw your consent, by writing to {o["email"]}. You can also lodge a complaint with the Spanish Data Protection Agency (www.aepd.es).</p>
<h2>7. Minors</h2>
<p>The forms are for adults. Trips for school groups are arranged with the school or organisation, never directly with students.</p>
<h2>8. Security</h2>
<p>We apply technical and organisational measures appropriate to the risk: restricted access, encrypted connections and minimisation of the data we keep.</p>''', f'''
<h2>1. Responsable del tratamiento</h2>
<p>{o["name"]} (SNAP SURF TRIPS), NIF {o["nif"]}, {o["addr"].replace("Spain", "España")}. Contacto para privacidad: {o["email"]}.</p>
<h2>2. Qué datos tratamos</h2>
<p>Los que nos facilitas en los formularios: nombre, email, teléfono, país, organización y los datos de tu viaje (fechas, número de personas, edades del grupo, nivel de surf, necesidades y presupuesto). También registramos la página desde la que envías la solicitud, su idioma y, si figuran en el enlace por el que llegaste, los parámetros de campaña (UTM). No pedimos categorías especiales de datos.</p>
<h2>3. Finalidades y bases jurídicas</h2>
<ul><li>Responder a tu solicitud y preparar y gestionar tu propuesta y tu reserva: medidas precontractuales a petición tuya y ejecución del contrato (art. 6.1.b RGPD).</li>
<li>Enviarte novedades y ofertas por email, solo si marcas la casilla opcional: tu consentimiento (art. 6.1.a RGPD y art. 21 LSSI), que puedes retirar en cualquier momento.</li>
<li>Cumplir obligaciones legales (contables, fiscales, atención de derechos): art. 6.1.c RGPD.</li></ul>
<h2>4. Plazos de conservación</h2>
<p>Solicitudes que no acaban en reserva: hasta 24 meses desde el último contacto. Reservas: los plazos que exige la normativa fiscal y mercantil. Comunicaciones comerciales: hasta que te des de baja; después conservamos solo tu email en una lista de exclusión para no volver a escribirte.</p>
<h2>5. Destinatarios</h2>
<p>El alojamiento y la escuela de surf que prestarían el servicio, solo cuando pides una propuesta o una reserva. Proveedores que actúan por cuenta nuestra como encargados del tratamiento: alojamiento web, correo y ofimática (Google), herramientas de CRM (HubSpot) y herramientas de gestión asistida por IA (Anthropic). Algunos pueden tratar datos fuera del Espacio Económico Europeo al amparo del Marco de Privacidad de Datos UE-EE. UU. o de cláusulas contractuales tipo. No vendemos tus datos.</p>
<h2>6. Tus derechos</h2>
<p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad, y retirar tu consentimiento, escribiendo a {o["email"]}. También puedes reclamar ante la Agencia Española de Protección de Datos (www.aepd.es).</p>
<h2>7. Menores</h2>
<p>Los formularios están dirigidos a personas adultas. Los viajes de grupos escolares se gestionan con el centro u organización, nunca directamente con el alumnado.</p>
<h2>8. Seguridad</h2>
<p>Aplicamos medidas técnicas y organizativas adecuadas al riesgo: acceso restringido, conexiones cifradas y minimización de los datos que conservamos.</p>'''))


def cookies():
    if GA_ID:
        table = L('''<table><thead><tr><th>Cookie</th><th>Owner</th><th>Purpose</th><th>Duration</th></tr></thead><tbody>
<tr><td>snap_consent (local storage)</td><td>SNAP SURF TRIPS</td><td>Remembers your choice about cookies. Strictly necessary.</td><td>12 months</td></tr>
<tr><td>_ga, _ga_*</td><td>Google Ireland Ltd.</td><td>Analytics: counts visits and how the site is used. Only with your consent.</td><td>Up to 2 years</td></tr></tbody></table>
<p>Analytics cookies are only installed if you press “Accept”. You can change your choice at any time with the “Cookie settings” link in the footer.</p>''',
                  '''<table><thead><tr><th>Cookie</th><th>Titular</th><th>Finalidad</th><th>Duración</th></tr></thead><tbody>
<tr><td>snap_consent (almacenamiento local)</td><td>SNAP SURF TRIPS</td><td>Recuerda tu elección sobre las cookies. Estrictamente necesaria.</td><td>12 meses</td></tr>
<tr><td>_ga, _ga_*</td><td>Google Ireland Ltd.</td><td>Analítica: cuenta las visitas y cómo se usa el sitio. Solo con tu consentimiento.</td><td>Hasta 2 años</td></tr></tbody></table>
<p>Las cookies analíticas solo se instalan si pulsas «Aceptar». Puedes cambiar tu elección en cualquier momento con el enlace «Configurar cookies» del pie de página.</p>''')
    else:
        table = L("<p><strong>This website does not currently use cookies or any similar technology that requires your consent.</strong> It installs no analytics, advertising or social media cookies, loads no third-party fonts or scripts, and therefore shows no cookie banner. If this changes, we will update this policy and ask for your consent first, with the same ease to accept or to reject.</p>",
                  "<p><strong>Actualmente este sitio web no utiliza cookies ni tecnologías similares que requieran tu consentimiento.</strong> No instala cookies analíticas, publicitarias ni de redes sociales, no carga tipografías ni scripts de terceros y, por eso, no muestra banner de cookies. Si esto cambia, actualizaremos esta política y te pediremos antes tu consentimiento, con la misma facilidad para aceptar que para rechazar.</p>")
    return legal(L("Cookie policy", "Política de cookies"), L(f'''
<h2>1. What cookies are</h2>
<p>Cookies are small files that a website stores on your device. Spanish law (art. 22.2 LSSI-CE) requires your informed consent before installing any cookie that is not strictly necessary.</p>
<h2>2. Cookies used on this website</h2>{table}<p>We count visits anonymously on our own server, without cookies or any identifier: we only record the day, the page visited and the campaign source (for example, Instagram), added up.</p>
<h2>3. How to manage cookies in your browser</h2>
<p>You can block or delete cookies from the settings of your browser (Chrome, Safari, Firefox, Edge). Blocking them does not affect the use of this website.</p>
<h2>4. Controller</h2>
<p>{ORG["name"]} (SNAP SURF TRIPS) · {ORG["email"]}.</p>''', f'''
<h2>1. Qué son las cookies</h2>
<p>Las cookies son pequeños archivos que un sitio web guarda en tu dispositivo. La ley española (art. 22.2 LSSI-CE) exige tu consentimiento informado antes de instalar cualquier cookie que no sea estrictamente necesaria.</p>
<h2>2. Cookies que utiliza este sitio</h2>{table}<p>Contamos las visitas de forma anónima en nuestro propio servidor, sin cookies ni ningún identificador: solo registramos el día, la página visitada y el origen de la campaña (por ejemplo, Instagram), de forma agregada.</p>
<h2>3. Cómo gestionar las cookies en tu navegador</h2>
<p>Puedes bloquear o eliminar las cookies desde la configuración de tu navegador (Chrome, Safari, Firefox, Edge). Bloquearlas no afecta al uso de este sitio.</p>
<h2>4. Responsable</h2>
<p>{ORG["name"]} (SNAP SURF TRIPS) · {ORG["email"]}.</p>'''))


def terms():
    return legal(L("Terms and conditions", "Condiciones generales"), L(f'''
<h2>1. Who we are and what we do</h2>
<p>SNAP SURF TRIPS (a brand of {ORG["name"]}, NIF {ORG["nif"]}) acts as a commercial agent of surf camps and surf houses: it presents their surf trips and manages enquiries. SNAP SURF TRIPS is not a travel agency. The accommodation, surf lessons and other services are provided by independent providers, and the contract for those services is concluded between the customer and the provider.</p>
<h2>2. Enquiries</h2>
<p>An enquiry sent through this website is a request for information. It does not create a booking or any obligation to pay.</p>
<h2>3. Prices</h2>
<p>No prices are published on this website. Every trip is quoted personally and the valid price is the one stated in the written proposal.</p>
<h2>4. Proposal, booking and payment</h2>
<p>After your enquiry we send you a written proposal with the services included, dates, price, payment terms, cancellation terms and the identity of the provider of the services. The booking exists only when you expressly accept that proposal and make the payment it indicates. [BOOKING, PAYMENT AND CANCELLATION TERMS: TO BE COMPLETED WITH THE LEGAL ADVISER]</p>
<h2>5. Travel requirements</h2>
<p>Flights, transfers and travel insurance are not included unless the proposal says so. Each traveller is responsible for valid travel documents. Surfing is a physical activity with inherent risks; participants follow the instructions of the surf school.</p>
<h2>6. Minors</h2>
<p>Minors travel only in groups organised by a school or organisation and accompanied by responsible adults, from the age of 16.</p>
<h2>7. Complaints</h2>
<p>You can send any complaint to {ORG["email"]}. We will answer as soon as possible and in any case within one month.</p>
<h2>8. Applicable law</h2>
<p>These terms are governed by Spanish law. Nothing in them limits the rights that consumer law grants you.</p>''', f'''
<h2>1. Quiénes somos y qué hacemos</h2>
<p>SNAP SURF TRIPS (marca de {ORG["name"]}, NIF {ORG["nif"]}) actúa como agente comercial de surf camps y surf houses: presenta sus viajes de surf y gestiona las solicitudes. SNAP SURF TRIPS no es una agencia de viajes. El alojamiento, las clases de surf y los demás servicios los prestan proveedores independientes, y el contrato de esos servicios se celebra entre el cliente y el proveedor.</p>
<h2>2. Solicitudes</h2>
<p>La solicitud enviada desde este sitio es una petición de información. No constituye una reserva ni genera ninguna obligación de pago.</p>
<h2>3. Precios</h2>
<p>En este sitio no se publican precios. Cada viaje se presupuesta de forma personalizada y el precio válido es el que figura en la propuesta escrita.</p>
<h2>4. Propuesta, reserva y pago</h2>
<p>Tras tu solicitud te enviamos una propuesta escrita con los servicios incluidos, las fechas, el precio, las condiciones de pago y de cancelación y la identidad del prestador de los servicios. La reserva solo existe cuando aceptas expresamente esa propuesta y realizas el pago que indica. [CONDICIONES DE RESERVA, PAGO Y CANCELACIÓN: A COMPLETAR CON EL ASESOR LEGAL]</p>
<h2>5. Requisitos del viaje</h2>
<p>Los vuelos, los traslados y el seguro de viaje no están incluidos salvo que la propuesta lo indique. Cada viajero es responsable de llevar la documentación en regla. El surf es una actividad física con riesgos propios; los participantes siguen las indicaciones de la escuela de surf.</p>
<h2>6. Menores</h2>
<p>Los menores solo viajan en grupos organizados por un centro u organización y acompañados por adultos responsables, a partir de los 16 años.</p>
<h2>7. Reclamaciones</h2>
<p>Puedes enviar cualquier reclamación a {ORG["email"]}. Responderemos lo antes posible y, en todo caso, en el plazo de un mes.</p>
<h2>8. Legislación aplicable</h2>
<p>Estas condiciones se rigen por la legislación española. Nada de lo aquí dispuesto limita los derechos que te reconoce la normativa de consumo.</p>'''))


# clave: (función, título EN, título ES, descripción EN, descripción ES, etiqueta de miga EN, ES)
exec(open(SRC / "extra.py", encoding="utf-8").read())
PATHS.update(EXTRA_PATHS)

PAGES = {
    "home": (home, "Surf Trips & Surf Camps for Travellers and Groups | SNAP", "Viajes de surf y surf camps para viajeros y grupos | SNAP",
             "Surf trips and surf camps for travellers and groups, starting in Sagres, Portugal. Packages of 3, 5 and 7 nights. One enquiry, one personalised proposal.",
             "Viajes de surf y surf camps para viajeros y grupos, empezando por Sagres (Portugal). Packs de 3, 5 y 7 noches. Una solicitud, una propuesta personalizada.", "Home", "Inicio"),
    "sagres": (sagres, "Surf Camp in Sagres, Algarve: surf & stay packages | SNAP", "Surf camp en Sagres (Algarve): packs de surf y alojamiento | SNAP",
               "Surf house with pool in Sagres, Portugal. Surf packages of 3, 5 and 7 nights with lessons and breakfast. Personalised proposal with no commitment.",
               "Surf house con piscina en Sagres (Portugal). Packs de surf de 3, 5 y 7 noches con clases y desayuno. Propuesta personalizada sin compromiso.", "Sagres", "Sagres"),
    "groups": (groups, "Group Surf Trips: schools, universities, clubs & companies | SNAP", "Viajes de surf para grupos, institutos y universidades | SNAP",
               "Group surf trips for schools, universities, Erasmus groups, clubs and companies. Closed proposal on request.",
               "Viajes de surf para institutos, universidades, grupos Erasmus, clubs y empresas. Propuesta cerrada a medida.", "Group surf trips", "Viajes de surf para grupos"),
    "camps": (camps, "For Surf Camps: join the SNAP partner network", "Para surf camps: únete a la red de partners de SNAP",
              "Do you run a surf camp or surf house? SNAP SURF TRIPS brings you groups and travellers.", "¿Tienes un surf camp o una surf house? SNAP SURF TRIPS te lleva grupos y viajeros.", "For surf camps", "Para surf camps"),
    "contact": (contact, "Contact | SNAP SURF TRIPS", "Contacto | SNAP SURF TRIPS", "Contact SNAP SURF TRIPS by form, email or WhatsApp.", "Contacta con SNAP SURF TRIPS por formulario, email o WhatsApp.", "Contact", "Contacto"),
    "faq": (faq, "Surf Trip FAQ: prices, packages and bookings | SNAP SURF TRIPS", "Preguntas frecuentes: precios, packs y reservas | SNAP SURF TRIPS",
            "Answers about surf trips to Sagres: prices, what is included, season, groups and how booking works.", "Respuestas sobre los viajes de surf a Sagres: precios, qué incluyen, temporada, grupos y cómo se reserva.", "FAQ", "Preguntas frecuentes"),
    "notice": (notice, "Legal notice | SNAP SURF TRIPS", "Aviso legal | SNAP SURF TRIPS", "Legal notice of SNAP SURF TRIPS.", "Aviso legal de SNAP SURF TRIPS.", "Legal notice", "Aviso legal"),
    "privacy": (privacy, "Privacy policy | SNAP SURF TRIPS", "Política de privacidad | SNAP SURF TRIPS", "How SNAP SURF TRIPS handles your personal data.", "Cómo trata SNAP SURF TRIPS tus datos personales.", "Privacy policy", "Política de privacidad"),
    "cookies": (cookies, "Cookie policy | SNAP SURF TRIPS", "Política de cookies | SNAP SURF TRIPS", "Cookies used on the SNAP SURF TRIPS website.", "Cookies que utiliza la web de SNAP SURF TRIPS.", "Cookie policy", "Política de cookies"),
    "terms": (terms, "Terms and conditions | SNAP SURF TRIPS", "Condiciones generales | SNAP SURF TRIPS", "Terms and conditions of SNAP SURF TRIPS.", "Condiciones generales de SNAP SURF TRIPS.", "Terms", "Condiciones"),
}

PAGES.update(EXTRA_PAGES)


def crumbs(key):
    """Migas: Inicio > [padre] > página."""
    c = [("home", L("Home", "Inicio"))]
    if key in PARENT:
        c.append((PARENT[key], PAGES[PARENT[key]][5 if LANG == "en" else 6]))
    c.append((key, PAGES[key][5 if LANG == "en" else 6]))
    return c


def schema(key, title, desc):
    org = {"@type": "Organization", "@id": DOMAIN + "/#org", "name": "SNAP SURF TRIPS", "legalName": ORG["name"], "url": DOMAIN + "/",
           "logo": DOMAIN + "/img/snap-logo.png", "email": ORG["email"], "telephone": ORG["tel"], "slogan": "You surf. We handle the rest.",
           "areaServed": "Worldwide", "sameAs": [u for u in (SOCIAL["instagram"],) if u], "knowsAbout": ["surf trips", "surf camps", "surf houses", "group surf trips", "Sagres", "Algarve"]}
    g = [org, {"@type": "WebPage", "@id": DOMAIN + "/" + path(key) + "#page", "url": DOMAIN + "/" + path(key), "name": title, "description": desc,
               "inLanguage": LANG, "isPartOf": {"@id": DOMAIN + "/#site"}, "dateModified": TODAY},
         {"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN + "/", "name": "SNAP SURF TRIPS", "publisher": {"@id": DOMAIN + "/#org"}, "inLanguage": ["en", "es"]}]
    if key != "home":
        g.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + "/" + path(k)} for i, (k, n) in enumerate(crumbs(key))]})
    qa = faqs if key == "faq" else PAGE_FAQ.get(key)
    if qa:
        g.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa()]})
    if key in GUIDES:
        g.append({"@type": "Article", "headline": title.split(" | ")[0], "description": desc, "inLanguage": LANG, "datePublished": TODAY, "dateModified": TODAY,
                  "author": {"@id": DOMAIN + "/#org"}, "publisher": {"@id": DOMAIN + "/#org"}, "image": DOMAIN + "/img/og.jpg", "mainEntityOfPage": DOMAIN + "/" + path(key)})
    if key == "bali":
        g.append({"@type": "TouristTrip", "name": L("Surf trip to Bali", "Viaje de surf a Bali"), "description": desc, "touristType": ["Surfers", "Remote workers", "Small groups"], "provider": {"@id": DOMAIN + "/#org"},
                  "itinerary": {"@type": "Place", "name": "Bukit peninsula, Bali, Indonesia", "address": {"@type": "PostalAddress", "addressRegion": "Bali", "addressCountry": "ID"}}})
    if key == "sagres":
        g.append({"@type": "TouristTrip", "name": L("Surf trip to Sagres, Algarve", "Viaje de surf a Sagres, Algarve"), "description": desc,
                  "touristType": ["Surfers", "Beginners", "Groups"], "provider": {"@id": DOMAIN + "/#org"},
                  "itinerary": {"@type": "Place", "name": "Sagres, Algarve, Portugal", "address": {"@type": "PostalAddress", "addressLocality": "Sagres", "addressRegion": "Algarve", "addressCountry": "PT"}},
                  "image": DOMAIN + "/img/sagres-coast.jpg"})
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False)


def page(key):
    fn, t_en, t_es, d_en, d_es, _, _ = PAGES[key]
    title, desc = L(t_en, t_es), L(d_en, d_es)
    PRELOAD.clear()
    body = fn()
    if key in SHARE:
        body += share(key, title.split(" | ")[0])
    other = "es" if LANG == "en" else "en"
    canon = DOMAIN + "/" + path(key)
    NOINDEX = '<meta name="robots" content="noindex,nofollow">\n' if PREVIEW else ""
    logo = f'<img src="{rel("img/snap-logo.png")}" alt="SNAP SURF TRIPS" width="900" height="214">'
    nav = (f'<a href="{url("trips")}">{L("Surf trips", "Viajes de surf")}</a><a href="{url("groups")}">{L("Groups", "Grupos")}</a>'
           f'<a href="{url("camps")}">{L("For surf camps", "Para surf camps")}</a><a href="{url("faq")}">FAQ</a><a href="{url("contact")}">{L("Contact", "Contacto")}</a>')
    langs = "".join(
        f'<a href="{rel(path(key, lg))}" hreflang="{lg}" lang="{lg}" title="{name}"' + (' aria-current="true"' if lg == LANG else "") + f'>{FLAG[lg]}<span>{lg.upper()}</span></a>'
        for lg, name in (("en", "English"), ("es", "Español")))
    langsw = f'<nav class="lang" aria-label="{L("Language", "Idioma")}">{langs}</nav>'
    ig = SOCIAL["instagram"]
    ig_html = (f'<a href="{ig}" target="_blank" rel="noopener" aria-label="Instagram ({L("opens in a new tab", "se abre en una pestaña nueva")})">{ICON["instagram"]}</a>' if ig else
               f'<span class="soon" role="img" aria-label="Instagram ({L("coming soon", "próximamente")})" title="Instagram · {L("coming soon", "próximamente")}">{ICON["instagram"]}</span>')
    social = f'<div class="social">{ig_html}<a href="{WA}" rel="noopener" aria-label="WhatsApp">{ICON["whatsapp"]}</a></div>'
    cr = crumbs(key)
    crumb = "" if key == "home" else '<nav class="crumb" aria-label="Breadcrumb">' + " / ".join(f'<a href="{url(k)}">{n}</a>' for k, n in cr[:-1]) + f' / <span aria-current="page">{cr[-1][1]}</span></nav>'
    banner = "" if not GA_ID else f'''<div id="ck" class="ck" role="dialog" aria-label="Cookies" hidden>
<p>{L("We use analytics cookies to understand how the site is used. They are only installed if you accept.", "Usamos cookies analíticas para saber cómo se utiliza el sitio. Solo se instalan si las aceptas.")} <a href="{url("cookies")}">{L("Cookie policy", "Política de cookies")}</a></p>
<div class="row"><button class="btn sm" type="button" data-ck="0">{L("Reject", "Rechazar")}</button><button class="btn sm" type="button" data-ck="1">{L("Accept", "Aceptar")}</button></div></div>'''
    cks = "" if not GA_ID else f'<a href="#" id="ck-open">{L("Cookie settings", "Configurar cookies")}</a>'
    return f'''<!DOCTYPE html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{DOMAIN}/{path(key, "en")}">
<link rel="alternate" hreflang="es" href="{DOMAIN}/{path(key, "es")}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{path(key, "en")}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SNAP SURF TRIPS">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/img/{OG.get(key, "og.jpg")}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title}">
<meta property="og:locale" content="{L("en_GB", "es_ES")}">
{NOINDEX}<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFF8EE">
<link rel="icon" href="{rel("img/favicon.png")}">
<link rel="apple-touch-icon" href="{rel("img/favicon.png")}">
{"".join(PRELOAD)}
<link rel="preload" href="{rel("assets/fonts/anton.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{rel("assets/fonts/archivo.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel("assets/site.css")}?v={VER}">
<script type="application/ld+json">{schema(key, title, desc)}</script>
</head>
<body data-api="{rel("api/enquiry.php")}" data-ga="{GA_ID}" data-req="{L("Please fill in the fields marked with * and accept the privacy policy.", "Rellena los campos marcados con * y acepta la política de privacidad.")}" data-fail="{L("Sorry, your enquiry could not be sent. Please try again or write to us on WhatsApp", "Lo sentimos, no se ha podido enviar tu solicitud. Inténtalo de nuevo o escríbenos por WhatsApp")} {ORG["tel"]}." data-ref="{L("Reference", "Referencia")}">
<a class="skip" href="#main">{L("Skip to content", "Saltar al contenido")}</a>
<header class="top rule">
<a class="logo" href="{url("home")}">{logo}</a>
<nav id="mainnav" aria-label="{L("Main", "Principal")}">{nav}</nav>
{langsw}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mainnav"><span></span>{L("Menu", "Menú")}</button>
<a class="btn btn-ink sm" href="{url("sagres", "#enquire")}">{L("Plan my trip", "Planear mi viaje")}</a>
</header>
<main id="main">{crumb}{body}</main>
<footer class="foot">
<div><a class="logo" href="{url("home")}">{logo}</a><p class="small">{L("Surf trips around the world for travellers and groups.", "Viajes de surf por el mundo para viajeros y grupos.")}<br>{ORG["email"]} · {ORG["tel"]}</p>{social}</div>
<nav aria-label="{L("Site", "Sitio")}"><a href="{url("trips")}">{L("Surf destinations", "Destinos de surf")}</a><a href="{url("match")}">{L("Surf trip matcher", "Encuentra tu surf trip")}</a><a href="{url("sagres")}">{L("Surf trip to Sagres", "Viaje de surf a Sagres")}</a><a href="{url("groups")}">{L("Group surf trips", "Viajes de surf para grupos")}</a><a href="{url("camps")}">{L("For surf camps", "Para surf camps")}</a><a href="{url("guides")}">{L("Surf guides", "Guías de surf")}</a><a href="{url("faq")}">FAQ</a><a href="{url("contact")}">{L("Contact", "Contacto")}</a></nav>
<nav aria-label="Legal"><a href="{url("notice")}">{L("Legal notice", "Aviso legal")}</a><a href="{url("privacy")}">{L("Privacy policy", "Privacidad")}</a><a href="{url("cookies")}">{L("Cookie policy", "Cookies")}</a><a href="{url("terms")}">{L("Terms", "Condiciones")}</a>{cks}</nav>
<p class="small legal-line">© {TODAY[:4]} SNAP SURF TRIPS · {L("A brand of", "Marca de")} {ORG["name"]} · NIF {ORG["nif"]}</p>
</footer>
<dialog id="ok" aria-labelledby="ok-t">
<svg viewBox="0 0 400 60" aria-hidden="true"><path d="M0 40 Q25 10 50 40 T100 40 T150 40 T200 40 T250 40 T300 40 T350 40 T400 40 V60 H0Z"/></svg>
<img class="dlg-ic" src="{rel("img/snap-wave.png")}" alt="" width="72" height="42">
<p class="kicker">{L("Enquiry received", "Solicitud recibida")}</p>
<h2 id="ok-t" class="big">{L("Shaka!<br>We got it.", "¡Shaka!<br>La tenemos.")}</h2>
<p>{L("Your enquiry is in. We're checking the line-up and will get back to you shortly.", "Tu solicitud ya está en el agua. Estamos mirando el line-up y te escribimos en breve.")}</p>
<p class="small" id="ok-ref"></p>
<button class="btn btn-ink" type="button" id="ok-x">{L("Back to the waves", "Volver a las olas")}</button>
</dialog>
<a class="wa-fab" href="{WA}" rel="noopener" aria-label="WhatsApp">{ICON["whatsapp"]}</a>
{banner}
<script src="{rel("assets/site.js")}?v={VER}" defer></script>
</body>
</html>
'''


def not_found():
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found | SNAP SURF TRIPS</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/site.css"></head>
<body><main class="pad"><p class="kicker">404</p><h1 class="mega">Wipe<br><mark>out.</mark></h1><p class="lead">This page does not exist. · Esta página no existe.</p><div class="row"><a class="btn btn-ink" href="/">Home</a><a class="btn" href="/es/">Inicio</a></div></main></body></html>'''


def llms():
    return f'''# SNAP SURF TRIPS

> SNAP SURF TRIPS is a commercial agent for surf camps and surf houses around the world (first destination: Sagres, Portugal; more coming). It presents their surf trips to individual travellers and for groups (schools 16+, universities, Erasmus, clubs, private groups, companies). Customers send one enquiry and receive one personalised proposal. An enquiry is not a booking.

## Key facts
- Destination: Bali (Indonesia), Bukit peninsula / Uluwatu area. Boutique surf & coworking hotel with pool, breakfast, spa. Open all year; travellers and small groups up to 18; adults only.
- Destination available: Sagres, Algarve, Portugal. Surf house with pool, private and shared rooms, breakfast included, own surf school. Open March to December.
- Surf packages: 3 nights + 1 surf day; 5 nights + 2 surf days; 7 nights + 5 surf days (2 sessions of 1 h 30 a day, equipment, picnic and insurance). Tailor-made options.
- Prices: no public price list. Every trip is quoted personally in a proposal, with no commitment.
- Group surf trips: price always quoted on request. School groups from age 16, organised through the school.
- Flights and airport transfers are not part of the packages.
- Contact: {ORG["email"]} · WhatsApp {ORG["tel"]}
- Operator: {ORG["name"]} (brand SNAP SURF TRIPS), Barcelona, Spain.

## Pages
- [Surf trip to Sagres]({DOMAIN}/{PATHS["sagres"][0]}): accommodation, packages and enquiry form
- [Group surf trips]({DOMAIN}/{PATHS["groups"][0]}): schools, universities, clubs, companies
- [Surf destinations]({DOMAIN}/{PATHS["trips"][0]})
- [End-of-year school surf trips (16+)]({DOMAIN}/{PATHS["school"][0]})
- [University & Erasmus surf trips]({DOMAIN}/{PATHS["uni"][0]})
- [Surf team building & company retreats]({DOMAIN}/{PATHS["team"][0]})
- [Guides]({DOMAIN}/{PATHS["guides"][0]}): how to organise a group surf trip, packing list, first surf trip
- [FAQ]({DOMAIN}/{PATHS["faq"][0]}): prices, inclusions, season, booking process
- [For surf camps]({DOMAIN}/{PATHS["camps"][0]}): partner network
- [Contact]({DOMAIN}/{PATHS["contact"][0]})
- Español: {DOMAIN}/es/
'''


def build(out, preview):
    global LANG, PREVIEW, CUR
    PREVIEW = preview
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SRC / "static", out)
    # minificar con csso (fusiona reglas repetidas) y terser; si no están, se deja el original
    import subprocess
    nm = pathlib.Path(os.environ.get("SNAP_NODE_MODULES", "/tmp/fnt/node_modules/.bin"))
    for tool, f, args in (("csso", "assets/site.css", ["--restructure-off"] if os.environ.get("SNAP_CSS_SAFE") else []), ("terser", "assets/site.js", ["-c", "-m"])):
        if (nm / tool).exists():
            r = subprocess.run([str(nm / tool), str(out / f), "-o", str(out / f), *args], capture_output=True, text=True)
            if r.returncode:
                print("aviso", tool, r.stderr[:200])
    for lang in ("en", "es"):
        LANG = lang
        for key in PAGES:
            CUR = path(key)
            d = out / CUR
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(page(key), encoding="utf-8")
    if preview:
        shutil.rmtree(out / "api")
        return
    (out / "404.html").write_text(not_found(), encoding="utf-8")
    ga = " https://www.googletagmanager.com https://*.google-analytics.com" if GA_ID else ""
    csp = (f"default-src 'self'; script-src 'self'{ga}; style-src 'self'; img-src 'self' data:{ga}; font-src 'self'; "
           f"connect-src 'self'{ga}; form-action 'self'; frame-ancestors 'self'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests")
    ht = out / ".htaccess"
    ht.write_text(ht.read_text().replace("#CSP#", f'Header always set Content-Security-Policy "{csp}"'))
    wk = out / ".well-known"; wk.mkdir(exist_ok=True)
    exp = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()
    (wk / "security.txt").write_text(f"Contact: mailto:{ORG['email']}\nExpires: {exp}T00:00:00Z\nPreferred-Languages: es, en\nCanonical: {DOMAIN}/.well-known/security.txt\n")
    (out / "llms.txt").write_text(llms(), encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    urls = ""
    for key in PAGES:
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{DOMAIN}/{PATHS[key][i]}"/>' for h, i in (("en", 0), ("es", 1), ("x-default", 0)))
        for i in (0, 1):
            urls += f"<url><loc>{DOMAIN}/{PATHS[key][i]}</loc><lastmod>{TODAY}</lastmod>{alt}</url>\n"
    (out / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n", encoding="utf-8")


build(DIST / "public", False)
build(DIST / "preview", True)
print("ok ·", len(PAGES) * 2, "páginas · dominio:", DOMAIN)
