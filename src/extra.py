# SNAP · páginas de grupos por intención, índice de destinos, guías e Instagram.
# Se ejecuta dentro de build.py (comparte L, url, pic, form, f_group, mini, LANG...). Solo datos verificados del CRM:
# temporada de grupos mar–jul y 16 sep–dic · grupos desde 20 · menores desde 16 con el centro · packs de camps/sagres-sun-stay.

EXTRA_PATHS = {
    "trips": ("surf-trips/", "es/viajes-surf/"),
    "school": ("group-surf-trips/school-trips/", "es/viajes-surf-grupos/viajes-fin-de-curso/"),
    "uni": ("group-surf-trips/universities-erasmus/", "es/viajes-surf-grupos/universidades-erasmus/"),
    "team": ("group-surf-trips/team-building/", "es/viajes-surf-grupos/team-building-empresas/"),
    "guides": ("guides/", "es/guias/"),
    "g_group": ("guides/how-to-organise-a-group-surf-trip/", "es/guias/como-organizar-viaje-surf-grupo/"),
    "g_pack": ("guides/surf-camp-packing-list/", "es/guias/que-llevar-surf-camp/"),
    "g_first": ("guides/first-surf-trip-beginners/", "es/guias/primer-viaje-surf-principiantes/"),
}
PARENT = {"sagres": "trips", "school": "groups", "uni": "groups", "team": "groups", "g_group": "guides", "g_pack": "guides", "g_first": "guides"}
GUIDES = ("g_group", "g_pack", "g_first")
PAGE_FAQ = {}


def cards(items):
    return '<section class="pad cards">' + "".join(f'<article><h2 class="h3">{h}</h2>{t}</article>' for h, t in items) + "</section>"


def common_blocks():
    return [
        (L("The destination", "El destino"),
         L("<p>Sagres, at the south-western tip of the Algarve, Portugal. Your group stays in a surf house with a swimming pool, private and shared rooms, common areas and its own surf school.</p>",
           "<p>Sagres, en el extremo suroeste del Algarve (Portugal). El grupo se aloja en una surf house con piscina, habitaciones privadas y compartidas, zonas comunes y escuela de surf propia.</p>")),
        (L("What a group trip can include", "Qué puede incluir el viaje"),
         L("<ul><li>Accommodation with breakfast</li><li>Surf lessons for every level, with equipment</li><li>Transport to the surf spot</li><li>Picnic and insurance on the 7-night format</li><li>Yoga and other activities on request</li></ul>",
           "<ul><li>Alojamiento con desayuno</li><li>Clases de surf para todos los niveles, con material</li><li>Transporte al spot</li><li>Picnic y seguro en el formato de 7 noches</li><li>Yoga y otras actividades a petición</li></ul>")),
        (L("Season and group size", "Temporada y tamaño del grupo"),
         L("<p>Group trips run from March to July and from mid-September to December. Group proposals start at 20 people. Fewer than 20? Send your enquiry from the <a href=\"" + url("sagres") + "\">Sagres page</a>.</p>",
           "<p>Los viajes de grupo se hacen de marzo a julio y de mediados de septiembre a diciembre. Las propuestas de grupo son a partir de 20 personas. ¿Sois menos de 20? Envía la solicitud desde la <a href=\"" + url("sagres") + "\">página de Sagres</a>.</p>")),
        (L("How it works", "Cómo funciona"),
         L("<p>You send what you know. We check availability with the accommodation and the surf school and send one closed proposal with the final price. One contact from the first email to the last wave.</p>",
           "<p>Nos envías lo que sepas. Comprobamos la disponibilidad con el alojamiento y la escuela de surf y te mandamos una propuesta cerrada con el precio final. Un único contacto desde el primer email hasta la última ola.</p>")),
    ]


def landing(key, kick, h1, lead, photo, alt, blocks, qa):
    PAGE_FAQ[key] = qa
    q = "".join(f"<details><summary><h3>{x}</h3></summary><p>{y}</p></details>" for x, y in qa())
    return f'''
<section class="split rule">
<div class="pad"><p class="kicker">{kick}</p><h1 class="big">{h1}</h1><p class="lead">{lead}</p><a class="btn btn-orange" href="#enquire">{L("Request a group proposal", "Pedir propuesta de grupo")}</a></div>
{pic(photo, alt, "ph tall", True)}
</section>
{cards(blocks + common_blocks())}
<section class="pad faq"><h2 class="big">{L("Questions", "Preguntas")}</h2>{q}</section>
<section class="split rule" id="enquire">
<div class="pad dark"><p class="kicker orange-t">{L("Group proposal", "Propuesta de grupo")}</p><h2 class="big">{L("Tell us about your group", "Cuéntanos sobre vuestro grupo")}</h2><p class="lead">{L("Only a name and an email are required. Group prices are always quoted on request.", "Solo hacen falta un nombre y un email. El precio para grupos siempre se presupuesta a medida.")}</p>{mini()}</div>
<div class="pad bl">{form("group", f_group(), L("Request a group proposal", "Pedir propuesta de grupo"))}</div>
</section>'''


