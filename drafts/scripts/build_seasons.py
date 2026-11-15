"""Build the four seasonal story pages and the mushroom story (EN and FR) from verified GBIF figures.

Usage: python build_seasons.py SEASON_GBIF_JSON DOCS_DIR
"""
import json, sys

G = json.load(open(sys.argv[1]))
DOCS = sys.argv[2]
MONTHS = {"spring": [3, 4, 5], "summer": [6, 7, 8], "autumn": [9, 10, 11], "winter": [12, 1, 2]}
MLAB = {"en": {"spring": "March to May", "summer": "June to August", "autumn": "September to November", "winter": "December to February"},
        "fr": {"spring": "de mars à mai", "summer": "de juin à août", "autumn": "de septembre à novembre", "winter": "de décembre à février"}}


def num(x, lang):
    s = format(x, ",")
    return s.replace(",", " ") if lang == "fr" else s


def season_fig(sp, season, lang):
    g = G[sp]
    tot = g["n77"]; m = g["months"]
    k = sum(int(m.get(str(x), m.get(x, 0))) for x in MONTHS[season])
    pct = round(k / tot * 100) if tot else 0
    if lang == "en":
        return f"GBIF holds {num(tot,'en')} records of it in Seine-et-Marne since 2000; {num(k,'en')} of them ({pct} %) were made from {MLAB['en'][season]}."
    return f"Le GBIF en compte {num(tot,'fr')} observations en Seine-et-Marne depuis 2000, dont {num(k,'fr')} ({pct} %) {MLAB['fr'][season]}."


def img(slug, alt):
    return f"![{alt}](../img/species/{slug}.jpg){{ width=\"320\" }}"

