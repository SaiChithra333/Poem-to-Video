"""
Offline Sample Cache for Poem-to-Video.

Provides pre-computed literary analysis, visual blueprints, 12-dimensional
keywords, and multilingual translations for built-in sample poems.
Allows the entire video generation pipeline to run offline or without
an LLM API key for testing and demonstration.
"""

from src.comprehension.visual_blueprint import VisualBlueprint

SAMPLE_CACHE = {
    "spring_dawn": {
        "paraphrase": {
            "title": "Spring Dawn (春晓)",
            "poet": "Meng Haoran (孟浩然)",
            "overall_mood": "peaceful contemplation of spring's awakening and seasonal transience",
            "overall_setting": "Traditional Chinese garden pavilion at daybreak in springtime",
            "lines": [
                {
                    "original": "春眠不觉晓，",
                    "literal_meaning": "In spring slumber, one wakes without realizing dawn has already arrived.",
                    "imagery": "Soft morning sunlight filtering through ornate wooden lattice windows onto a peaceful bed chamber, gentle morning mist outside.",
                    "emotion": "peaceful drowsiness and tranquil awakening",
                    "dominant_emotion": "tranquility",
                    "ner_tags": ["PERSON: sleeping poet", "PLACE: traditional pavilion bedroom", "TIME: early dawn"],
                    "symbolism": "The effortless harmony of human life with the natural rhythms of spring.",
                    "background": "Meng Haoran was renowned for his tranquil nature poetry."
                },
                {
                    "original": "处处闻啼鸟。",
                    "literal_meaning": "From everywhere all around, the melodious songs of birds can be heard.",
                    "imagery": "Vibrant songbirds perched among fresh green leaves and flowering peach blossoms, singing joyfully in morning light.",
                    "emotion": "cheerful joy and lively celebration of life",
                    "dominant_emotion": "joy",
                    "ner_tags": ["NATURE_OBJECT: chirping songbirds", "NATURE_OBJECT: blooming branches", "TIME: spring morning"],
                    "symbolism": "The spontaneous vitality and acoustic abundance of spring awakening.",
                    "background": "Tang nature poetry celebrated awakening to bird songs after secluded winter."
                },
                {
                    "original": "夜来风雨声，",
                    "literal_meaning": "Remembering the sound of wind and rain blowing through the trees during the night.",
                    "imagery": "Glistening damp flagstones in a stone courtyard, misty raindrops dripping from bamboo eaves into mossy garden puddles.",
                    "emotion": "reflective quietness and gentle contemplation",
                    "dominant_emotion": "contemplation",
                    "ner_tags": ["NATURE_OBJECT: wind and rain", "PLACE: courtyard veranda", "TIME: past stormy night"],
                    "symbolism": "The quiet awareness of unseen natural transformations occurring while one slept.",
                    "background": "Spring storms in southern China commonly scatter spring blossoms overnight."
                },
                {
                    "original": "花落知多少。",
                    "literal_meaning": "Wondering how many delicate blossoms have fallen to the ground overnight.",
                    "imagery": "Delicate pink and white flower petals scattered across damp green moss and dark stone steps, dewy morning glow.",
                    "emotion": "tender poignancy and wistful appreciation of beauty",
                    "dominant_emotion": "wistfulness",
                    "ner_tags": ["NATURE_OBJECT: fallen flower petals", "PLACE: garden pathway", "ABSTRACT: ephemeral beauty"],
                    "symbolism": "Appreciation of transience and the fleeting perfection of youth and spring.",
                    "background": "Appreciation of fallen petals is a core theme in classical Chinese literati aesthetics."
                }
            ]
        },
        "blueprint": VisualBlueprint(
            persistent_location="A traditional Chinese courtyard garden with carved wooden pavilion verandas, weeping willows, bamboo groves, and stone pathways with moss",
            color_script="Parchment ivory #F4EFE6, charcoal ink #2B2B2B, celadon green #8EA89D, and delicate cinnabar pink #D97A7A",
            unified_lighting="Soft diffused morning dawn light with gentle luminous mist",
            artist_influences="Shen Zhou, Wen Zhengming, and Baishi Qi traditional ink wash painting",
            overall_atmosphere="Tranquil, meditative, tenderly poignant spring dawn awakening",
            shot_progression=[
                {
                    "segment_id": 0,
                    "shot_type": "wide_establishing",
                    "camera_motion": "pan_horizontal",
                    "visual_focus": "Courtyard pavilion veranda enveloped in morning dawn mist",
                    "metaphor_guidance": "Quiet contemplation before the day begins"
                },
                {
                    "segment_id": 1,
                    "shot_type": "medium_shot",
                    "camera_motion": "tilt_up",
                    "visual_focus": "Songbirds chirping on blooming peach branches outside the veranda",
                    "metaphor_guidance": "Lively awakening of nature"
                },
                {
                    "segment_id": 2,
                    "shot_type": "medium_tracking",
                    "camera_motion": "dolly_in",
                    "visual_focus": "Damp mossy courtyard stones with rainwater reflections from last night",
                    "metaphor_guidance": "Memory of nocturnal rain"
                },
                {
                    "segment_id": 3,
                    "shot_type": "macro_close_up",
                    "camera_motion": "slow_zoom_in",
                    "visual_focus": "Delicate fallen pink flower petals resting on wet mossy flagstones",
                    "metaphor_guidance": "The gentle transience of beauty"
                }
            ],
            base_seed=42108
        ),
        "key_elements": [
            {
                "Subject": "traditional Chinese courtyard pavilion, wooden lattice window, sleeping scholar robes, gentle morning mist",
                "Action": "resting peacefully, morning mist drifting slowly",
                "Context": "interior looking out through carved pavilion lattice towards misty garden",
                "Environment": "dawn, spring morning, misty, quiet veranda",
                "Lighting": "soft dawn illumination, diffused morning glow",
                "Artist": "Shen Zhou, Baishi Qi",
                "Style": "traditional Chinese ink wash painting, literati painting",
                "Medium": "Chinese ink and subtle mineral color wash on aged Xuan rice paper",
                "Type": "architectural landscape, atmospheric view",
                "Color Scheme": "antique cream parchment, celadon green, charcoal black ink, subtle peach wash",
                "Computer Graphics": "none",
                "Quality": "masterpiece, finest detail, highly intricate brushwork, 8K resolution"
            },
            {
                "Subject": "spring songbirds, flowering peach branches, fresh willow leaves",
                "Action": "birds chirping, wings fluttering, blossoms opening",
                "Context": "midground garden foliage framed by veranda pillars",
                "Environment": "vibrant spring morning, lush green garden",
                "Lighting": "golden morning rays breaking through misty air",
                "Artist": "Baishi Qi, Zhao Mengfu",
                "Style": "traditional Chinese ink wash painting with delicate gongbi floral details",
                "Medium": "Chinese ink and subtle pastel pigments on textured rice paper",
                "Type": "bird and flower painting, lively nature landscape",
                "Color Scheme": "vivid spring greens, pale coral blossom accents, sumi ink tones",
                "Computer Graphics": "none",
                "Quality": "masterpiece, exquisite brushwork, highly detailed feather and petal textures"
            },
            {
                "Subject": "stone courtyard, wet mossy flagstones, bamboo eaves dripping water droplets, lingering puddles",
                "Action": "water dripping gently, morning breeze swaying bamboo",
                "Context": "ground level looking across courtyard garden path",
                "Environment": "post-rain morning, damp courtyard, gentle spring breeze",
                "Lighting": "soft overcast morning light reflecting in wet stones",
                "Artist": "Wen Zhengming, Ni Zan",
                "Style": "traditional Chinese ink wash landscape",
                "Medium": "moist ink wash, splashed ink technique on rice paper",
                "Type": "courtyard landscape, atmospheric wet garden",
                "Color Scheme": "deep charcoal ink, moss green, wet stone grey, pale water reflections",
                "Computer Graphics": "none",
                "Quality": "masterpiece, evocative atmospheric mood, fine textural detailing"
            },
            {
                "Subject": "fallen pink flower petals, wet dark moss, weathered stone garden steps",
                "Action": "petals resting on damp ground, water droplets glistening",
                "Context": "intimate close-up perspective of garden pathway",
                "Environment": "spring dawn garden path, fresh damp earth",
                "Lighting": "gentle morning glint highlighting water drops on petals",
                "Artist": "Baishi Qi, Yun Shouping",
                "Style": "traditional Chinese ink wash painting with fine flower and leaf painting",
                "Medium": "fine line ink with delicate translucent cinnabar washes",
                "Type": "botanical close-up, poetic nature vignette",
                "Color Scheme": "antique parchment, wet charcoal stone, tender cinnabar pink, emerald moss",
                "Computer Graphics": "none",
                "Quality": "masterpiece, delicate poetic atmosphere, exquisite high resolution"
            }
        ],
        "translations": {
            "zh": [
                "春眠不觉晓，",
                "处处闻啼鸟。",
                "夜来风雨声，",
                "花落知多少。"
            ],
            "en": [
                "In spring slumber, unaware of dawn arriving,",
                "Everywhere is filled with the sweet song of birds.",
                "In the night came sounds of wind and rain,",
                "Who knows how many blossoms have fallen?"
            ]
        }
    },
    "daffodils": {
        "paraphrase": {
            "title": "I Wandered Lonely as a Cloud",
            "poet": "William Wordsworth",
            "overall_mood": "joyous awe and elevated spiritual communion with nature",
            "overall_setting": "English Lake District shore with breeze, daffodils, and shimmering water",
            "lines": [
                {
                    "original": "I wandered lonely as a cloud\nThat floats on high o'er vales and hills,",
                    "literal_meaning": "The poet wanders alone through the countryside like a solitary floating cloud.",
                    "imagery": "Panoramic vista of rolling green hills, misty valleys, and blue sky with a solitary soft white cloud floating overhead.",
                    "emotion": "gentle solitude and detached contemplation",
                    "dominant_emotion": "solitude",
                    "ner_tags": ["PERSON: solitary wanderer", "NATURE_OBJECT: floating cloud", "PLACE: green vales and hills"],
                    "symbolism": "The solitary human spirit seeking sublime communion with nature.",
                    "background": "Wordsworth wrote this poem inspired by a walk with his sister Dorothy in the Lake District."
                },
                {
                    "original": "When all at once I saw a crowd,\nA host, of golden daffodils;",
                    "literal_meaning": "Suddenly coming upon an immense gathering of radiant golden daffodils.",
                    "imagery": "Vast carpet of thousands of luminous yellow daffodils glowing in sunlight alongside clear lake water.",
                    "emotion": "delightful surprise and exhilaration",
                    "dominant_emotion": "joy",
                    "ner_tags": ["NATURE_OBJECT: golden daffodils", "PLACE: lakeside", "ABSTRACT: sudden wonder"],
                    "symbolism": "The unexpected epiphany of natural abundance transforming loneliness into joy.",
                    "background": "The Lake District flora famously inspired the English Romantic movement."
                },
                {
                    "original": "Beside the lake, beneath the trees,\nFluttering and dancing in the breeze.",
                    "literal_meaning": "The blossoms swaying and dancing continuously under trees in the wind.",
                    "imagery": "Gentle spring wind sweeping over golden blossoms under tall oak trees, shimmering water reflections sparkling in the background.",
                    "emotion": "ecstatic joy and rhythmic harmony",
                    "dominant_emotion": "joy",
                    "ner_tags": ["NATURE_OBJECT: ancient trees", "NATURE_OBJECT: dancing daffodils", "NATURE_OBJECT: fresh spring breeze"],
                    "symbolism": "Universal living dance connecting flora, wind, water, and human perception.",
                    "background": "Romantic pantheism viewed nature as animated by a joyful vital spirit."
                }
            ]
        },
        "blueprint": VisualBlueprint(
            persistent_location="A serene English Lake District lakeshore with rolling green meadows, ancient oak trees, and sparkling blue lake water",
            color_script="Golden daffodil yellow #F5D061, lush meadow green #5E8B63, mountain lake azure #4A7A96, and soft cloud white #F7F9FA",
            unified_lighting="Bright morning sun with luminous reflections on rippling water",
            artist_influences="J.M.W. Turner, John Constable, English Romantic watercolorists",
            overall_atmosphere="Lyrical, vibrant, serene, and spiritually uplifting",
            shot_progression=[
                {
                    "segment_id": 0,
                    "shot_type": "wide_establishing",
                    "camera_motion": "pan_horizontal",
                    "visual_focus": "Rolling green hills beneath an open blue sky with floating cloud",
                    "metaphor_guidance": "Solitary wandering through majestic nature"
                },
                {
                    "segment_id": 1,
                    "shot_type": "medium_shot",
                    "camera_motion": "dolly_in",
                    "visual_focus": "Golden daffodils blooming profusely beside the shimmering lake",
                    "metaphor_guidance": "Sudden arrival at a field of luminous golden joy"
                },
                {
                    "segment_id": 2,
                    "shot_type": "macro_close_up",
                    "camera_motion": "slow_zoom_in",
                    "visual_focus": "Dancing daffodil petals fluttering in the breeze beneath shady oak boughs",
                    "metaphor_guidance": "Joyous harmonious rhythm of life and wind"
                }
            ],
            base_seed=51829
        ),
        "key_elements": [
            {
                "Subject": "solitary cloud, expansive green valleys, rolling mountain hills",
                "Action": "floating high above, drifting slowly",
                "Context": "panoramic bird's eye view over emerald landscape",
                "Environment": "sunny day, English countryside, rolling meadows",
                "Lighting": "open daylight, soft shadows across valley",
                "Artist": "John Constable, J.M.W. Turner",
                "Style": "English Romantic watercolor painting",
                "Medium": "watercolor on cold-pressed textured cotton paper, luminous washes",
                "Type": "panoramic landscape",
                "Color Scheme": "sky blue, soft cloud white, vibrant emerald greens, warm earth tones",
                "Computer Graphics": "none",
                "Quality": "masterpiece, fluid translucent washes, expressive brushwork, 8K resolution"
            },
            {
                "Subject": "mass of golden daffodils, sparkling mountain lake shore, grassy bank",
                "Action": "blooming vibrantly, catching brilliant sunlight",
                "Context": "lakeside shore extending towards distant hills",
                "Environment": "spring morning, clear mountain lake, fresh outdoor air",
                "Lighting": "sparkling golden hour sunlight reflecting off lake ripples",
                "Artist": "J.M.W. Turner, Thomas Girtin",
                "Style": "Romantic watercolor landscape",
                "Medium": "layered watercolor with vibrant gouache highlights on paper",
                "Type": "lakeside field landscape",
                "Color Scheme": "radiant cadmium yellow, lake cerulean, fresh sap green",
                "Computer Graphics": "none",
                "Quality": "masterpiece, luminous watercolor glow, high detail floral textures"
            },
            {
                "Subject": "fluttering daffodils, ancient oak trees, breeze ripples on water surface",
                "Action": "dancing in the wind, petals fluttering, branches swaying",
                "Context": "beneath mossy tree canopy looking toward sunlit water edge",
                "Environment": "gentle breeze, dappled shade and bright sun patches",
                "Lighting": "dappled sunlight filtering through green leaves onto golden petals",
                "Artist": "John Sell Cotman, J.M.W. Turner",
                "Style": "English Romantic watercolor illustration",
                "Medium": "translucent watercolor with delicate wet-on-wet bloom effects",
                "Type": "dynamic nature composition",
                "Color Scheme": "golden amber, leaf green, bark brown, sparkling white highlights",
                "Computer Graphics": "none",
                "Quality": "masterpiece, poetic motion, exquisite watercolor dynamics"
            }
        ],
        "translations": {
            "en": [
                "I wandered lonely as a cloud that floats on high o'er vales and hills,",
                "When all at once I saw a crowd, a host of golden daffodils;",
                "Beside the lake, beneath the trees, fluttering and dancing in the breeze."
            ],
            "zh": [
                "我如孤云独自漫游，飘浮在崇山幽谷之上，",
                "蓦然回首一片金黄，无边无际的水仙花海；",
                "在清澈湖畔绿树荫下，迎着和煦微风翩跹起舞。"
            ]
        }
    },
    "quiet_night": {
        "paraphrase": {
            "title": "Quiet Night Thought (静夜思)",
            "poet": "Li Bai (李白)",
            "overall_mood": "quiet solitude, homesickness, and serene moonlit contemplation",
            "overall_setting": "Traditional wooden chamber at midnight with bright moonlight through window",
            "lines": [
                {
                    "original": "床前明月光，",
                    "literal_meaning": "Bright moonlight pools upon the floor in front of the bed.",
                    "imagery": "A quiet wooden room in darkness, with a luminous beam of silver moonlight streaming through a lattice window onto the floor.",
                    "emotion": "solitude and peaceful stillness",
                    "dominant_emotion": "solitude",
                    "ner_tags": ["NATURE_OBJECT: bright moonlight", "PLACE: bed chamber", "TIME: midnight"],
                    "symbolism": "Moonlight as an uninvited yet serene companion in solitary stillness.",
                    "background": "Li Bai's most famous poem taught to children across the Chinese-speaking world."
                },
                {
                    "original": "疑是地上霜。",
                    "literal_meaning": "Looking down, one suspects it might be autumn frost upon the ground.",
                    "imagery": "The silver moonlight on the wooden floorboards glimmers with the cool whiteness of early winter frost.",
                    "emotion": "chilliness and quiet bewilderment",
                    "dominant_emotion": "surprise",
                    "ner_tags": ["NATURE_OBJECT: frost", "PLACE: floor", "ABSTRACT: illusion"],
                    "symbolism": "The coldness of the frost evokes the inner chill of being far from family and home.",
                    "background": "Autumn frost represents the passage of the year and distance from loved ones."
                },
                {
                    "original": "举头望明月，",
                    "literal_meaning": "Raising one's head to gaze up at the luminous round moon in the night sky.",
                    "imagery": "Looking up through the open window into the deep velvet indigo night, seeing the full silver moon glowing among quiet stars.",
                    "emotion": "longing, awe, and contemplation",
                    "dominant_emotion": "longing",
                    "ner_tags": ["NATURE_OBJECT: full moon", "NATURE_OBJECT: night sky", "PERSON: wandering poet"],
                    "symbolism": "The moon is a universal bridge connecting separated people across vast distances.",
                    "background": "In Chinese poetry, looking at the moon is the universal metaphor for missing home."
                },
                {
                    "original": "低头思故乡。",
                    "literal_meaning": "Lowering one's head, overcome with deep thoughts and yearning for one's hometown.",
                    "imagery": "The silhouette of a solitary poet in traditional Tang dynasty robes with head bowed in quiet reflection, shadowed against moonlit wall.",
                    "emotion": "deep nostalgia, homesickness, and tenderness",
                    "dominant_emotion": "melancholy",
                    "ner_tags": ["PERSON: pensive poet", "PLACE: distant homeland", "ABSTRACT: homesickness"],
                    "symbolism": "The return of thoughts inward to the roots of identity, family, and origin.",
                    "background": "Tang travelers were often separated from their ancestral homes for years."
                }
            ]
        },
        "blueprint": VisualBlueprint(
            persistent_location="A serene traditional Tang dynasty scholar's chamber with open lattice window looking onto a moonlit courtyard and distant mountain silhouettes",
            color_script="Deep midnight indigo #1A2238, luminous moon silver #E8ECEF, cool wood charcoal #2C3539, and quiet celadon grey #7A8B8B",
            unified_lighting="Cool, crisp, luminous silver moonlight casting sharp soft-edged shadows across wooden floors",
            artist_influences="Ni Zan, Mi Fu, and classic Tang monochrome ink masters",
            overall_atmosphere="Quiet, nocturnal, contemplative, and poignant solitude",
            shot_progression=[
                {
                    "segment_id": 0,
                    "shot_type": "medium_shot",
                    "camera_motion": "slow_zoom_in",
                    "visual_focus": "Moonlight streaming through lattice window onto the dark polished floor",
                    "metaphor_guidance": "The sudden arrival of silver light in silence"
                },
                {
                    "segment_id": 1,
                    "shot_type": "macro_close_up",
                    "camera_motion": "pan_horizontal",
                    "visual_focus": "Silver moonlight shimmering on the floor looking like delicate frost crystals",
                    "metaphor_guidance": "The poetic illusion of frost in autumn"
                },
                {
                    "segment_id": 2,
                    "shot_type": "tilt_up",
                    "camera_motion": "tilt_up",
                    "visual_focus": "Gazing through window at the brilliant full moon glowing in deep indigo sky",
                    "metaphor_guidance": "Connecting to home across thousands of miles"
                },
                {
                    "segment_id": 3,
                    "shot_type": "wide_establishing",
                    "camera_motion": "slow_zoom_in",
                    "visual_focus": "Solitary silhouette of the poet with bowed head beside the moonlit window",
                    "metaphor_guidance": "Quiet surrender to memories of distant home"
                }
            ],
            base_seed=18293
        ),
        "key_elements": [
            {
                "Subject": "traditional Tang chamber, wooden bed, luminous beam of moonlight, dark timber floor",
                "Action": "shining brightly, streaming silently",
                "Context": "interior chamber framed by lattice window",
                "Environment": "midnight, quiet autumn night, clear sky",
                "Lighting": "radiant silver moonlight against dark interior",
                "Artist": "Ni Zan, Ma Yuan",
                "Style": "traditional Chinese ink wash painting",
                "Medium": "monochrome Chinese ink with subtle silver-blue wash on Xuan paper",
                "Type": "nocturnal interior landscape",
                "Color Scheme": "midnight blue, moon silver, dark timber charcoal",
                "Computer Graphics": "none",
                "Quality": "masterpiece, delicate gradations of ink, evocative atmosphere, 8K"
            },
            {
                "Subject": "silver light pool on wooden planks, appearance of autumn frost crystals",
                "Action": "glistening coolly, spreading across floorboards",
                "Context": "low angle looking across moonlit floor",
                "Environment": "cold autumn night, still indoor air",
                "Lighting": "cool icy silver illumination, high contrast shadows",
                "Artist": "Muqi, Liang Kai",
                "Style": "traditional Chinese ink wash, minimalist Zen aesthetic",
                "Medium": "fine brushwork with subtle white mineral pigment accents",
                "Type": "close-up textural study",
                "Color Scheme": "frost silver, pale slate, deep indigo shadow",
                "Computer Graphics": "none",
                "Quality": "masterpiece, subtle textural mastery, high detail"
            },
            {
                "Subject": "brilliant full moon, open lattice window frame, deep midnight sky, faint stars",
                "Action": "glowing luminously, floating in velvet sky",
                "Context": "looking up through open window towards night sky",
                "Environment": "clear crisp autumn midnight",
                "Lighting": "intense ethereal lunar glow, soft atmospheric halo",
                "Artist": "Ma Yuan, Xia Gui",
                "Style": "classical Song dynasty ink landscape",
                "Medium": "graded ink washes with reserved white paper for moon",
                "Type": "celestial nocturnal landscape",
                "Color Scheme": "deep indigo, luminous pearl white, midnight black",
                "Computer Graphics": "none",
                "Quality": "masterpiece, sublime simplicity, poetic resonance"
            },
            {
                "Subject": "solitary poet silhouette in Tang scholar robes, bowed head, quiet room",
                "Action": "standing in contemplation, head bowed in longing",
                "Context": "interior profile against moonlit courtyard backdrop",
                "Environment": "quiet midnight, timeless contemplation",
                "Lighting": "backlit by silver moonlight with gentle rim lighting",
                "Artist": "Liang Kai, Chen Hongshou",
                "Style": "traditional Chinese literati figure painting",
                "Medium": "expressive sumi-e ink brushstrokes with subtle washes",
                "Type": "poetic figure painting",
                "Color Scheme": "ink monochrome, muted silver grey, warm paper ground",
                "Computer Graphics": "none",
                "Quality": "masterpiece, profound emotional depth, refined brushwork"
            }
        ],
        "translations": {
            "zh": [
                "床前明月光，",
                "疑是地上霜。",
                "举头望明月，",
                "低头思故乡。"
            ],
            "en": [
                "Before my bed a pool of bright moonlight,",
                "Looking like frost upon the ground.",
                "I raise my head to gaze at the bright moon,",
                "And lower my head, thinking of my home."
            ]
        }
    },
    "basho_old_pond": {
        "paraphrase": {
            "title": "The Old Pond (古池や)",
            "poet": "Matsuo Bashō (松尾芭蕉)",
            "overall_mood": "Zen tranquility, sudden natural motion, and timeless stillness",
            "overall_setting": "Ancient mossy temple garden pond in Japan under quiet trees",
            "lines": [
                {
                    "original": "古池や",
                    "literal_meaning": "An ancient, quiet pond resting undisturbed.",
                    "imagery": "Still emerald water in an ancient stone pond, surrounded by lush moss, quiet bamboo grove, and floating green lily pads.",
                    "emotion": "deep stillness and meditative serenity",
                    "dominant_emotion": "tranquility",
                    "ner_tags": ["PLACE: ancient stone pond", "NATURE_OBJECT: mossy rocks", "TIME: quiet afternoon"],
                    "symbolism": "The timeless, unmoving universe waiting in deep silence.",
                    "background": "Basho composed this quintessential Zen haiku at his cottage in Fukagawa."
                },
                {
                    "original": "蛙飛びこむ",
                    "literal_meaning": "A frog suddenly leaps in.",
                    "imagery": "A small green frog leaping gracefully from a mossy stone into the still surface of the clear pond.",
                    "emotion": "spontaneous energy and awakening life",
                    "dominant_emotion": "surprise",
                    "ner_tags": ["NATURE_OBJECT: green frog", "PLACE: water surface", "ABSTRACT: sudden movement"],
                    "symbolism": "The momentary spark of dynamic action breaking through eternal stillness.",
                    "background": "The leap of the frog is the kinetic spark that activates human perception."
                },
                {
                    "original": "水の音",
                    "literal_meaning": "The gentle plop sound of water rippling outward.",
                    "imagery": "Concentric silver water ripples spreading gently outward across the mirror-like surface of the pond, fading into silence.",
                    "emotion": "sublime peace and returning silence",
                    "dominant_emotion": "tranquility",
                    "ner_tags": ["NATURE_OBJECT: water ripples", "ABSTRACT: acoustic silence", "PLACE: temple pond"],
                    "symbolism": "Sound dissolves back into the great cosmic silence.",
                    "background": "In Zen aesthetics, the sound deepens the surrounding silence."
                }
            ]
        },
        "blueprint": VisualBlueprint(
            persistent_location="An ancient Japanese temple garden with a dark stone-rimmed pond, mossy flagstones, bamboo, and weeping maple boughs",
            color_script="Moss green #4A6B48, bamboo celadon #829875, stone charcoal #36393B, and water reflection azure #587285",
            unified_lighting="Soft diffused dappled garden sunlight filtering through lush tree canopy",
            artist_influences="Makoto Shinkai, Studio Ghibli, and classical Japanese ukiyo-e woodblock landscapes",
            overall_atmosphere="Zen tranquility, meditative silence, and crystal-clear acoustic clarity",
            shot_progression=[
                {
                    "segment_id": 0,
                    "shot_type": "wide_establishing",
                    "camera_motion": "pan_horizontal",
                    "visual_focus": "The entire mossy stone pond resting in temple garden silence",
                    "metaphor_guidance": "Timeless stillness of the natural world"
                },
                {
                    "segment_id": 1,
                    "shot_type": "medium_shot",
                    "camera_motion": "dolly_in",
                    "visual_focus": "A small green tree frog poised on a mossy boulder above the water",
                    "metaphor_guidance": "Poised anticipation before action"
                },
                {
                    "segment_id": 2,
                    "shot_type": "macro_close_up",
                    "camera_motion": "slow_zoom_in",
                    "visual_focus": "Concentric circular ripples expanding on the glassy pond surface",
                    "metaphor_guidance": "Echo of sound returning to profound silence"
                }
            ],
            base_seed=77218
        ),
        "key_elements": [
            {
                "Subject": "ancient Japanese temple pond, mossy stone basin, bamboo water spout, floating lotus leaf",
                "Action": "resting in absolute stillness, water reflecting garden canopy",
                "Context": "wide view of traditional Japanese garden enclosure",
                "Environment": "quiet garden, ancient temple courtyard, secluded outdoor",
                "Lighting": "dappled soft afternoon sunlight through maple leaves",
                "Artist": "Studio Ghibli, Makoto Shinkai, Hasui Kawase",
                "Style": "anime background art, cinematic aesthetic",
                "Medium": "digital painting with lush painterly textures and atmospheric lighting",
                "Type": "tranquil landscape",
                "Color Scheme": "deep moss green, warm timber charcoal, slate grey stone, sky reflection blue",
                "Computer Graphics": "octane render, anime cinematography",
                "Quality": "masterpiece, 8K wallpaper, Makoto Shinkai quality, breathtaking detail"
            },
            {
                "Subject": "vibrant green frog, mossy boulder edge, clear water surface",
                "Action": "leaping through air, diving into water",
                "Context": "dynamic mid-shot at water level capturing motion",
                "Environment": "pond edge, lush foliage, clean fresh water",
                "Lighting": "focused sunbeam catching airborne water droplets",
                "Artist": "Studio Ghibli, Makoto Shinkai",
                "Style": "anime background art, cinematic animation frame",
                "Medium": "digital painting with dynamic motion blur and specular droplets",
                "Type": "action wildlife vignette",
                "Color Scheme": "bright emerald green, sparkling white spray, dark pond green",
                "Computer Graphics": "cinematic anime render",
                "Quality": "masterpiece, dynamic framing, highly detailed"
            },
            {
                "Subject": "concentric circular water ripples, reflection of green leaves, clear pond surface",
                "Action": "rippling outward in smooth circles, water settling back to glass",
                "Context": "overhead downward macro angle of expanding ripples",
                "Environment": "serene garden pond, stillness after sound",
                "Lighting": "glistening highlights tracing each concentric ripple crest",
                "Artist": "Makoto Shinkai, Hasui Kawase",
                "Style": "anime background art, contemplative Japanese landscape",
                "Medium": "digital painting with crystal translucent water caustics",
                "Type": "macro water study",
                "Color Scheme": "cool azure, emerald water depth, silver highlight rings",
                "Computer Graphics": "octane render, photorealistic anime caustics",
                "Quality": "masterpiece, exquisite liquid dynamics, meditative serenity"
            }
        ],
        "translations": {
            "ja": [
                "古池や",
                "蛙飛びこむ",
                "水の音"
            ],
            "en": [
                "The old pond —",
                "A frog leaps in,",
                "Sound of water."
            ]
        }
    }
}


def find_sample_key(text_or_sample: str) -> str | None:
    """Find matching sample key if text corresponds to a known sample."""
    if not text_or_sample:
        return None
    normalized = text_or_sample.strip().lower().replace("_", " ")
    for key in SAMPLE_CACHE:
        clean_key = key.replace("_", " ")
        if clean_key in normalized or key in normalized:
            return key
    # Check text snippets & titles
    if "春晓" in text_or_sample or "春眠" in text_or_sample or "spring dawn" in normalized:
        return "spring_dawn"
    if "daffodils" in normalized or "wandered lonely" in normalized:
        return "daffodils"
    if "床前明月光" in text_or_sample or "静夜思" in text_or_sample or "quiet night" in normalized:
        return "quiet_night"
    if "古池" in text_or_sample or "basho" in normalized or "old pond" in normalized:
        return "basho_old_pond"
    return None


def get_cached_sample(sample_key: str) -> dict | None:
    """Retrieve pre-computed sample data."""
    return SAMPLE_CACHE.get(sample_key)