def school():
    return landing("school", L("Group surf trips · Schools", "Viajes de surf para grupos · Institutos y colegios"),
        L("End-of-year <mark>surf trips</mark> for schools", "Viajes de fin de curso <mark>de surf</mark>"),
        L("A surf week in Sagres for students aged 16 and over, organised with the school and its teachers. Sport, nature and a trip they will remember.",
          "Una semana de surf en Sagres para alumnos de 16 años o más, organizada con el centro y su profesorado. Deporte, naturaleza y un viaje que no olvidarán."),
        "sagres-surf-group", L("Students warming up before a surf lesson", "Alumnos calentando antes de una clase de surf"),
        [(L("Always with the school", "Siempre con el centro"),
          L("<p>We only work with the school or organisation, never directly with students. Minimum age 16, with accompanying teachers.</p>",
            "<p>Trabajamos solo con el centro u organización, nunca directamente con el alumnado. Edad mínima 16 años, con profesorado acompañante.</p>")),
         (L("Supervision and safety", "Supervisión y seguridad"),
          L("<p>Supervision, insurance and house rules for groups with minors are set out in the proposal, before you confirm anything.</p>",
            "<p>La supervisión, el seguro y las normas de la casa para grupos con menores se detallan en la propuesta, antes de que confirméis nada.</p>"))],
        lambda: [(L("From what age?", "¿Desde qué edad?"), L("From 16, travelling as a school group with accompanying teachers.", "Desde los 16 años, viajando como grupo del centro con profesorado acompañante.")),
                 (L("When can a school group travel?", "¿Cuándo puede viajar un grupo escolar?"), L("From March to July and from mid-September to December.", "De marzo a julio y de mediados de septiembre a diciembre.")),
                 (L("Do students need to know how to surf?", "¿Hace falta saber surfear?"), L("No. Lessons are for every level, from first-timers up.", "No. Las clases son para todos los niveles, también para quien nunca ha surfeado."))])


def uni():
    return landing("uni", L("Group surf trips · Universities", "Viajes de surf para grupos · Universidades"),
        L("Surf trips for <mark>universities</mark> &amp; Erasmus", "Viajes de surf para <mark>universidades</mark> y Erasmus"),
        L("For student associations, university sports services and Erasmus groups: a surf week in Sagres with accommodation, lessons and transport in one closed proposal.",
          "Para asociaciones de estudiantes, servicios de deportes universitarios y grupos Erasmus: una semana de surf en Sagres con alojamiento, clases y transporte en una propuesta cerrada."),
        "sagres-surf-lesson", L("Group surf lesson on the beach", "Clase de surf en grupo en la playa"),
        [(L("Built for student groups", "Pensado para grupos de estudiantes"),
          L("<p>Shared rooms, common areas and a pool: the formula that works for big student groups. One organiser talks to one contact.</p>",
            "<p>Habitaciones compartidas, zonas comunes y piscina: la fórmula que funciona para grupos grandes de estudiantes. Una persona organiza y habla con un único contacto.</p>")),
         (L("Mixed levels, no problem", "Niveles mezclados, sin problema"),
          L("<p>Beginners and surfers who already ride waves can travel together: lessons are organised by level.</p>",
            "<p>Principiantes y gente que ya coge olas pueden viajar juntos: las clases se organizan por niveles.</p>"))],
        lambda: [(L("How big can the group be?", "¿De cuántas personas puede ser el grupo?"), L("Group proposals start at 20 people. Tell us your approximate number and we check availability.", "Las propuestas de grupo son a partir de 20 personas. Dinos un número aproximado y comprobamos la disponibilidad.")),
                 (L("Can each student pay separately?", "¿Puede pagar cada estudiante por su cuenta?"), L("Payment terms are set out in the proposal. Tell us how your group prefers to pay when you enquire.", "Las condiciones de pago se detallan en la propuesta. Indícanos en la solicitud cómo prefiere pagar vuestro grupo.")),
                 (L("Are flights included?", "¿Están incluidos los vuelos?"), L("No. Flights and airport transfers are not part of the packages.", "No. Los vuelos y los traslados desde el aeropuerto no forman parte de los packs."))])


def team():
    return landing("team", L("Group surf trips · Companies", "Viajes de surf para grupos · Empresas"),
        L("Surf <mark>team building</mark> &amp; company retreats", "<mark>Team building</mark> de surf y retiros de empresa"),
        L("Surf as a shared challenge, yoga to reset and a space to work together. A company retreat in Sagres, quoted for your team.",
          "El surf como reto compartido, yoga para desconectar y un espacio para trabajar juntos. Un retiro de empresa en Sagres, presupuestado para vuestro equipo."),
        "sagres-house-yoga", L("Yoga session at the surf house", "Sesión de yoga en la surf house"),
        [(L("Work and surf", "Trabajo y surf"),
          L("<p>The surf house has a coworking space with a projector for sessions and meetings between surf lessons.</p>",
            "<p>La surf house tiene un espacio coworking con proyector para sesiones y reuniones entre clases de surf.</p>")),
         (L("A shared challenge", "Un reto compartido"),
          L("<p>Everyone starts from the same place on a surfboard. Lessons by level, yoga and time together outside the office.</p>",
            "<p>Sobre una tabla todo el mundo empieza desde el mismo sitio. Clases por niveles, yoga y tiempo juntos fuera de la oficina.</p>"))],
        lambda: [(L("Can we hold meetings there?", "¿Podemos hacer reuniones allí?"), L("Yes. There is a coworking space with a projector.", "Sí. Hay un espacio coworking con proyector.")),
                 (L("Do we need surf experience?", "¿Hace falta experiencia en surf?"), L("No. Lessons are organised by level, from complete beginners.", "No. Las clases se organizan por niveles, también para quien empieza de cero.")),
                 (L("How do you quote a company trip?", "¿Cómo presupuestáis un viaje de empresa?"), L("Send dates, number of people and what you need. You receive one closed proposal.", "Envíanos fechas, número de personas y lo que necesitáis. Recibís una propuesta cerrada."))])