# Each post: key, theme, species (Latin, for GBIF), slug, names, hook, p1, p2, status, tag
SEASONS = {
 "spring": {
  "date": {"en": "from the spring equinox, Saturday 20 March 2027", "fr": "à partir de l'équinoxe de printemps, samedi 20 mars 2027"},
  "title": {"en": "Spring in the wetlands of Seine-et-Marne", "fr": "Le printemps dans les zones humides de Seine-et-Marne"},
  "intro": {"en": "Six posts for March to May: the first flowers, the migrants back from Africa, the damselflies, the toads on the move, a spring fungus and the flooded meadows where pike spawn.",
            "fr": "Six posts pour mars à mai : les premières fleurs, les migrateurs revenus d'Afrique, les demoiselles, les crapauds en route, un champignon de printemps et les prés inondés où fraie le brochet."},
  "posts": [
   ("plant", "Caltha palustris", "caltha-palustris",
    {"en": "Marsh marigold, populage des marais", "fr": "Populage des marais, souci d'eau"},
    {"en": "🌼💧 Which flower opens first in a wet meadow?", "fr": "🌼💧 Quelle fleur s'ouvre la première dans un pré humide ?"},
    {"en": "The populage des marais, marsh marigold (Caltha palustris), opens large, glossy yellow cups along ditches and in alder woods in March and April, before most of the meadow has woken up.",
     "fr": "Le populage des marais (Caltha palustris), ou souci d'eau, ouvre de grandes coupes jaunes et brillantes le long des fossés et dans les aulnaies en mars et avril, avant que le reste du pré ne se réveille."},
    {"en": "It needs soil that stays wet in spring, so it is a good sign of an intact wet meadow. Like many buttercups, it is poisonous when fresh, to people and to livestock.",
     "fr": "Il lui faut un sol qui reste mouillé au printemps : c'est un bon signe d'un pré humide intact. Comme beaucoup de renoncules, il est toxique frais, pour l'homme comme pour le bétail."},
    {"en": "Least Concern (IUCN).", "fr": "Préoccupation mineure (UICN)."}, "#MarshMarigold #CalthaPalustris"),
   ("bird", "Acrocephalus scirpaceus", "acrocephalus-scirpaceus",
    {"en": "Reed warbler, rousserolle effarvatte", "fr": "Rousserolle effarvatte"},
    {"en": "🐦🌾 Who is singing inside the reeds in April?", "fr": "🐦🌾 Qui chante au cœur des roseaux en avril ?"},
    {"en": "The rousserolle effarvatte, reed warbler (Acrocephalus scirpaceus), spends the winter in Africa south of the Sahara and comes back to the reedbeds in April. It is heard far more than seen: a steady, chattering song from deep in the reeds.",
     "fr": "La rousserolle effarvatte (Acrocephalus scirpaceus) passe l'hiver en Afrique au sud du Sahara et revient dans les roselières en avril. On l'entend bien plus qu'on ne la voit : un chant régulier et bavard, du fond des roseaux."},
    {"en": "It weaves its nest around three or four reed stems above the water, which is why a reedbed must stay standing and wet in spring. It is a frequent host of the cuckoo.",
     "fr": "Elle tisse son nid autour de trois ou quatre tiges de roseau au-dessus de l'eau : une roselière doit donc rester debout et en eau au printemps. C'est un hôte fréquent du coucou."},
    {"en": "Least Concern (IUCN); protected in France.", "fr": "Préoccupation mineure (UICN) ; protégée en France."}, "#ReedWarbler #Birds #Migration"),
   ("insect", "Coenagrion puella", "coenagrion-puella",
    {"en": "Azure damselfly, agrion jouvencelle", "fr": "Agrion jouvencelle"},
    {"en": "💙🪷 What are the small blue needles over the pond in May?", "fr": "💙🪷 Quelles sont ces petites aiguilles bleues au-dessus de la mare en mai ?"},
    {"en": "The agrion jouvencelle, azure damselfly (Coenagrion puella), is one of the first damselflies of the year, blue and black, with a small U-shaped mark at the base of the male's abdomen.",
     "fr": "L'agrion jouvencelle (Coenagrion puella) est l'une des premières demoiselles de l'année, bleue et noire, avec une petite marque en U à la base de l'abdomen du mâle."},
    {"en": "Its larvae have spent the winter in the pond; in spring they climb a stem and the adults emerge. Common, but only where ponds keep water plants.",
     "fr": "Ses larves ont passé l'hiver dans la mare ; au printemps, elles grimpent sur une tige et les adultes émergent. Commune, mais seulement là où les mares gardent leurs plantes aquatiques."},
    {"en": "Least Concern (IUCN); not protected.", "fr": "Préoccupation mineure (UICN) ; non protégée."}, "#Damselflies #Odonata"),
   ("animal", "Bufo bufo", "bufo-bufo",
    {"en": "Common toad, crapaud commun", "fr": "Crapaud commun"},
    {"en": "🐸🌧️ Why do toads cross the road on rainy March nights?", "fr": "🐸🌧️ Pourquoi les crapauds traversent-ils la route les soirs de pluie de mars ?"},
    {"en": "On the first mild, rainy nights of the year, the crapaud commun, common toad (Bufo bufo), leaves its winter shelter in the woods and walks back to the pond where it was born, sometimes more than a kilometre away.",
     "fr": "Dès les premières nuits douces et pluvieuses de l'année, le crapaud commun (Bufo bufo) quitte son abri d'hiver dans les bois et retourne à la mare où il est né, parfois à plus d'un kilomètre."},
    {"en": "Roads cut that path, and every spring volunteers set up toad crossings, fences and buckets to carry them over. A pond is only as good as the woods and the paths around it.",
     "fr": "Les routes coupent ce chemin, et chaque printemps des bénévoles installent des crapauducs, des filets et des seaux pour leur faire traverser. Une mare ne vaut que par les bois et les chemins qui l'entourent."},
    {"en": "Least Concern (IUCN); protected in France.", "fr": "Préoccupation mineure (UICN) ; protégé en France."}, "#Toads #Amphibians #ToadCrossing"),
   ("fungus", "Cerioporus squamosus", "cerioporus-squamosus",
    {"en": "Dryad's saddle, polypore écailleux", "fr": "Polypore écailleux"},
    {"en": "🍄🌳 Which mushroom grows on willows in spring?", "fr": "🍄🌳 Quel champignon pousse sur les saules au printemps ?"},
    {"en": "The polypore écailleux, dryad's saddle (Cerioporus squamosus), forms large brown brackets with darker scales on willows, ash and elms in the valleys, from April. It smells of watermelon rind.",
     "fr": "Le polypore écailleux (Cerioporus squamosus) forme de grandes consoles brunes couvertes d'écailles sombres sur les saules, frênes et ormes des vallées, dès avril. Il sent l'écorce de pastèque."},
    {"en": "It rots the wood of old and dying trees and opens cavities for birds and insects. Edible only when very young and well cooked; for recognition only, never eat a mushroom without a check by a pharmacist or a mycologist.",
     "fr": "Il décompose le bois des arbres vieux ou mourants et ouvre des cavités pour les oiseaux et les insectes. Comestible seulement très jeune et bien cuit ; pour la reconnaissance seulement, ne mangez jamais un champignon sans l'avis d'un pharmacien ou d'un mycologue."},
    {"en": "Edible when young, well cooked. Not evaluated (IUCN).", "fr": "Comestible jeune, bien cuit. Non évalué (UICN)."}, "#Fungi #Mushrooms #DryadsSaddle"),
   ("ecosystem", "Esox lucius", "esox-lucius",
    {"en": "The flooded meadow, with the pike", "fr": "Le pré inondé, avec le brochet"},
    {"en": "🐟🌊 Why does a fish need a meadow?", "fr": "🐟🌊 Pourquoi un poisson a-t-il besoin d'un pré ?"},
    {"en": "At the end of winter and in early spring, the brochet, pike (Esox lucius), leaves the river for flooded grassland and shallow marshes to spawn among drowned grass. Its young grow in warm, shallow water that only a floodplain gives.",
     "fr": "À la fin de l'hiver et au début du printemps, le brochet (Esox lucius) quitte la rivière pour les prairies inondées et les marais peu profonds, et fraie dans l'herbe noyée. Ses alevins grandissent dans une eau chaude et peu profonde que seule une plaine d'inondation offre."},
    {"en": "So the toads, the marsh marigold and the pike all depend on the same thing in spring: meadows that are allowed to flood. In the catchments that drain Seine-et-Marne, confirmed and probable wetlands cover 27.8 % of the Île-de-France part, much of it in the floodplains of the Bassée and the Marne.",
     "fr": "Le crapaud, le populage et le brochet dépendent donc de la même chose au printemps : des prés qu'on laisse inonder. Dans les bassins versants qui drainent la Seine-et-Marne, zones humides avérées et probables couvrent 27,8 % de la partie francilienne, en bonne part dans les plaines d'inondation de la Bassée et de la Marne."},
    {"en": "Pike: Least Concern (IUCN).", "fr": "Brochet : préoccupation mineure (UICN)."}, "#Floodplain #Pike #Ecosystems"),
  ]},
 "summer": {
  "date": {"en": "from the summer solstice, Monday 21 June 2027", "fr": "à partir du solstice d'été, lundi 21 juin 2027"},
  "title": {"en": "Summer in the wetlands of Seine-et-Marne", "fr": "L'été dans les zones humides de Seine-et-Marne"},
  "intro": {"en": "Six posts for June to August: purple loosestrife in flower, the kingfisher, the banded demoiselle, a water snake, a milkcap of wet hollows and the low water of August.",
            "fr": "Six posts pour juin à août : la salicaire en fleur, le martin-pêcheur, le caloptéryx, une couleuvre nageuse, un lactaire des creux humides et l'étiage d'août."},
  "posts": [
   ("plant", "Lythrum salicaria", "lythrum-salicaria",
    {"en": "Purple loosestrife, salicaire", "fr": "Salicaire"},
    {"en": "💜🐝 What turns the riverbanks purple in July?", "fr": "💜🐝 Qu'est-ce qui colore les berges de violet en juillet ?"},
    {"en": "The salicaire, purple loosestrife (Lythrum salicaria), raises tall purple spikes along banks and ditches from July, in the same tall-herb fringe as meadowsweet.",
     "fr": "La salicaire (Lythrum salicaria) dresse de hauts épis violets le long des berges et des fossés dès juillet, dans la même frange de hautes herbes que la reine-des-prés."},
    {"en": "Bees, hoverflies and butterflies visit it all summer. Native here, it became one of the best-known invasive plants of North American wetlands after it was introduced there.",
     "fr": "Abeilles, syrphes et papillons la visitent tout l'été. Indigène ici, elle est devenue l'une des plantes envahissantes les plus connues des zones humides d'Amérique du Nord après y avoir été introduite."},
    {"en": "Least Concern (IUCN).", "fr": "Préoccupation mineure (UICN)."}, "#PurpleLoosestrife #Pollinators"),
   ("bird", "Alcedo atthis", "alcedo-atthis",
    {"en": "Kingfisher, martin-pêcheur", "fr": "Martin-pêcheur d'Europe"},
    {"en": "💙🐟 What was that blue flash over the river?", "fr": "💙🐟 Quel est cet éclair bleu au-dessus de la rivière ?"},
    {"en": "The martin-pêcheur, kingfisher (Alcedo atthis), flies low and fast along the water with a sharp call, and dives from a branch for small fish.",
     "fr": "Le martin-pêcheur (Alcedo atthis) file au ras de l'eau avec un cri aigu et plonge d'une branche sur les petits poissons."},
    {"en": "It needs clear water to see its prey and vertical earth banks to dig its nesting burrow. Stabilised, concreted banks and cloudy water are where it disappears.",
     "fr": "Il lui faut une eau claire pour voir ses proies et des berges de terre verticales pour creuser son terrier. Berges bétonnées et eau trouble : c'est là qu'il disparaît."},
    {"en": "Least Concern (IUCN); protected in France; Annex I of the EU Birds Directive.", "fr": "Préoccupation mineure (UICN) ; protégé en France ; annexe I de la directive Oiseaux."}, "#Kingfisher #Birds #Rivers"),
   ("insect", "Calopteryx splendens", "calopteryx-splendens",
    {"en": "Banded demoiselle, caloptéryx éclatant", "fr": "Caloptéryx éclatant"},
    {"en": "🦋💎 Is it a butterfly or a dragonfly?", "fr": "🦋💎 Papillon ou libellule ?"},
    {"en": "The caloptéryx éclatant, banded demoiselle (Calopteryx splendens), flutters like a butterfly over slow rivers; the male is metallic blue with a dark band across each wing.",
     "fr": "Le caloptéryx éclatant (Calopteryx splendens) volette comme un papillon au-dessus des rivières lentes ; le mâle est bleu métallique, avec une bande sombre sur chaque aile."},
    {"en": "Its larvae live among the water plants of flowing rivers, so it is a good sign of a living riverbank.",
     "fr": "Ses larves vivent dans les herbiers des eaux courantes : c'est un bon signe d'une berge vivante."},
    {"en": "Least Concern (IUCN); not protected.", "fr": "Préoccupation mineure (UICN) ; non protégé."}, "#Damselflies #Odonata #Rivers"),
   ("animal", "Natrix helvetica", "natrix-helvetica",
    {"en": "Barred grass snake, couleuvre helvétique", "fr": "Couleuvre helvétique"},
    {"en": "🐍💧 Why is there a snake swimming in the pond?", "fr": "🐍💧 Pourquoi un serpent nage-t-il dans la mare ?"},
    {"en": "The couleuvre helvétique, barred grass snake (Natrix helvetica), swims well and hunts frogs, toads and small fish in ponds and ditches in summer.",
     "fr": "La couleuvre helvétique (Natrix helvetica) nage très bien et chasse grenouilles, crapauds et petits poissons dans les mares et les fossés en été."},
    {"en": "It is harmless to people; when threatened it may play dead. It depends on the same ponds as the amphibians it eats.",
     "fr": "Elle est inoffensive pour l'homme ; menacée, elle peut faire la morte. Elle dépend des mêmes mares que les amphibiens qu'elle mange."},
    {"en": "Least Concern (IUCN); protected in France.", "fr": "Préoccupation mineure (UICN) ; protégée en France."}, "#Snakes #Reptiles"),
   ("fungus", "Lactarius lacunarum", "lactarius-lacunarum",
    {"en": "Puddle milkcap, lactaire des flaques", "fr": "Lactaire des flaques"},
    {"en": "🍄💦 Which mushroom grows where puddles dry out?", "fr": "🍄💦 Quel champignon pousse là où sèchent les flaques ?"},
    {"en": "The lactaire des flaques, puddle milkcap (Lactarius lacunarum), is a small orange milkcap of wet hollows, pond edges and ruts under willows and alders. Its Latin name means \"of the puddles\".",
     "fr": "Le lactaire des flaques (Lactarius lacunarum) est un petit lactaire orangé des creux humides, des bords de mares et des ornières, sous les saules et les aulnes. Son nom latin signifie « des flaques »."},
    {"en": "It lives in partnership with the roots of these trees, a mycorrhiza. Not edible.",
     "fr": "Il vit en association avec les racines de ces arbres, une mycorhize. Non comestible."},
    {"en": "Not edible. Not evaluated (IUCN).", "fr": "Non comestible. Non évalué (UICN)."}, "#Fungi #Mushrooms #Mycorrhiza"),
   ("ecosystem", "Lythrum salicaria", "filipendula-ulmaria",
    {"en": "Low water in August", "fr": "L'étiage d'août"},
    {"en": "🌞💧 Where does a river get its water in August?", "fr": "🌞💧 D'où une rivière tire-t-elle son eau en août ?"},
    {"en": "In late summer, rain is scarce and the rivers of Seine-et-Marne reach their lowest flow. Ponds shrink, warm up and lose oxygen; damselfly larvae and frogs crowd into what is left.",
     "fr": "À la fin de l'été, la pluie se fait rare et les rivières de Seine-et-Marne atteignent leur débit le plus bas. Les mares rétrécissent, se réchauffent et perdent leur oxygène ; larves et grenouilles se serrent dans ce qui reste."},
    {"en": "This is when wetlands earn their keep: the wet soils and meadows that filled in winter give their water back slowly to the rivers. In the catchments draining the département, confirmed and probable wetlands cover 27.8 % of the Île-de-France part.",
     "fr": "C'est là que les zones humides font leur travail : les sols et les prés gorgés d'eau en hiver la rendent lentement aux rivières. Dans les bassins qui drainent le département, zones humides avérées et probables couvrent 27,8 % de la partie francilienne."},
    {"en": "", "fr": ""}, "#LowFlow #Drought #Ecosystems"),
  ]},
 "autumn": {
  "date": {"en": "from the autumn equinox, Thursday 23 September 2027", "fr": "à partir de l'équinoxe d'automne, jeudi 23 septembre 2027"},
  "title": {"en": "Autumn in the wetlands of Seine-et-Marne", "fr": "L'automne dans les zones humides de Seine-et-Marne"},
  "intro": {"en": "Six posts for September to November: alder seeds on the water, the snipe on passage, the last red dragonflies, the harvest mouse, a mushroom with a deadly look-alike, and the leaves that feed the streams.",
            "fr": "Six posts pour septembre à novembre : les graines d'aulne au fil de l'eau, la bécassine de passage, les dernières libellules rouges, le rat des moissons, un champignon au sosie mortel, et les feuilles qui nourrissent les ruisseaux."},
  "posts": [
   ("plant", "Alnus glutinosa", "alnus-glutinosa",
    {"en": "Alder, aulne glutineux", "fr": "Aulne glutineux"},
    {"en": "🌳🍂 How does a tree travel by river?", "fr": "🌳🍂 Comment un arbre voyage-t-il par la rivière ?"},
    {"en": "In autumn the small woody cones of the aulne glutineux, alder (Alnus glutinosa), open and let out seeds with tiny air-filled wings that float. The river carries them downstream to new banks.",
     "fr": "En automne, les petits cônes ligneux de l'aulne glutineux (Alnus glutinosa) s'ouvrent et libèrent des graines munies de petites ailes pleines d'air, qui flottent. La rivière les emporte vers de nouvelles berges."},
    {"en": "Its roots hold the banks and carry nodules with bacteria that fix nitrogen from the air. Alder and ash woods along rivers are a priority EU habitat, 91E0*.",
     "fr": "Ses racines tiennent les berges et portent des nodules à bactéries qui fixent l'azote de l'air. Les aulnaies-frênaies des rivières sont un habitat prioritaire de l'UE, 91E0*."},
    {"en": "Least Concern (IUCN).", "fr": "Préoccupation mineure (UICN)."}, "#Alder #Trees #Riverbanks"),
   ("bird", "Gallinago gallinago", "gallinago-gallinago",
    {"en": "Common snipe, bécassine des marais", "fr": "Bécassine des marais"},
    {"en": "🐦🍂 Which bird probes the mud with a bill as long as its head?", "fr": "🐦🍂 Quel oiseau sonde la vase avec un bec aussi long que la tête ?"},
    {"en": "In autumn the bécassine des marais, common snipe (Gallinago gallinago), arrives from the north and east and feeds in muddy meadows and pond edges, probing for worms and larvae. Flushed, it rises in a fast zigzag.",
     "fr": "En automne, la bécassine des marais (Gallinago gallinago) arrive du nord et de l'est et se nourrit dans les prés boueux et au bord des mares, en sondant la vase à la recherche de vers et de larves. Levée, elle s'envole en zigzag rapide."},
    {"en": "It needs soft, wet ground that has not been drained. In France it is a game species, which makes the state of its wet meadows all the more important.",
     "fr": "Il lui faut un sol mou et humide, non drainé. En France, c'est une espèce chassable, ce qui rend l'état de ses prés humides d'autant plus important."},
    {"en": "Least Concern (IUCN); game species in France.", "fr": "Préoccupation mineure (UICN) ; espèce chassable en France."}, "#Snipe #Birds #Migration"),
   ("insect", "Sympetrum sanguineum", "sympetrum-sanguineum",
    {"en": "Ruddy darter, sympétrum sanguin", "fr": "Sympétrum sanguin"},
    {"en": "❤️🍂 Which dragonfly is still flying in October?", "fr": "❤️🍂 Quelle libellule vole encore en octobre ?"},
    {"en": "The sympétrum sanguin, ruddy darter (Sympetrum sanguineum), is one of the last dragonflies of the year; the blood-red males perch on stems in the autumn sun.",
     "fr": "Le sympétrum sanguin (Sympetrum sanguineum) est l'une des dernières libellules de l'année ; les mâles rouge sang se posent sur les tiges au soleil d'automne."},
    {"en": "It lays its eggs at the edges of ponds that dry out and fill again; the eggs wait for the water to come back.",
     "fr": "Il pond au bord des mares qui s'assèchent puis se remplissent ; les œufs attendent le retour de l'eau."},
    {"en": "Least Concern (IUCN); not protected.", "fr": "Préoccupation mineure (UICN) ; non protégé."}, "#Dragonflies #Odonata"),
   ("animal", "Micromys minutus", "micromys-minutus",
    {"en": "Harvest mouse, rat des moissons", "fr": "Rat des moissons"},
    {"en": "🐭🌾 Who builds a ball of grass in the reeds?", "fr": "🐭🌾 Qui construit une boule d'herbe dans les roseaux ?"},
    {"en": "The rat des moissons, harvest mouse (Micromys minutus), is the smallest rodent in Europe. It climbs reeds and tall grass with a tail that grips, and weaves a ball-shaped nest between the stems.",
     "fr": "Le rat des moissons (Micromys minutus) est le plus petit rongeur d'Europe. Il grimpe dans les roseaux et les hautes herbes avec une queue préhensile et tisse un nid en boule entre les tiges."},
    {"en": "It is rarely seen, and its nests, easiest to find in autumn and winter, are how most records are made. Cutting all the tall vegetation of a bank at once removes its home.",
     "fr": "On le voit rarement : ce sont ses nids, plus faciles à trouver en automne et en hiver, qui donnent la plupart des observations. Faucher d'un coup toute la végétation haute d'une berge lui retire son abri."},
    {"en": "Least Concern (IUCN).", "fr": "Préoccupation mineure (UICN)."}, "#HarvestMouse #Mammals"),
   ("fungus", "Kuehneromyces mutabilis", "kuehneromyces-mutabilis",
    {"en": "Sheathed woodtuft, pholiote changeante", "fr": "Pholiote changeante"},
    {"en": "🍄⚠️ Why do mushroom hunters fear this one's twin?", "fr": "🍄⚠️ Pourquoi les cueilleurs craignent-ils le sosie de celui-ci ?"},
    {"en": "The pholiote changeante, sheathed woodtuft (Kuehneromyces mutabilis), grows in tufts on stumps of willow, alder and poplar; its cap changes colour as it dries, two-toned for a while.",
     "fr": "La pholiote changeante (Kuehneromyces mutabilis) pousse en touffes sur les souches de saule, d'aulne et de peuplier ; son chapeau change de couleur en séchant et reste un temps bicolore."},
    {"en": "It is edible, but it grows in the same places as the galère marginée (Galerina marginata), which contains the same deadly toxins as the death cap. For recognition only: never eat it without a check by a pharmacist or a mycologist.",
     "fr": "Elle est comestible, mais elle pousse aux mêmes endroits que la galère marginée (Galerina marginata), qui contient les mêmes toxines mortelles que l'amanite phalloïde. Pour la reconnaissance seulement : ne la mangez jamais sans l'avis d'un pharmacien ou d'un mycologue."},
    {"en": "Edible, deadly look-alike: avoid. Least Concern (IUCN).", "fr": "Comestible, sosie mortel : à éviter. Préoccupation mineure (UICN)."}, "#Fungi #Mushrooms #MushroomSafety"),
   ("ecosystem", "Alnus glutinosa", "auricularia-auricula-judae",
    {"en": "Leaf fall feeds the streams", "fr": "La chute des feuilles nourrit les ruisseaux"},
    {"en": "🍂💧 What do ponds eat in autumn?", "fr": "🍂💧 De quoi se nourrissent les mares en automne ?"},
    {"en": "In autumn the leaves of alders and willows fall into ditches, streams and ponds. Fungi and bacteria soften them, and insect larvae shred them; those larvae feed fish, frogs and birds through the winter.",
     "fr": "En automne, les feuilles des aulnes et des saules tombent dans les fossés, les ruisseaux et les mares. Champignons et bactéries les ramollissent, des larves d'insectes les déchiquettent ; ces larves nourrissent poissons, grenouilles et oiseaux tout l'hiver."},
    {"en": "Autumn is also the season of fungi: in Seine-et-Marne, GBIF holds 18,296 records of fungi since 2000, and 53 % were made from September to November. A wetland without its trees and its dead wood loses much of what feeds it.",
     "fr": "L'automne est aussi la saison des champignons : en Seine-et-Marne, le GBIF compte 18 296 observations de champignons depuis 2000, dont 53 % de septembre à novembre. Une zone humide sans ses arbres et son bois mort perd une grande part de ce qui la nourrit."},
    {"en": "", "fr": ""}, "#LeafLitter #Decomposition #Ecosystems"),
  ]},
 "winter": {
  "date": {"en": "from the winter solstice, Monday 21 December 2026", "fr": "à partir du solstice d'hiver, lundi 21 décembre 2026"},
  "title": {"en": "Winter in the wetlands of Seine-et-Marne", "fr": "L'hiver dans les zones humides de Seine-et-Marne"},
  "intro": {"en": "Six posts for December to February: the standing reedbed, the bittern, a beetle under the ice, bats asleep, a scarlet cup on wet twigs, and the winter floods.",
            "fr": "Six posts pour décembre à février : la roselière debout, le butor étoilé, un coléoptère sous la glace, les chauves-souris endormies, une coupe écarlate sur les brindilles mouillées, et les crues d'hiver."},
  "posts": [
   ("plant", "Phragmites australis", "phragmites-australis",
    {"en": "Common reed, roseau commun", "fr": "Roseau commun, phragmite"},
    {"en": "🌾❄️ Why leave the reeds standing all winter?", "fr": "🌾❄️ Pourquoi laisser les roseaux debout tout l'hiver ?"},
    {"en": "In winter the roselière, the reedbed of roseau commun (Phragmites australis), is a forest of dry, pale stems topped with feathery plumes, still standing in the water.",
     "fr": "En hiver, la roselière de roseau commun (Phragmites australis) est une forêt de tiges sèches et pâles, coiffées de plumets, encore debout dans l'eau."},
    {"en": "The stems shelter insects and birds, and the reedbed filters the water that runs through it; reed beds are also built on purpose to clean wastewater. Reed was cut in winter for thatch; where it is still cut, a part is left uncut each year.",
     "fr": "Les tiges abritent insectes et oiseaux, et la roselière filtre l'eau qui la traverse ; on construit même des filtres plantés de roseaux pour épurer les eaux usées. Le roseau se coupait en hiver pour les toits de chaume ; là où on le coupe encore, on en laisse une partie chaque année."},
    {"en": "Least Concern (IUCN).", "fr": "Préoccupation mineure (UICN)."}, "#Reedbed #Phragmites"),
   ("bird", "Botaurus stellaris", "botaurus-stellaris",
    {"en": "Eurasian bittern, butor étoilé", "fr": "Butor étoilé"},
    {"en": "🐦🌾 Can you see the heron hiding in the reeds?", "fr": "🐦🌾 Voyez-vous le héron caché dans les roseaux ?"},
    {"en": "The butor étoilé, Eurasian bittern (Botaurus stellaris), is a heron striped brown like dry reeds; when alarmed it points its bill to the sky and sways with the stems. Wintering birds from further north and east join the few residents.",
     "fr": "Le butor étoilé (Botaurus stellaris) est un héron rayé de brun comme les roseaux secs ; inquiet, il pointe le bec vers le ciel et se balance avec les tiges. Des oiseaux venus du nord et de l'est rejoignent en hiver les rares résidents."},
    {"en": "It needs large, wet reedbeds, the rarest of wetland habitats; in spring the males' booming call carries for kilometres.",
     "fr": "Il lui faut de grandes roselières en eau, l'habitat humide le plus rare ; au printemps, le chant grave des mâles porte à des kilomètres."},
    {"en": "Least Concern (IUCN); protected in France; Annex I of the EU Birds Directive.", "fr": "Préoccupation mineure (UICN) ; protégé en France ; annexe I de la directive Oiseaux."}, "#Bittern #Birds #Reedbed"),
   ("insect", "Dytiscus marginalis", "dytiscus-marginalis",
    {"en": "Great diving beetle, dytique bordé", "fr": "Dytique bordé"},
    {"en": "🪲🧊 What swims under the ice?", "fr": "🪲🧊 Qu'est-ce qui nage sous la glace ?"},
    {"en": "The dytique bordé, great diving beetle (Dytiscus marginalis), stays active all winter, even under ice, carrying a bubble of air under its wing cases.",
     "fr": "Le dytique bordé (Dytiscus marginalis) reste actif tout l'hiver, même sous la glace, en emportant une bulle d'air sous ses élytres."},
    {"en": "Adults and larvae are fierce predators of tadpoles, insect larvae and small fish. A pond with dytiscus is a pond full of life.",
     "fr": "Adultes et larves sont de redoutables prédateurs de têtards, de larves d'insectes et de petits poissons. Une mare à dytiques est une mare pleine de vie."},
    {"en": "Not evaluated (IUCN).", "fr": "Non évalué (UICN)."}, "#WaterBeetles #Insects #Ponds"),
   ("animal", "Myotis daubentonii", "myotis-daubentonii",
    {"en": "Daubenton's bat, murin de Daubenton", "fr": "Murin de Daubenton"},
    {"en": "🦇❄️ Where are the bats that hunt over the river in summer?", "fr": "🦇❄️ Où sont les chauves-souris qui chassent au-dessus de la rivière en été ?"},
    {"en": "The murin de Daubenton, Daubenton's bat (Myotis daubentonii), skims the water at dusk in summer, catching insects just above the surface. In winter it hibernates in caves, cellars, quarries and under old bridges.",
     "fr": "Le murin de Daubenton (Myotis daubentonii) rase l'eau au crépuscule en été et attrape les insectes juste au-dessus de la surface. En hiver, il hiberne dans les grottes, les caves, les carrières et sous les vieux ponts."},
    {"en": "Volunteers count bats in their winter roosts each year; a bat woken in winter burns fat it cannot replace, so the counts are short and quiet.",
     "fr": "Chaque hiver, des bénévoles comptent les chauves-souris dans leurs gîtes ; une chauve-souris réveillée en hiver brûle des réserves qu'elle ne peut pas reconstituer, alors les comptages sont brefs et silencieux."},
    {"en": "Least Concern (IUCN); protected in France, like all bats.", "fr": "Préoccupation mineure (UICN) ; protégé en France, comme toutes les chauves-souris."}, "#Bats #Mammals #Hibernation"),
   ("fungus", "Sarcoscypha coccinea", "sarcoscypha-coccinea",
    {"en": "Scarlet elf cup, pézize écarlate", "fr": "Pézize écarlate"},
    {"en": "🍄❤️ What is the red cup on the fallen twig?", "fr": "🍄❤️ Quelle est cette coupe rouge sur la brindille tombée ?"},
    {"en": "The pézize écarlate, scarlet elf cup (Sarcoscypha coccinea), grows on fallen, mossy, wet twigs in damp woods from the end of winter, a bright red cup when little else is fruiting.",
     "fr": "La pézize écarlate (Sarcoscypha coccinea) pousse sur les brindilles tombées, moussues et mouillées des bois humides dès la fin de l'hiver, une coupe rouge vif quand presque rien d'autre ne fructifie."},
    {"en": "It decomposes small dead wood and needs damp air and clean surroundings. Not recommended for eating.",
     "fr": "Elle décompose le petit bois mort et a besoin d'air humide et d'un milieu propre. Consommation non recommandée."},
    {"en": "Not recommended. Not evaluated (IUCN).", "fr": "Non recommandée. Non évaluée (UICN)."}, "#Fungi #Mushrooms #WinterFungi"),
   ("ecosystem", "Phragmites australis", "alnus-glutinosa",
    {"en": "Winter floods", "fr": "Les crues d'hiver"},
    {"en": "🌊❄️ Where does a river go when it floods?", "fr": "🌊❄️ Où va une rivière quand elle déborde ?"},
    {"en": "In winter, rain falls on soils that are already wet, and the rivers rise. Where the valley is still open, they spread over meadows and alder woods instead of running straight downstream.",
     "fr": "En hiver, la pluie tombe sur des sols déjà gorgés d'eau, et les rivières montent. Là où la vallée est restée ouverte, elles s'étalent sur les prés et les aulnaies au lieu de filer vers l'aval."},
    {"en": "That flooded ground stores water, slows the flood for the towns downstream and refills the water table for the summer. It is also where pike will spawn and toads will lay in a few weeks.",
     "fr": "Ces terres inondées stockent l'eau, ralentissent la crue pour les villes en aval et rechargent la nappe pour l'été. C'est aussi là que le brochet fraiera et que les crapauds pondront dans quelques semaines."},
    {"en": "", "fr": ""}, "#Floods #Floodplain #Ecosystems"),
  ]},
}
THEMES = {"en": {"plant": "Plant", "bird": "Bird", "insect": "Insect", "animal": "Animal", "fungus": "Fungus", "ecosystem": "Ecosystem"},
          "fr": {"plant": "Plante", "bird": "Oiseau", "insect": "Insecte", "animal": "Animal", "fungus": "Champignon", "ecosystem": "Écosystème"}}