def trips():
    return f'''
<section class="pad"><h1 class="kicker">{L("Surf trips and surf camp destinations", "Viajes de surf y destinos de surf camp")}</h1>
<p class="mega">{L("Where<br>we <mark>surf</mark>", "Dónde<br><mark>surfeamos</mark>")}</p>
<p class="lead">{L("Each destination is a surf camp or surf house we work with. Pick one and send one enquiry: you get one personalised proposal.", "Cada destino es un surf camp o surf house con el que trabajamos. Elige uno y envía una solicitud: recibes una propuesta personalizada.")}</p><a class="btn btn-orange" href="{url("match")}">{L("Not sure? Find your match", "¿Dudas? Encuentra tu destino")}</a></section>
<section class="pad dest">
<a class="dcard" href="{url("sagres")}">{pic("sagres-coast", L("Beach and cliffs near Sagres", "Playa y acantilados cerca de Sagres"), sizes="(max-width:860px) 100vw, 50vw")}<span class="kicker">Portugal · Algarve</span><span class="h2">Sagres</span><span>{L("Surf house with pool · 3, 5 and 7 nights →", "Surf house con piscina · 3, 5 y 7 noches →")}</span></a>
<a class="dcard" href="{url("bali")}">{pic("bali-pool-day", L("Swimming pool and thatched lounge in the garden of the surf and coworking hotel in Bali", "Piscina y zona lounge con techo de palma en el jardín del hotel de surf y coworking en Bali"), sizes="(max-width:860px) 100vw, 50vw")}<span class="kicker">Indonesia · Bali</span><span class="h2">Bali</span><span>{L("Surf &amp; coworking hotel · all year · up to 18 →", "Hotel de surf y coworking · todo el año · hasta 18 →")}</span></a>
<a class="dcard soon" href="{url("contact")}"><span class="kicker">{L("Coming soon", "Muy pronto")}</span><span class="h2">{L("New destinations", "Nuevos destinos")}</span><span>{L("We are adding new surf camps. Ask us where you would like to go →", "Estamos sumando nuevos surf camps. Dinos adónde te gustaría ir →")}</span></a>
</section>'''


def guide_page(key, h1, intro, sections, photo, alt):
    body = "".join(f"<h2>{h}</h2>{t}" for h, t in sections)
    mins = max(2, round(len(re.findall(r"\w+", re.sub("<[^>]+>", " ", intro + body))) / 200))
    related = "".join(f'<a href="{url(k)}">{PAGES[k][1 if LANG == "en" else 2].split(" | ")[0]} →</a>' for k in GUIDES if k != key)
    return f'''
<article>
<section class="pad guide-head"><p class="kicker">{L("Guide", "Guía")} · {mins} min {L("read", "de lectura")}</p><h1 class="big">{h1}</h1><p class="lead drop">{intro}</p></section>
{pic(photo, alt, "ph pano", True, "100vw")}
<section class="pad prose">{body}
<p><a class="btn btn-ink" href="{url("sagres", "#enquire")}">{L("Plan my surf trip", "Planear mi viaje de surf")}</a> <a class="btn" href="{url("groups")}">{L("Group proposal", "Propuesta de grupo")}</a></p>
<nav class="related" aria-label="{L("More guides", "Más guías")}">{related}</nav></section>
</article>'''


def g_group():
    return guide_page("g_group", L("How to organise a group surf trip, step by step", "Cómo organizar un viaje de surf en grupo, paso a paso"),
        L("Organising a surf trip for a school, a university association, a club or a company is simpler when you follow a clear order. These are the steps we follow with every group.",
          "Organizar un viaje de surf para un instituto, una asociación universitaria, un club o una empresa es más sencillo si sigues un orden claro. Estos son los pasos que seguimos con cada grupo."),
        [(L("1. Define the group", "1. Define el grupo"), L("<p>Approximate number of people, ages and surf level. An estimate is enough to start: for example «about 30, aged 18 to 24, mostly beginners».</p>", "<p>Número aproximado de personas, edades y nivel de surf. Para empezar basta una estimación: por ejemplo «unas 30 personas, de 18 a 24 años, casi todos principiantes».</p>")),
         (L("2. Choose the dates", "2. Elige las fechas"), L("<p>In Sagres, group trips run from March to July and from mid-September to December. Give two or three options if you can: it makes availability easier.</p>", "<p>En Sagres los viajes de grupo se hacen de marzo a julio y de mediados de septiembre a diciembre. Si puedes, da dos o tres opciones: facilita la disponibilidad.</p>")),
         (L("3. Pick the length", "3. Elige la duración"), L("<p>3, 5 or 7 nights. The 7-night format includes 5 days of surf with 2 sessions of 1 h 30 a day, equipment, transport, picnic and insurance.</p>", "<p>3, 5 o 7 noches. El formato de 7 noches incluye 5 días de surf con 2 sesiones de 1 h 30 al día, material, transporte, picnic y seguro.</p>")),
         (L("4. Check the rules for minors", "4. Revisa las normas para menores"), L("<p>School groups travel from age 16, organised by the school with accompanying teachers. Supervision and insurance are set out in the proposal.</p>", "<p>Los grupos escolares viajan desde los 16 años, organizados por el centro y con profesorado acompañante. La supervisión y el seguro se detallan en la propuesta.</p>")),
         (L("5. Ask for one closed proposal", "5. Pide una propuesta cerrada"), L("<p>Send what you know. We check availability and send a proposal with everything included and the final price. Flights are not part of the packages, so book them once dates are confirmed.</p>", "<p>Envía lo que sepas. Comprobamos la disponibilidad y te mandamos una propuesta con todo lo incluido y el precio final. Los vuelos no forman parte de los packs: resérvalos cuando las fechas estén confirmadas.</p>"))],
        "sagres-surf-group", L("Surf group on the beach", "Grupo de surf en la playa"))


def g_pack():
    return guide_page("g_pack", L("What to pack for a surf camp: the essential list", "Qué llevar a un surf camp: la lista esencial"),
        L("You do not need much for a surf trip, but forgetting a few things can spoil a day. This is the list we recommend.", "Para un viaje de surf no hace falta mucho, pero olvidar algunas cosas puede estropearte un día. Esta es la lista que recomendamos."),
        [(L("For the water", "Para el agua"), L("<ul><li>Swimsuit or bikini to wear under the wetsuit</li><li>High-protection, water-resistant sunscreen</li><li>Beach towel or poncho</li><li>Flip-flops</li></ul><p>Board and wetsuit: check what your package includes. On the 7-night surf package equipment is included.</p>", "<ul><li>Bañador o bikini para llevar bajo el neopreno</li><li>Protector solar alto y resistente al agua</li><li>Toalla de playa o poncho</li><li>Chanclas</li></ul><p>Tabla y neopreno: revisa qué incluye tu pack. En el pack de 7 noches el material está incluido.</p>")),
         (L("For the rest of the day", "Para el resto del día"), L("<ul><li>A warm layer or hoodie for the evenings by the sea</li><li>Comfortable clothes and trainers</li><li>Reusable water bottle</li><li>Cap and sunglasses</li></ul>", "<ul><li>Una capa de abrigo o sudadera para las tardes junto al mar</li><li>Ropa cómoda y zapatillas</li><li>Botella de agua reutilizable</li><li>Gorra y gafas de sol</li></ul>")),
         (L("Documents", "Documentación"), L("<ul><li>ID card or passport</li><li>European Health Insurance Card if you live in the EU</li><li>Travel insurance details, if you have it</li></ul>", "<ul><li>DNI o pasaporte</li><li>Tarjeta Sanitaria Europea si vives en la UE</li><li>Datos de tu seguro de viaje, si lo tienes</li></ul>")),
         (L("Leave at home", "Déjalo en casa"), L("<p>Valuables you will not use. You will spend most of the day on the beach.</p>", "<p>Objetos de valor que no vayas a usar. Pasarás casi todo el día en la playa.</p>"))],
        "sagres-surf-wave", L("Surfer riding a wave", "Surfista cogiendo una ola"))


def g_first():
    return guide_page("g_first", L("Your first surf trip: what to expect as a beginner", "Tu primer viaje de surf: qué esperar si eres principiante"),
        L("Never surfed before? Good: most people on a surf camp are beginners. This is what a first surf week usually looks like.", "¿Nunca has surfeado? Perfecto: en un surf camp la mayoría empieza de cero. Así suele ser una primera semana de surf."),
        [(L("First, on the sand", "Primero, en la arena"), L("<p>Lessons start on the beach: how to lie on the board, paddle and stand up. Then you try it in the white water close to shore.</p>", "<p>Las clases empiezan en la playa: cómo tumbarse en la tabla, remar y ponerse de pie. Después lo pruebas en la espuma, cerca de la orilla.</p>")),
         (L("Sessions of 1 h 30", "Sesiones de 1 h 30"), L("<p>On the 7-night package there are 2 sessions a day. Surfing is tiring: it is normal to feel your arms and shoulders the first days.</p>", "<p>En el pack de 7 noches hay 2 sesiones al día. El surf cansa: es normal notar brazos y hombros los primeros días.</p>")),
         (L("Safety first", "La seguridad, lo primero"), L("<p>You should be comfortable in the water. Always follow the instructor: they choose the spot and the conditions for your level.</p>", "<p>Tienes que sentirte cómodo en el agua. Sigue siempre las indicaciones del monitor: elige el spot y las condiciones según tu nivel.</p>")),
         (L("Progress at your pace", "Progresa a tu ritmo"), L("<p>Some people stand up on the first day, others later. What matters is enjoying the sea and the group.</p>", "<p>Hay quien se pone de pie el primer día y quien tarda más. Lo importante es disfrutar del mar y del grupo.</p>"))],
        "sagres-surf-lesson", L("Beginners in a surf lesson", "Principiantes en una clase de surf"))