SNAME = {"en": {"spring": "Spring", "summer": "Summer", "autumn": "Autumn", "winter": "Winter"},
         "fr": {"spring": "Printemps", "summer": "Été", "autumn": "Automne", "winter": "Hiver"}}
BASE = "https://lindangulopez.github.io/wetlands-seine-et-marne"
COMMON_TAGS = {"en": "#ZonesHumides #Wetlands #SeineEtMarne #Biodiversity #GBIF #OpenData",
               "fr": "#ZonesHumides #SeineEtMarne #Biodiversite #GBIF #DonneesOuvertes"}


def page(season, lang):
    d = SEASONS[season]
    out = [f"# {d['title'][lang]}", ""]
    out += [d["intro"][lang], ""]
    out += [("**When to post:** " if lang == "en" else "**Quand publier :** ") + d["date"][lang] + (", one post a day." if lang == "en" else ", un post par jour."), ""]
    url = f"{BASE}/{'fr/' if lang=='fr' else ''}story/{season}/"
    for i, (theme, sp, slug, names, hook, p1, p2, status, tags) in enumerate(d["posts"], 1):
        out += [f"## {('Day' if lang=='en' else 'Jour')} {i}, {THEMES[lang][theme].lower()}: {names[lang]}", ""]
        out += [img(slug, names[lang]), ""]
        fig = season_fig(sp, season, lang) if theme != "ecosystem" else ""
        body1 = p1[lang] + (" " + fig if fig else "")
        series = (f"Day {i} of six on the wetlands of Seine-et-Marne in {SNAME['en'][season].lower()}: a plant, a bird, an insect, an animal, a fungus, then the whole ecosystem." if lang == "en"
                  else f"Jour {i} sur six, les zones humides de Seine-et-Marne {('au ' if season=='spring' else 'en ')}{SNAME['fr'][season].lower()} : une plante, un oiseau, un insecte, un animal, un champignon, puis tout l'écosystème.")
        lab = "Maps and sources" if lang == "en" else "Cartes et sources"
        out += [f"> {hook[lang]}", ">", f"> {body1}", ">", f"> {p2[lang]}", ">", f"> {series}", ">", f"> {lab}: 👉 {url}", ">", f"> {COMMON_TAGS[lang]} {tags}", ""]
        if status[lang]:
            out += [("*Status:* " if lang == "en" else "*Statut :* ") + status[lang], ""]
    out += ["## " + ("Sources" if lang == "en" else "Sources"), ""]
    if lang == "en":
        out += ["(i) GBIF.org occurrence search, 15 Nov 2026: records with coordinates in Seine-et-Marne (GADM FRA.8.4_1), 2000 to 2026, counted by month; IUCN categories from the GBIF species API.",
                "", "(ii) Protection in France: arrêté of 29 October 2009 (birds), arrêté of 8 January 2021 (amphibians and reptiles), arrêté of 23 April 2007 (mammals, including all bats). Wetland shares: [slide 6](../wetlands.md).",
                "", "(iii) Photos: lead images of the English Wikipedia articles, from Wikimedia Commons; one Commons photo for the puddle milkcap. Credits: [photo credits](../sources.md#photo-credits)."]
    else:
        out += ["(i) GBIF.org, recherche d'occurrences, 15 nov. 2026 : observations avec coordonnées en Seine-et-Marne (GADM FRA.8.4_1), 2000 à 2026, comptées par mois ; catégories UICN via l'API espèces du GBIF.",
                "", "(ii) Protection en France : arrêté du 29 octobre 2009 (oiseaux), arrêté du 8 janvier 2021 (amphibiens et reptiles), arrêté du 23 avril 2007 (mammifères, dont toutes les chauves-souris). Parts de zones humides : [diapositive 6](../wetlands.md).",
                "", "(iii) Photos : images principales des articles de Wikipédia en anglais, issues de Wikimedia Commons ; une photo Commons pour le lactaire des flaques. Crédits : [crédits photo](../sources.md#photo-credits)."]
    return "\n".join(out) + "\n"


for s in SEASONS:
    for lang in ("en", "fr"):
        fn = f"{DOCS}/story/{s}{'.fr' if lang=='fr' else ''}.md"
        open(fn, "w").write(page(s, lang))
        print("wrote", fn)