def guides():
    items = "".join(f'<a class="dcard" href="{url(k)}">{pic(ph, "", sizes="(max-width:860px) 100vw, 33vw")}<span class="kicker">{L("Guide", "Guía")}</span><span class="h3">{PAGES[k][1 if LANG == "en" else 2].split(" | ")[0]}</span></a>'
                    for k, ph in (("g_group", "sagres-surf-group"), ("g_pack", "sagres-surf-wave"), ("g_first", "sagres-surf-lesson")))
    return f'''
<section class="pad"><h1 class="kicker">{L("Surf trip guides", "Guías de viajes de surf")}</h1><p class="mega">{L("Surf<br><mark>guides</mark>", "Guías<br>de <mark>surf</mark>")}</p>
<p class="lead">{L("Practical guides to plan a surf trip, alone, with friends or with a group.", "Guías prácticas para planear un viaje de surf, por tu cuenta, con amigos o en grupo.")}</p></section>
<section class="pad dest three-up">{items}</section>'''


def home_guides():
    items = "".join(f'<a href="{url(k)}"><span class="kicker">{L("Guide", "Guía")}</span><span class="h3">{PAGES[k][1 if LANG == "en" else 2].split(" | ")[0]}</span><span>{L("Read →", "Leer →")}</span></a>' for k in GUIDES)
    return f'<section class="pad"><div class="head"><h2 class="big">{L("Surf guides", "Guías de surf")}</h2><a class="kicker" href="{url("guides")}">{L("All guides →", "Todas las guías →")}</a></div></section><section class="three">{items}</section>'


def ig_block():
    ig = SOCIAL["instagram"]
    if not ig:
        return ""
    tiles = "".join(f'<a href="{ig}" target="_blank" rel="noopener" class="igt">{pic(p, "", sizes="(max-width:860px) 33vw, 16vw")}</a>' for p in ("bali-pool-day", "bali-terrace", "bali-pool-night", "bali-mirror-bedroom", "bali-coffee", "bali-kitchen-cowork"))
    return f'<section class="pad"><div class="head"><h2 class="big">{L("Follow the swell", "Síguenos")}</h2><a class="btn" href="{ig}" target="_blank" rel="noopener">{IG_HANDLE} · Instagram</a></div><div class="igrid">{tiles}</div></section>'


EXTRA_PAGES = {
    "trips": (trips, "Surf Trips & Surf Camp Destinations | SNAP SURF TRIPS", "Viajes de surf y destinos de surf camp | SNAP SURF TRIPS",
              "Surf camp destinations for travellers and groups: Sagres in Portugal and Bali in Indonesia, with new destinations coming.", "Destinos de surf camp para viajeros y grupos: Sagres (Portugal) y Bali (Indonesia), y pronto habrá más.", "Surf trips", "Viajes de surf"),
    "school": (school, "End-of-Year School Surf Trips (16+) | SNAP SURF TRIPS", "Viajes de fin de curso de surf (16+) | SNAP SURF TRIPS",
               "End-of-year surf trips to Sagres for school groups aged 16+, organised with the school. Closed proposal on request.", "Viajes de fin de curso de surf a Sagres para grupos escolares de 16+ años, organizados con el centro. Propuesta cerrada a medida.", "School trips", "Fin de curso"),
    "uni": (uni, "University & Erasmus Surf Trips | SNAP SURF TRIPS", "Viajes de surf para universidades y Erasmus | SNAP",
            "Surf trips to Sagres for student associations, university sports and Erasmus groups. Accommodation, lessons and transport.", "Viajes de surf a Sagres para asociaciones de estudiantes, deportes universitarios y grupos Erasmus. Alojamiento, clases y transporte.", "Universities & Erasmus", "Universidades y Erasmus"),
    "team": (team, "Surf Team Building & Company Retreats | SNAP SURF TRIPS", "Team building de surf y retiros de empresa | SNAP",
             "Surf team building and company retreats in Sagres, Portugal: surf lessons, yoga and a coworking space. Quoted for your team.", "Team building de surf y retiros de empresa en Sagres (Portugal): clases de surf, yoga y coworking. Presupuesto para tu equipo.", "Team building", "Team building"),
    "guides": (guides, "Surf Trip Guides | SNAP SURF TRIPS", "Guías de viajes de surf | SNAP SURF TRIPS",
               "Practical guides to plan a surf trip: group trips, packing list and first surf trip.", "Guías prácticas para planear un viaje de surf: viajes en grupo, qué llevar y primer viaje de surf.", "Guides", "Guías"),
    "g_group": (g_group, "How to Organise a Group Surf Trip, Step by Step | SNAP", "Cómo organizar un viaje de surf en grupo, paso a paso | SNAP",
                "The 5 steps to organise a surf trip for a school, university, club or company: group, dates, length, minors and proposal.", "Los 5 pasos para organizar un viaje de surf para un instituto, universidad, club o empresa: grupo, fechas, duración, menores y propuesta.", "Group surf trip", "Viaje de surf en grupo"),
    "g_pack": (g_pack, "What to Pack for a Surf Camp: Essential List | SNAP", "Qué llevar a un surf camp: la lista esencial | SNAP",
               "The essential packing list for a surf camp: for the water, for the rest of the day, documents and what to leave at home.", "La lista esencial para un surf camp: para el agua, para el resto del día, documentación y qué dejar en casa.", "Packing list", "Qué llevar"),
    "g_first": (g_first, "Your First Surf Trip: What to Expect | SNAP SURF TRIPS", "Tu primer viaje de surf: qué esperar | SNAP SURF TRIPS",
                "Never surfed? What a first surf week looks like: lessons on the sand, sessions of 1 h 30, safety and progress.", "¿Nunca has surfeado? Así es una primera semana de surf: clases en la arena, sesiones de 1 h 30, seguridad y progreso.", "First surf trip", "Primer viaje de surf"),
}


# ---------- Bali (camps/partner-bali · listing bali-bukit-01) ----------
# Sin nombre, sin Instagram y sin fotos del partner hasta tener permiso escrito (R-006 + ficha del CRM). Cartel gráfico propio.
EXTRA_PATHS["bali"] = ("surf-trips/bali/", "es/viajes-surf/bali/")
PARENT["bali"] = "trips"


def poster(word, sub, cls=""):
    return f'<div class="poster {cls}" role="img" aria-label="{word} · {sub}"><span class="sun"></span><span class="pw">{word}</span><span class="ps">{sub}</span></div>'


def bali():
    facts = L(["Swimming pool", "Breakfast included", "Coworking with fast wifi", "Spa &amp; massages", "Rooms with balcony or terrace"],
              ["Piscina", "Desayuno incluido", "Coworking con wifi rápido", "Spa y masajes", "Habitaciones con balcón o terraza"])
    return f'''
<section class="pad rule">
<p class="kicker">Indonesia · Bali · {L("Bukit peninsula", "Península de Bukit")}</p>
<h1 class="mega">{L("Surf trip<br>to <mark>Bali</mark>", "Viaje de surf<br>a <mark>Bali</mark>")}</h1>
<p class="lead">{L("A small boutique surf &amp; coworking hotel on the Bukit peninsula, in the Uluwatu area: surf in the morning, work or rest in the afternoon. Open all year, for travellers and small groups up to 18.",
                    "Un pequeño hotel boutique de surf y coworking en la península de Bukit, en la zona de Uluwatu: surf por la mañana, trabajo o descanso por la tarde. Abierto todo el año, para viajeros y grupos pequeños de hasta 18 personas.")}</p>
</section>
{pic("bali-pool-day", L("Swimming pool and thatched lounge in the garden of the surf and coworking hotel in Bali", "Piscina y zona lounge con techo de palma en el jardín del hotel de surf y coworking en Bali"), "ph pano rule", True, "100vw")}
<section class="split rule">
<div class="pad">
<p class="kicker">{L("The stay", "El alojamiento")}</p>
<h2 class="big">{L("Surf &amp; remote work", "Surf y trabajo en remoto")}</h2>
<p class="lead">{L("A boutique hotel with few rooms, personal service and a coworking space. The surf spots of the Uluwatu area, like Balangan, Padang Padang and Bingin, are a short drive away. Bali airport is about 30 minutes by car.",
                    "Un hotel boutique de pocas habitaciones, trato cercano y espacio coworking. Los spots de la zona de Uluwatu, como Balangan, Padang Padang y Bingin, están a pocos minutos en coche. El aeropuerto de Bali queda a unos 30 minutos.")}</p>
<ul class="facts">{"".join(f"<li>{x}</li>" for x in facts)}</ul>
<a class="btn btn-orange" href="#enquire">{L("Get my proposal", "Pedir mi propuesta")}</a>
</div>
{pic("bali-cowork-lounge", L("Shared work and lounge area with wooden tables and woven lamps", "Zona común de trabajo y descanso con mesas de madera y lámparas de fibra"), "ph tall bl")}
</section>
<section class="gallery rule" aria-label="{L("Photos", "Fotos")}">
{pic("bali-terrace", L("Room terrace with sofa and sliding doors to the bedroom", "Terraza de la habitación con sofá y puertas correderas al dormitorio"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("bali-bedroom-garden", L("Bedroom opening onto the garden", "Dormitorio abierto al jardín"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("bali-kitchen-cowork", L("Kitchen and work table with fresh fruit", "Cocina y mesa de trabajo con fruta fresca"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("bali-pool-night", L("Swimming pool lit up at night", "Piscina iluminada por la noche"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("bali-mirror-bedroom", L("Bedroom with a large wooden mirror and woven lamp", "Dormitorio con gran espejo de madera y lámpara de fibra"), sizes="(max-width:860px) 50vw, 33vw")}
{pic("bali-coffee", L("Fresh ground coffee", "Café recién molido"), sizes="(max-width:860px) 50vw, 33vw")}
</section>
{cards([
  (L("Who it is for", "Para quién"), L("<p>Surfers who want to combine waves and remote work, friends and small groups of up to 18 people. Adults only.</p>", "<p>Surfistas que quieren combinar olas y trabajo en remoto, amigos y grupos pequeños de hasta 18 personas. Solo adultos.</p>")),
  (L("When to go", "Cuándo ir"), L("<p>Open all year. Tell us your dates and we check availability.</p>", "<p>Abierto todo el año. Dinos tus fechas y comprobamos la disponibilidad.</p>")),
  (L("Surfing", "El surf"), L("<p>Tell us your level. Surf options for your trip are confirmed in your personalised proposal.</p>", "<p>Cuéntanos tu nivel. Las opciones de surf de tu viaje se confirman en tu propuesta personalizada.</p>")),
  (L("How it works", "Cómo funciona"), L("<p>One enquiry, one proposal with the final price. Flights and airport transfers are not included unless the proposal says so.</p>", "<p>Una solicitud, una propuesta con el precio final. Los vuelos y los traslados no están incluidos salvo que la propuesta lo indique.</p>"))])}
<section class="split rule" id="enquire">
<div class="pad dark"><p class="kicker orange-t">{L("Enquire", "Solicitud")}</p><h2 class="big">{L("Tell us about your trip", "Cuéntanos tu viaje")}</h2><p class="lead">{L("No payment now. We check availability and come back with your proposal.", "Sin pagar nada ahora. Comprobamos la disponibilidad y te enviamos tu propuesta.")}</p>{mini()}</div>
<div class="pad bl">{form("individual", f_ind().replace('max="19"', 'max="18"').replace('<option>3</option><option>5</option><option>7</option>', '<option>5</option><option>7</option><option>10</option><option>14</option>'), L("Send my enquiry", "Enviar mi solicitud"), '<input type="hidden" name="listingId" value="bali-bukit-01"><input type="hidden" name="destination" value="Bali">')}</div>
</section>'''


def home_more():
    return f'''<div class="dest">
<a class="dcard" href="{url("bali")}">{pic("bali-pool-day", L("Swimming pool and thatched lounge in the garden of the surf and coworking hotel in Bali", "Piscina y zona lounge con techo de palma en el jardín del hotel de surf y coworking en Bali"), sizes="(max-width:860px) 100vw, 50vw")}<span class="kicker">Indonesia · Bali</span><span class="h3">{L("Surf &amp; coworking hotel · all year", "Hotel de surf y coworking · todo el año")}</span></a>
<a class="dcard soon" href="{url("contact")}"><span class="kicker">{L("Coming soon", "Muy pronto")}</span><span class="h3">{L("More destinations", "Más destinos")}</span><span>{L("Tell us where you would like to surf →", "Dinos dónde te gustaría surfear →")}</span></a>
</div>'''


EXTRA_PAGES["bali"] = (bali, "Surf Trip to Bali: Surf & Coworking Hotel | SNAP", "Viaje de surf a Bali: hotel de surf y coworking | SNAP",
    "Surf trip to Bali: boutique surf and coworking hotel in the Uluwatu area, open all year, for travellers and small groups up to 18.",
    "Viaje de surf a Bali: hotel boutique de surf y coworking en la zona de Uluwatu, abierto todo el año, para viajeros y grupos de hasta 18.", "Bali", "Bali")


# ---------- compartir (sin scripts de terceros) y cartel OG ----------
SHARE = {"sagres", "bali", "school", "uni", "team", *GUIDES}


def share(key, title):
    from urllib.parse import quote
    u = DOMAIN + "/" + path(key)
    q, qt = quote(u, safe=""), quote(title + " " + u, safe="")
    return f'''<section class="pad share" aria-label="{L("Share", "Compartir")}"><p class="kicker">{L("Share this trip with your crew", "Comparte este viaje con tu grupo")}</p>
<div class="row"><a class="btn sm" href="https://wa.me/?text={qt}" rel="noopener">WhatsApp</a><a class="btn sm" href="https://www.linkedin.com/sharing/share-offsite/?url={q}" rel="noopener">LinkedIn</a><a class="btn sm" href="https://twitter.com/intent/tweet?url={q}&amp;text={quote(title, safe="")}" rel="noopener">X</a><button class="btn sm" type="button" data-copy="{u}">{L("Copy link", "Copiar enlace")}</button></div></section>'''


def og_poster(dest, word, sub):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (1200, 630)); d = ImageDraw.Draw(im)
    for y in range(630):
        k = y / 630; d.line([(0, y), (1200, y)], fill=(int(14 + 8 * k), int(42 + 30 * k), int(58 + 34 * k)))
    d.ellipse((760, 70, 1100, 410), fill=(255, 90, 31))
    f = SRC / "anton.ttf"
    big = ImageFont.truetype(str(f), 260) if f.exists() else ImageFont.load_default()
    small = ImageFont.truetype(str(f), 40) if f.exists() else ImageFont.load_default()
    d.text((70, 250), word, font=big, fill=(244, 241, 234)); d.text((76, 548), sub, font=small, fill=(244, 241, 234))
    im.save(dest, quality=85)


# ---------- Buscador de surf trip (matcher) ----------
# Reglas = datos de camps/{id} del CRM (16/11). Sin «IA» de cara al cliente: puntuación transparente con motivos.
# Las respuestas viajan en la solicitud (inbound.data.matcher) y alimentan el scoring/campFit del CRM (M_WEB).
EXTRA_PATHS["match"] = ("surf-trip-matcher/", "es/encuentra-tu-surf-trip/")
MATCH_DATA = {
    "sagres": {"listing": "sagres-surf-house-01", "max": 100, "minors": True, "months": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
               "groupClosed": [1, 2, 8], "lessons": True,
               "vibe": {"learn": 25, "progress": 15, "work": 10, "social": 20, "nature": 20}},
    "bali": {"listing": "bali-bukit-01", "max": 18, "minors": False, "months": list(range(1, 13)), "groupClosed": [], "lessons": False,
             "vibe": {"learn": 5, "progress": 15, "work": 30, "social": 15, "nature": 15}},
}


def q(name, label, opts):
    o = "".join(f'<label class="pill"><input type="radio" name="{name}" value="{v}" required><span>{t}</span></label>' for v, t in opts)
    return f'<fieldset class="mq"><legend class="h3">{label}</legend><div class="pills">{o}</div></fieldset>'


def match():
    months = L(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"])
    data = {"d": MATCH_DATA, "u": {k: url(k) for k in ("sagres", "bali", "groups", "contact")}, "lang": LANG,
            "t": {"sagres": "Sagres · Portugal", "bali": "Bali · Indonesia",
                  "why": L("Why", "Por qué"), "alt": L("Also a good fit", "También encaja"), "none": L("No destination fits those answers yet. Tell us what you need and we look for it.", "Todavía no hay un destino que encaje con esas respuestas. Cuéntanos qué buscas y lo buscamos."),
                  "r": {"size": L("Fits your group size", "Encaja con el tamaño de vuestro grupo"), "month": L("Open in the month you chose", "Abierto en el mes que has elegido"),
                        "lessons": L("Surf school on site: perfect to start", "Escuela de surf propia: ideal para empezar"), "work": L("Coworking to combine surf and work", "Coworking para combinar surf y trabajo"),
                        "minors": L("Accepts school groups from 16", "Acepta grupos escolares desde 16 años"), "vibe": L("Matches the trip you are looking for", "Encaja con el viaje que buscas"),
                        "big": L("Too many people for this place", "Demasiadas personas para este alojamiento"), "closed": L("Closed for groups that month", "Cerrado para grupos ese mes"), "noMinors": L("Adults only", "Solo adultos")}}}
    import json as _json
    return f'''
<section class="pad"><h1 class="kicker">{L("Surf trip matcher", "Buscador de surf trip")}</h1>
<p class="mega">{L("Find your<br><mark>surf trip</mark>", "Encuentra tu<br><mark>surf trip</mark>")}</p>
<p class="lead">{L("Five questions, thirty seconds. We match your answers with the surf camps we work with and tell you why.", "Cinco preguntas, treinta segundos. Cruzamos tus respuestas con los surf camps con los que trabajamos y te decimos por qué.")}</p></section>
<section class="pad"><form id="matcher" class="matcher" novalidate>
{q("who", L("Who is travelling?", "¿Quién viaja?"), L([("solo", "Just me"), ("friends", "Friends or couple"), ("students", "University / Erasmus"), ("school", "School group (16+)"), ("company", "Company / team"), ("club", "Club / association")], [("solo", "Solo yo"), ("friends", "Amigos o pareja"), ("students", "Universidad / Erasmus"), ("school", "Grupo escolar (16+)"), ("company", "Empresa / equipo"), ("club", "Club / asociación")]))}
{q("size", L("How many people?", "¿Cuántas personas?"), [("1", "1"), ("4", "2–6"), ("12", "7–18"), ("25", "19–30"), ("50", "31–60"), ("80", "60+")])}
{q("month", L("When?", "¿Cuándo?"), [(str(i + 1), m) for i, m in enumerate(months)] + [("0", L("Flexible", "Flexible"))])}
{q("level", L("Surf level", "Nivel de surf"), L([("never", "Never surfed"), ("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced"), ("mixed", "Mixed")], [("never", "Nunca"), ("beginner", "Principiante"), ("intermediate", "Intermedio"), ("advanced", "Avanzado"), ("mixed", "Mezclado")]))}
{q("vibe", L("What do you want most?", "¿Qué buscas sobre todo?"), L([("learn", "Learn to surf"), ("progress", "Progress"), ("work", "Surf + remote work"), ("social", "Good vibes with the group"), ("nature", "Nature and calm")], [("learn", "Aprender a surfear"), ("progress", "Progresar"), ("work", "Surf + trabajo en remoto"), ("social", "Buen rollo en grupo"), ("nature", "Naturaleza y calma")]))}
<button class="btn btn-orange" type="submit">{L("See my match", "Ver mi destino")}</button>
</form>
<div id="mres" class="mres" hidden aria-live="polite"></div>
<script type="application/json" id="mdata">{_json.dumps(data, ensure_ascii=False)}</script>
</section>
<section class="split rule" id="enquire" hidden>
<div class="pad dark"><p class="kicker orange-t">{L("Your proposal", "Tu propuesta")}</p><h2 class="big">{L("Want this trip?", "¿Quieres este viaje?")}</h2><p class="lead">{L("Leave your details: we already have your answers. No payment now.", "Déjanos tus datos: ya tenemos tus respuestas. Sin pagar nada ahora.")}</p>{mini()}</div>
<div class="pad bl">{form("individual", f_gen(), L("Request my proposal", "Pedir mi propuesta"), '<input type="hidden" name="listingId" value=""><input type="hidden" name="people" value=""><input type="hidden" name="dates" value=""><input type="hidden" name="level" value=""><input type="hidden" name="groupType" value="">')}</div>
</section>'''


def match_cta():
    return f'<section class="pad mcta"><p class="kicker">{L("Not sure where to go?", "¿No sabes adónde ir?")}</p><h2 class="big">{L("Find your surf trip<br>in <mark>30 seconds</mark>", "Encuentra tu surf trip<br>en <mark>30 segundos</mark>")}</h2><a class="btn btn-ink" href="{url("match")}">{L("Start the matcher", "Empezar")}</a></section>'


EXTRA_PAGES["match"] = (match, "Surf Trip Matcher: find your surf trip in 30 seconds | SNAP", "Encuentra tu surf trip en 30 segundos | SNAP SURF TRIPS",
    "Answer five questions and find the surf camp that fits you or your group: destination, dates, size and surf level.",
    "Responde cinco preguntas y encuentra el surf camp que encaja contigo o con tu grupo: destino, fechas, tamaño y nivel de surf.", "Surf trip matcher", "Encuentra tu surf trip")
SHARE.add("match")
