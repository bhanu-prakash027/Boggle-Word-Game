"""
Script to generate a rich starter English dictionary for the Boggle game.
Contains thousands of common English words and valid inflections.
"""
import os

BASE_WORDS = [
    # A
    "abandon", "ability", "able", "about", "above", "abroad", "absence", "absent", "absolute", "absorb", "abstract",
    "absurd", "abuse", "academic", "accept", "access", "accident", "accompany", "accomplish", "according", "account",
    "accurate", "accuse", "achieve", "acid", "acquire", "across", "action", "active", "actor", "actress", "actual",
    "adapt", "addition", "address", "adequate", "adjust", "admire", "admit", "adopt", "adult", "advance", "advantage",
    "adventure", "advice", "advise", "affair", "affect", "afford", "afraid", "after", "again", "against", "agency",
    "agenda", "agent", "aggressive", "agree", "agreement", "ahead", "aircraft", "airline", "airport", "alarm", "album",
    "alcohol", "alert", "alien", "alike", "alive", "alleged", "alliance", "allow", "almost", "alone", "along", "already",
    "alter", "alternative", "although", "always", "amazing", "ambition", "among", "amount", "analysis", "analyst", "analyze",
    "ancient", "anger", "angle", "angry", "animal", "annual", "another", "answer", "anxiety", "anybody", "anymore",
    "anyone", "anything", "anyway", "anywhere", "apart", "apartment", "apparent", "appeal", "appear", "appearance", "apple",
    "application", "apply", "appoint", "appreciate", "approach", "appropriate", "approval", "approve", "approximate", "architect",
    "architecture", "area", "argue", "argument", "arise", "armed", "army", "around", "arrange", "arrangement", "arrest",
    "arrival", "arrive", "arrow", "article", "artist", "artistic", "aside", "aspect", "assault", "assert", "assess",
    "asset", "assign", "assist", "associate", "association", "assume", "assumption", "assure", "athlete", "athletic",
    "atmosphere", "attach", "attack", "attempt", "attend", "attention", "attitude", "attorney", "attract", "attractive",
    "attribute", "audience", "author", "authority", "automatic", "available", "average", "avoid", "award", "aware", "awareness",
    "away", "awful", "agent", "acute", "anchor", "angel", "amber", "amuse", "antic", "apron", "arena", "aroma",
    
    # B
    "baby", "back", "background", "bacon", "badge", "badly", "bagel", "baker", "bakery", "balance", "balcony", "ball",
    "balloon", "banana", "band", "bank", "banker", "banner", "barely", "bargain", "barrel", "barrier", "base", "baseball",
    "basement", "basic", "basically", "basis", "basket", "basketball", "battery", "battle", "beach", "beam", "bean",
    "bear", "beard", "beast", "beat", "beautiful", "beauty", "become", "bedroom", "beef", "beer", "before", "began",
    "begin", "beginning", "behalf", "behave", "behavior", "behind", "being", "belief", "believe", "bell", "belong",
    "below", "belt", "bench", "bend", "beneath", "benefit", "beside", "besides", "best", "better", "between", "beyond",
    "bicycle", "bike", "bill", "billion", "binary", "bind", "biography", "biology", "bird", "birth", "birthday",
    "bishop", "bite", "bitter", "black", "blade", "blame", "blank", "blanket", "blast", "blend", "bless", "blind",
    "block", "blood", "bloody", "bloom", "blossom", "blow", "blue", "board", "boat", "body", "boil", "bold",
    "bomb", "bond", "bone", "bonus", "book", "boom", "boot", "booth", "border", "bored", "boring", "born",
    "borrow", "boss", "both", "bother", "bottle", "bottom", "bounce", "boundary", "bowl", "bracket", "brain", "brake",
    "branch", "brand", "brass", "brave", "bread", "break", "breakfast", "breast", "breath", "breathe", "breeze", "brick",
    "bride", "bridge", "brief", "bright", "brilliant", "bring", "broad", "broadcast", "broken", "broker", "bronze", "brother",
    "brown", "brush", "bubble", "budget", "build", "builder", "building", "bulb", "bulk", "bullet", "bunch", "burden",
    "bureau", "burn", "burst", "bury", "bush", "business", "busy", "butter", "button", "buyer",

    # C
    "cabin", "cabinet", "cable", "cafe", "cage", "cake", "calculate", "calendar", "call", "caller", "calm", "camera",
    "camp", "campaign", "campus", "canal", "cancel", "cancer", "candidate", "candle", "candy", "cane", "canvas",
    "capable", "capacity", "capital", "captain", "capture", "carbon", "card", "care", "career", "careful", "carefully",
    "cargo", "carpet", "carrier", "carrot", "carry", "cart", "case", "cash", "casino", "cast", "castle",
    "casual", "casualty", "catalog", "catch", "category", "cater", "cause", "cave", "cease", "ceiling", "celebrate",
    "celebrity", "cell", "cemetery", "center", "central", "century", "ceremony", "certain", "chain", "chair", "chairman",
    "chalk", "challenge", "chamber", "champion", "chance", "change", "channel", "chaos", "chapter", "charge", "charity",
    "charm", "chart", "chase", "cheap", "cheat", "check", "cheek", "cheer", "cheese", "chef", "chemical", "cherry",
    "chest", "chicken", "chief", "child", "childhood", "chili", "chill", "chimney", "chin", "chip", "choice",
    "choose", "chorus", "chronic", "church", "cider", "cigar", "cigarette", "circle", "circuit", "circus", "cite",
    "citizen", "city", "civil", "civilian", "claim", "clamp", "clan", "clash", "class", "classic", "clean",
    "cleaner", "clear", "clerk", "clever", "click", "client", "cliff", "climate", "climb", "clinic", "clinical",
    "clip", "clock", "clone", "close", "closet", "cloth", "clothes", "clothing", "cloud", "clown", "club",
    "cluster", "coach", "coal", "coalition", "coast", "coastal", "coat", "cocktail", "cocoa", "code", "coffee",
    "cognitive", "coin", "cold", "collar", "colleague", "collect", "college", "colony", "color", "column", "combat",
    "combine", "comedy", "comfort", "comic", "command", "comment", "commerce", "commission", "commit", "committee", "common",
    "community", "company", "compare", "compel", "compete", "complete", "complex", "comply", "compose", "compound", "computer",
    "concept", "concern", "concert", "conclude", "concrete", "condition", "conduct", "conference", "confirm", "conflict",
    "confront", "confuse", "connect", "conscious", "consent", "consequence", "conservative", "consider", "consist", "consistent",
    "constant", "constitute", "construct", "consult", "consume", "contact", "contain", "content", "contest", "context",
    "continue", "contract", "contrast", "contribute", "control", "convert", "convince", "cook", "cookie", "cooking",
    "cool", "cooperate", "cope", "copper", "copy", "coral", "core", "corn", "corner", "corporate", "correct",
    "corridor", "cost", "costume", "cottage", "cotton", "couch", "cough", "could", "council", "counsel", "count",
    "counter", "country", "county", "couple", "courage", "course", "court", "cousin", "cover", "coverage", "crack",
    "craft", "crash", "crater", "crawl", "crazy", "cream", "create", "creation", "creative", "creature", "credit",
    "creek", "creep", "crew", "cricket", "crime", "criminal", "crisis", "criteria", "critic", "critical", "criticism",
    "crop", "cross", "crowd", "crowded", "crown", "crucial", "crude", "cruel", "cruise", "crush", "crust",
    "crystal", "cube", "cue", "cultural", "culture", "cupboard", "curious", "current", "curtain", "curve", "cushion",
    "custom", "customer", "cycle",

    # D
    "daily", "dairy", "damage", "dance", "danger", "dangerous", "dare", "dark", "darkness", "data", "database",
    "date", "daughter", "dawn", "dead", "deal", "dealer", "dear", "death", "debate", "debris", "debt",
    "decade", "decay", "decent", "decide", "decision", "deck", "declare", "decline", "decorate", "decrease", "dedicate",
    "deem", "deep", "defeat", "defend", "defense", "deficit", "define", "definite", "degree", "delay", "delegate",
    "delete", "deliberate", "delicate", "delight", "deliver", "delivery", "demand", "democracy", "democrat", "demonstrate",
    "denial", "dense", "density", "dental", "deny", "depart", "department", "depend", "dependent", "depict", "deploy",
    "deposit", "depth", "deputy", "derive", "descend", "describe", "description", "desert", "deserve", "design",
    "designer", "desire", "desk", "despair", "despite", "destroy", "detail", "detailed", "detect", "detective", "determine",
    "develop", "developer", "development", "device", "devote", "dialogue", "diamond", "diary", "diet", "differ",
    "difference", "different", "difficult", "difficulty", "digest", "digital", "dignity", "dilemma", "dimension", "dinner",
    "diplomat", "direct", "direction", "director", "directory", "dirt", "dirty", "disabled", "disagree", "disappear",
    "disaster", "disc", "discipline", "disclose", "discount", "discover", "discovery", "discuss", "discussion", "disease",
    "dish", "disk", "dismiss", "disorder", "display", "dispute", "distance", "distant", "distinct", "distort", "distribute",
    "district", "disturb", "dive", "diverse", "divide", "divine", "division", "divorce", "doctor", "document", "dollar",
    "domain", "domestic", "dominant", "dominate", "donate", "door", "dose", "double", "doubt", "dough", "down",
    "draft", "dragon", "drain", "drama", "dramatic", "draw", "drawer", "drawing", "dream", "dress", "drift",
    "drill", "drink", "drive", "driver", "drop", "drown", "drug", "drum", "drunk", "duck", "dump",
    "dune", "duration", "during", "dust", "duty",

    # E
    "eager", "eagle", "early", "earn", "earnings", "earth", "ease", "easily", "east", "eastern", "easy",
    "echo", "ecology", "economic", "economics", "economy", "edge", "edit", "edition", "editor", "educate", "education",
    "effect", "effective", "efficiency", "efficient", "effort", "eight", "either", "elaborate", "elder", "elderly", "elect",
    "election", "electric", "electrical", "electricity", "electronic", "elegant", "element", "elementary", "elevator", "eleven", "elite",
    "else", "elsewhere", "email", "embassy", "embrace", "emerge", "emergency", "emission", "emotion", "emotional", "emphasis",
    "emphasize", "empire", "employ", "employee", "employer", "employment", "empty", "enable", "enact", "encounter", "encourage",
    "endless", "endorse", "endure", "enemy", "energy", "enforce", "engage", "engine", "engineer", "engineering", "enhance",
    "enjoy", "enormous", "enough", "enroll", "ensure", "enter", "enterprise", "entertain", "enthusiasm", "entire", "entirely",
    "entitle", "entity", "entrance", "entry", "envelope", "environment", "envy", "epidemic", "episode", "epoch", "equal",
    "equation", "equip", "equipment", "equity", "equivalent", "error", "escape", "especially", "essay", "essential", "establish",
    "estate", "estimate", "eternal", "ethics", "ethnic", "evacuate", "evaluate", "even", "evening", "event", "eventually",
    "every", "everybody", "everyday", "everyone", "everything", "everywhere", "evidence", "evident", "evil", "evolution", "evolve",
    "exact", "exactly", "examine", "example", "exceed", "excellent", "except", "exception", "excess", "exchange", "excited",
    "excitement", "exciting", "exclude", "exclusive", "excuse", "execute", "executive", "exempt", "exercise", "exhaust", "exhibit",
    "exhibition", "exist", "existence", "exit", "exotic", "expand", "expansion", "expect", "expectation", "expense", "expensive",
    "experience", "experiment", "expert", "expertise", "explain", "explanation", "explode", "exploit", "explore", "explosion", "export",
    "expose", "exposure", "express", "expression", "extend", "extension", "extensive", "extent", "external", "extra", "extraordinary",
    "extreme", "extremely", "eyebrow",

    # F
    "fabric", "fabulous", "face", "facility", "fact", "factor", "factory", "faculty", "fade", "fail", "failure",
    "faint", "fair", "fairly", "faith", "faithful", "fall", "false", "fame", "familiar", "family", "famous",
    "fancy", "fantasy", "fare", "farm", "farmer", "fashion", "fast", "fatal", "fate", "father", "fault",
    "favor", "favorite", "fear", "feather", "feature", "federal", "feed", "feedback", "feel", "feeling", "fellow",
    "female", "fence", "ferry", "festival", "fever", "fiber", "fiction", "field", "fierce", "fiesta", "fight",
    "fighter", "figure", "file", "fill", "film", "filter", "final", "finally", "finance", "financial", "find",
    "fine", "finger", "finish", "fire", "firm", "first", "fiscal", "fish", "fist", "fitness", "flag",
    "flame", "flash", "flat", "flavor", "flee", "fleet", "flesh", "flight", "float", "flock", "flood",
    "floor", "flour", "flow", "flower", "fluid", "flush", "flyer", "focus", "folk", "follow", "fond",
    "food", "fool", "foolish", "foot", "footage", "football", "force", "forecast", "foreign", "forest", "forever",
    "forget", "forgive", "fork", "form", "formal", "format", "formation", "former", "formula", "forth", "fortune",
    "forward", "fossil", "foster", "found", "foundation", "fountain", "fraction", "fragment", "frame", "framework", "frankly",
    "fraud", "free", "freedom", "freeway", "freeze", "freezer", "freight", "frequency", "frequent", "fresh", "friend",
    "friendly", "friendship", "frighten", "frog", "from", "front", "frontier", "frost", "fruit", "frustrate", "fuel",
    "full", "fully", "fund", "fundamental", "funding", "funeral", "funny", "furnish", "furniture", "further", "future",

    # G
    "gain", "galaxy", "gallery", "game", "gang", "garage", "garbage", "garden", "garlic", "gasoline", "gate",
    "gather", "gauge", "gear", "gender", "gene", "general", "generally", "generate", "generation", "generator", "generic",
    "generous", "genius", "genre", "gentle", "gentleman", "genuine", "geography", "gesture", "ghost", "giant", "gift",
    "gifted", "giggle", "ginger", "girl", "girlfriend", "give", "glad", "glance", "glass", "glimpse", "global",
    "globe", "gloom", "glory", "glove", "glow", "glue", "goal", "goat", "gold", "golden", "golf",
    "good", "goodness", "goods", "gorgeous", "gospel", "govern", "government", "governor", "grab", "grace", "grade",
    "gradual", "graduate", "grain", "grand", "grandchild", "grandfather", "grandmother", "grant", "grape", "graphic", "grasp",
    "grass", "grateful", "grave", "gravity", "gray", "great", "greatly", "green", "greet", "grief", "grill",
    "grim", "grin", "grip", "grocery", "gross", "ground", "group", "grow", "growth", "guarantee", "guard",
    "guess", "guest", "guidance", "guide", "guideline", "guilt", "guilty", "guitar", "gulf", "gutter",

    # H
    "habit", "habitat", "hair", "half", "hall", "hallway", "halt", "hand", "handful", "handle", "handsome",
    "hang", "happen", "happily", "happiness", "happy", "harbor", "hard", "hardly", "hardship", "hardware", "harm",
    "harmony", "harsh", "harvest", "hate", "haunt", "hazard", "head", "headache", "headline", "heal", "health",
    "healthy", "hear", "hearing", "heart", "heat", "heaven", "heavy", "hedge", "heel", "height", "helicopter",
    "hell", "hello", "helmet", "help", "helpful", "hence", "herb", "here", "heritage", "hero", "heroic",
    "hesitate", "hidden", "hide", "high", "highlight", "highway", "hill", "hint", "hire", "historic", "historical",
    "history", "hobby", "hockey", "hold", "holder", "hole", "holiday", "holy", "home", "homeless", "homework",
    "honest", "honesty", "honey", "honor", "hook", "hope", "horizon", "hormone", "horn", "horrible", "horror",
    "horse", "hospital", "host", "hostage", "hostile", "hotel", "hour", "house", "household", "housing", "hover",
    "however", "huge", "human", "humanity", "humble", "humor", "hundred", "hunger", "hungry", "hunt", "hunter",
    "hurry", "hurt", "husband", "hydrogen",

    # I
    "icon", "idea", "ideal", "identical", "identify", "identity", "ideology", "ignore", "illness", "illusion", "illustrate",
    "image", "imagination", "imagine", "immediate", "immediately", "immense", "immigrant", "immune", "impact", "impatient",
    "implement", "implication", "imply", "import", "importance", "important", "impose", "impossible", "impress", "impression",
    "impressive", "improve", "improvement", "impulse", "incentive", "incident", "include", "including", "income", "incorporate",
    "increase", "incredible", "incur", "indeed", "independence", "independent", "index", "indicate", "indicator", "indictment",
    "individual", "indoor", "induce", "industrial", "industry", "inevitable", "infant", "infect", "infection", "inflation",
    "influence", "influential", "inform", "information", "infrastructure", "ingredient", "inherit", "initial", "initially",
    "initiate", "initiative", "injury", "inmate", "inner", "innocent", "innovation", "input", "inquiry", "insect", "insert",
    "inside", "insight", "insist", "inspect", "inspector", "inspire", "install", "instance", "instant", "instead", "instinct",
    "institute", "institution", "instruct", "instruction", "instructor", "instrument", "insurance", "insult", "intact", "integrate",
    "integrity", "intellectual", "intelligence", "intend", "intense", "intensity", "intent", "intention", "interact", "interest",
    "interested", "interesting", "interior", "internal", "international", "internet", "interpret", "interrupt", "interval",
    "intervention", "interview", "intimate", "into", "introduce", "introduction", "invade", "invasion", "invent", "invest",
    "investigate", "investigation", "investment", "investor", "invite", "invoke", "involve", "involved", "iron", "irony",
    "island", "isolate", "issue", "item", "itself",

    # J
    "jacket", "jail", "jazz", "jealous", "jeans", "jelly", "jeopardy", "jewelry", "job", "join", "joint",
    "joke", "journal", "journalist", "journey", "joy", "judge", "judgment", "juice", "juicy", "jump", "jungle",
    "junior", "jurisdiction", "juror", "jury", "just", "justice", "justify",

    # K
    "keen", "keep", "keeper", "kettle", "keyboard", "kick", "kidnap", "kidney", "kill", "killer", "kind",
    "king", "kingdom", "kiss", "kitchen", "kite", "kitten", "knee", "kneel", "knife", "knight", "knit",
    "knock", "knot", "know", "knowledge", "known",

    # L
    "label", "labor", "laboratory", "lack", "ladder", "lady", "lake", "lamp", "land", "landing", "landmark",
    "landscape", "lane", "language", "lantern", "large", "largely", "laser", "last", "late", "lately", "later",
    "latter", "laugh", "laughter", "launch", "laundry", "lawmaker", "lawn", "lawyer", "layer", "lead", "leader",
    "leadership", "leaf", "league", "leak", "lean", "leap", "learn", "learning", "least", "leather", "leave",
    "lecture", "legacy", "legal", "legend", "legislation", "legitimate", "lemon", "length", "lens", "lesson",
    "letter", "level", "lever", "liability", "liable", "liberal", "liberty", "library", "license", "life",
    "lifestyle", "lifetime", "lift", "light", "lighting", "like", "likely", "limit", "limitation", "limited", "line",
    "linear", "linger", "link", "lion", "liquid", "list", "listen", "listener", "literary", "literature", "little",
    "live", "lively", "liver", "load", "loan", "lobby", "local", "locate", "location", "lock", "lodge",
    "logic", "logical", "lonely", "long", "look", "loop", "loose", "lose", "loss", "lost", "lottery",
    "loud", "lounge", "love", "lovely", "lover", "lower", "loyal", "loyalty", "luck", "lucky", "lunch",
    "lung", "luxury", "lyric",

    # M
    "machine", "machinery", "magazine", "magic", "magical", "magnet", "magnificent", "mail", "main", "mainly",
    "maintain", "maintenance", "major", "majority", "maker", "makeup", "male", "manage", "management", "manager",
    "mandate", "manner", "mansion", "manual", "manufacture", "many", "maple", "marble", "margin", "marine",
    "mark", "market", "marketing", "marriage", "married", "marry", "mask", "mass", "massive", "master",
    "match", "mate", "material", "mathematics", "matrix", "matter", "maximum", "maybe", "mayor", "meadow",
    "meal", "mean", "meaning", "meantime", "meanwhile", "measure", "measurement", "meat", "mechanic", "mechanism",
    "medal", "media", "medical", "medication", "medicine", "medium", "meet", "meeting", "melody", "member",
    "membership", "memory", "mental", "mention", "mentor", "menu", "merchant", "mercy", "mere", "merely",
    "merger", "merit", "message", "metal", "meter", "method", "metro", "middle", "midnight", "midst",
    "might", "mighty", "military", "milk", "mill", "million", "mind", "mine", "miner", "mineral",
    "minimal", "minimize", "minimum", "minister", "ministry", "minor", "minority", "minute", "miracle", "mirror",
    "misery", "miss", "missile", "mission", "mistake", "mistress", "mixture", "mobile", "mode", "model",
    "moderate", "modern", "modest", "modify", "module", "moisture", "molecule", "moment", "momentum", "money",
    "monitor", "monkey", "monster", "month", "monthly", "monument", "mood", "moon", "moral", "more",
    "moreover", "morning", "mortality", "mortgage", "mostly", "mother", "motion", "motivate", "motivation", "motor",
    "mount", "mountain", "mouse", "mouth", "move", "movement", "movie", "muffin", "multiple", "multiply",
    "municipal", "murder", "muscle", "museum", "music", "musical", "musician", "must", "mutual", "mystery",
    "myth",

    # N
    "nail", "naive", "naked", "name", "narrative", "narrow", "nasty", "nation", "national", "native",
    "natural", "naturally", "nature", "navy", "near", "nearby", "nearly", "neat", "necessarily", "necessary",
    "necessity", "neck", "need", "needle", "negative", "negotiate", "negotiation", "neighbor", "neighborhood", "neither",
    "nerve", "nervous", "nest", "network", "neutral", "never", "nevertheless", "news", "newspaper", "next",
    "nice", "nicely", "niche", "nickel", "night", "nightmare", "nine", "nitrogen", "noble", "nobody",
    "noise", "noisy", "nominate", "nomination", "none", "nonetheless", "nonsense", "noon", "norm", "normal",
    "normally", "north", "northern", "nose", "note", "notebook", "notice", "notion", "novel", "novelist",
    "nuclear", "number", "numerous", "nurse", "nursery", "nutrient", "nutrition",

    # O
    "oak", "oasis", "object", "objective", "obligation", "oblige", "observation", "observe", "observer", "obstacle",
    "obtain", "obvious", "obviously", "occasion", "occasional", "occupation", "occupy", "occur", "ocean", "odds",
    "offender", "offense", "offensive", "offer", "office", "officer", "official", "offset", "often", "ongoing",
    "onion", "online", "only", "onset", "open", "opening", "operate", "operating", "operation", "operator",
    "opinion", "opponent", "opportunity", "oppose", "opposite", "opposition", "optimistic", "option", "orange", "orbit",
    "order", "ordinary", "organ", "organic", "organization", "organize", "orientation", "origin", "original", "originally",
    "other", "otherwise", "ought", "ounce", "ourselves", "outcome", "outdoor", "outer", "outfit", "outlet",
    "outline", "outlook", "output", "outrage", "outside", "outsider", "outstanding", "oven", "over", "overall",
    "overcome", "overlook", "overnight", "oversee", "overwhelm", "owe", "owner", "ownership", "oxygen",

    # P
    "pace", "pack", "package", "packet", "page", "pain", "painful", "paint", "painter", "painting", "pair",
    "palace", "pale", "palm", "panel", "panic", "pants", "paper", "parade", "paradise", "paragraph", "parallel",
    "parent", "parish", "park", "parking", "parliament", "part", "partial", "partially", "participant", "participate",
    "particle", "particular", "particularly", "partly", "partner", "partnership", "party", "pass", "passage", "passenger",
    "passion", "passionate", "passive", "passport", "past", "pasta", "patch", "path", "patience", "patient",
    "patrol", "patron", "pattern", "pause", "pavement", "payment", "peace", "peaceful", "peak", "peanut",
    "pearl", "peer", "penalty", "pencil", "pension", "people", "pepper", "perceive", "percentage", "perception",
    "perfect", "perfectly", "perform", "performance", "performer", "period", "permanent", "permission", "permit", "persist",
    "person", "personal", "personality", "perspective", "persuade", "petal", "petition", "petroleum", "phase", "phenomenon",
    "philosophy", "phone", "photo", "photograph", "phrase", "physical", "physician", "physics", "piano", "pick",
    "picture", "piece", "pierce", "pile", "pillow", "pilot", "pine", "pink", "pioneer", "pipe", "pipeline",
    "pistol", "pitch", "pizza", "place", "placement", "plain", "plan", "plane", "planet", "planner", "plant",
    "plastic", "plate", "platform", "play", "player", "playground", "plea", "plead", "pleasant", "please", "pleasure",
    "pledge", "plenty", "plot", "plunge", "plus", "pocket", "poem", "poet", "poetry", "point", "poison",
    "polar", "pole", "police", "policeman", "policy", "polish", "polite", "political", "politician", "politics", "poll",
    "pollution", "pond", "pool", "poor", "popular", "population", "porch", "pork", "port", "portal", "portion",
    "portrait", "portray", "pose", "position", "positive", "possess", "possession", "possibility", "possible", "possibly",
    "post", "postage", "poster", "pot", "potato", "potential", "pound", "pour", "poverty", "powder", "power",
    "powerful", "practical", "practice", "praise", "pray", "prayer", "preach", "precede", "precious", "precise",
    "predict", "prediction", "prefer", "preference", "prefix", "pregnant", "prejudice", "premise", "premium", "preparation",
    "prepare", "prescription", "presence", "present", "presentation", "preserve", "president", "press", "pressure", "prestige",
    "presume", "pretend", "pretty", "prevail", "prevent", "prevention", "previous", "previously", "price", "pride", "priest",
    "primary", "prime", "prince", "princess", "principal", "principle", "print", "printer", "prior", "priority", "prison",
    "prisoner", "privacy", "private", "privilege", "prize", "probably", "probe", "problem", "procedure", "proceed",
    "process", "processor", "produce", "producer", "product", "production", "productive", "profession", "professor", "profile",
    "profit", "profound", "program", "progress", "progressive", "prohibit", "project", "projection", "prominent", "promise",
    "promote", "promotion", "prompt", "proof", "proper", "properly", "property", "proportion", "proposal", "propose",
    "prospect", "protect", "protection", "protective", "protein", "protest", "protocol", "proud", "proudly", "prove",
    "provide", "provider", "province", "provision", "provoke", "prudent", "psychology", "public", "publication", "publicity",
    "publish", "publisher", "pulse", "pump", "punch", "punish", "pupil", "puppet", "purchase", "pure", "purple",
    "purpose", "pursue", "pursuit", "push", "puzzle",

    # Q
    "quaint", "qualify", "quality", "quantity", "quarrel", "quarter", "queen", "query", "quest", "question",
    "quick", "quickly", "quiet", "quietly", "quilt", "quit", "quite", "quota", "quote",

    # R
    "rabbit", "race", "racial", "racing", "radar", "radiation", "radical", "radio", "rage", "raid", "rail",
    "railroad", "railway", "rain", "rainbow", "raise", "rally", "ranch", "random", "range", "rank", "rapid",
    "rare", "rarely", "rate", "rather", "ratio", "rational", "raw", "reach", "react", "reaction", "read",
    "reader", "readily", "ready", "real", "realistic", "reality", "realize", "really", "realm", "rear", "reason",
    "reasonable", "rebel", "rebellion", "recall", "receipt", "receive", "receiver", "recent", "recently", "reception",
    "recipe", "recognition", "recognize", "recommend", "record", "recover", "recovery", "recruit", "recycle", "reduce",
    "reduction", "refer", "reference", "reflect", "reflection", "reform", "refuge", "refugee", "refusal", "refuse",
    "regard", "regarding", "regardless", "regime", "region", "regional", "register", "regret", "regular", "regularly",
    "regulate", "regulation", "reinforce", "reject", "relate", "relation", "relationship", "relative", "relax", "release",
    "relevant", "reliable", "relief", "relieve", "religion", "religious", "rely", "remain", "remainder", "remaining",
    "remark", "remarkable", "remedy", "remember", "remind", "reminder", "remote", "removal", "remove", "render",
    "renew", "rent", "rental", "repair", "repeat", "repeatedly", "replace", "reply", "report", "reporter", "represent",
    "representative", "republic", "reputation", "request", "require", "requirement", "rescue", "research", "researcher",
    "resemble", "reservation", "reserve", "reservoir", "residence", "resident", "residential", "resign", "resist", "resistance",
    "resolution", "resolve", "resort", "resource", "respect", "respective", "respond", "response", "responsibility", "responsible",
    "rest", "restaurant", "restore", "restrict", "restriction", "result", "resume", "retail", "retain", "retire",
    "retirement", "retreat", "return", "reveal", "revelation", "revenge", "revenue", "reverse", "review", "reviewer",
    "revise", "revision", "revive", "revolution", "reward", "rhythm", "ribbon", "rice", "rich", "ride", "rider",
    "ridge", "rifle", "right", "rigid", "ring", "riot", "ripe", "ripple", "rise", "risk", "risky",
    "ritual", "rival", "river", "road", "roast", "robot", "robust", "rock", "rocket", "role", "roll",
    "romance", "romantic", "roof", "room", "root", "rope", "rose", "rough", "roughly", "round", "route",
    "routine", "rover", "royal", "rubber", "ruin", "rule", "ruler", "rumor", "runner", "running", "rural",
    "rush", "rust",

    # S
    "sack", "sacred", "sacrifice", "sad", "saddle", "safe", "safely", "safety", "sail", "sailor", "saint",
    "sake", "salad", "salary", "sale", "salmon", "salt", "salty", "salute", "sample", "sanction", "sand",
    "sandwich", "satellite", "satisfaction", "satisfy", "sauce", "save", "saving", "scale", "scan", "scandal",
    "scare", "scarce", "scared", "scarf", "scatter", "scenario", "scene", "scenery", "scent", "schedule", "scheme",
    "scholar", "scholarship", "school", "science", "scientific", "scientist", "scope", "score", "scout", "scramble",
    "scrap", "scratch", "scream", "screen", "screw", "script", "sculpture", "seal", "search", "season", "seat",
    "second", "secret", "secretary", "section", "sector", "secure", "security", "seed", "seek", "seeker", "seem",
    "segment", "seize", "seldom", "select", "selection", "self", "seller", "semester", "semiconductor", "seminar",
    "senate", "senator", "send", "senior", "sensation", "sense", "sensible", "sensitive", "sensor", "sentence",
    "sentiment", "separate", "sequence", "series", "serious", "seriously", "servant", "serve", "service", "session",
    "settle", "settlement", "seven", "several", "severe", "sew", "shade", "shadow", "shaft", "shake", "shall",
    "shallow", "shame", "shape", "share", "shareholder", "shark", "sharp", "shatter", "sheep", "sheet", "shelf",
    "shell", "shelter", "shift", "shine", "ship", "shirt", "shock", "shoe", "shoot", "shop", "shopping",
    "shore", "short", "shortage", "shortly", "shot", "shoulder", "shout", "show", "shower", "shrink", "shrug",
    "shut", "shuttle", "sick", "side", "sidewalk", "sigh", "sight", "sign", "signal", "signature", "significance",
    "significant", "silent", "silicon", "silk", "silly", "silver", "similar", "similarity", "simple", "simplify",
    "simply", "simulate", "sin", "since", "sincere", "sing", "singer", "single", "sink", "sister", "site",
    "situation", "six", "sixth", "size", "skate", "skeleton", "sketch", "ski", "skill", "skilled", "skin",
    "skirt", "skull", "sky", "slam", "slap", "slate", "slave", "slavery", "sleep", "sleeve", "slice",
    "slide", "slight", "slightly", "slip", "slogan", "slope", "slot", "slow", "slowly", "small", "smart",
    "smash", "smell", "smile", "smoke", "smooth", "snake", "snap", "snack", "snow", "soap", "soar",
    "soccer", "social", "society", "sock", "socket", "sodium", "sofa", "soft", "software", "soil", "solar",
    "soldier", "sole", "solely", "solid", "solitary", "solo", "solution", "solve", "some", "somebody", "somehow",
    "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "son", "song", "soon", "sophisticated",
    "sore", "sorrow", "sorry", "sort", "soul", "sound", "soup", "source", "south", "southern", "space",
    "spare", "spark", "speak", "speaker", "special", "specialist", "species", "specific", "specify", "specimen",
    "spectacle", "spectacular", "spectator", "spectrum", "speculate", "speech", "speed", "spell", "spend", "spending",
    "sphere", "spice", "spider", "spill", "spin", "spine", "spirit", "spiritual", "spite", "splash", "split",
    "spoil", "spoke", "spoken", "sponsor", "spoon", "sport", "spot", "spouse", "spray", "spread", "spring",
    "sprint", "spur", "squad", "square", "squeeze", "stability", "stable", "stack", "stadium", "staff", "stage",
    "stain", "stair", "stake", "stale", "stall", "stamp", "stand", "standard", "standing", "star", "stare",
    "start", "starter", "starve", "state", "statement", "station", "statistic", "status", "statute", "stay",
    "steady", "steak", "steal", "steam", "steel", "steep", "steer", "stem", "step", "stick", "sticker",
    "stiff", "still", "stimulate", "stimulus", "stir", "stock", "stomach", "stone", "stool", "stop", "storage",
    "store", "storm", "story", "stove", "straight", "strain", "strand", "strange", "stranger", "strap", "strategic",
    "strategy", "straw", "strawberry", "stream", "street", "strength", "strengthen", "stress", "stretch", "strict",
    "strike", "string", "strip", "stroke", "strong", "strongly", "structure", "struggle", "student", "studio",
    "study", "stuff", "stumble", "stun", "stunning", "style", "subject", "submit", "subsequent", "subsidy", "substance",
    "substantial", "substitute", "subtle", "suburb", "succeed", "success", "successful", "such", "sudden", "suddenly",
    "suffer", "sufficient", "sugar", "suggest", "suggestion", "suit", "suitable", "suite", "sum", "summary",
    "summer", "summit", "sun", "sunlight", "sunny", "super", "superb", "superior", "supermarket", "supper", "supplement",
    "supply", "support", "supporter", "suppose", "supreme", "sure", "surely", "surface", "surge", "surgeon", "surgery",
    "surplus", "surprise", "surrender", "surround", "survey", "survival", "survive", "survivor", "suspect", "suspend",
    "suspicion", "sustain", "swallow", "swan", "swear", "sweat", "sweater", "sweep", "sweet", "swell", "swim",
    "swimming", "swing", "switch", "sword", "symbol", "sympathy", "symptom", "syndrome", "system",

    # T
    "table", "tablet", "tackle", "tactic", "tactical", "tail", "talent", "talk", "tall", "tank", "tap",
    "tape", "target", "task", "taste", "tasty", "tax", "taxpayer", "tea", "teach", "teacher", "teaching",
    "team", "tear", "teaspoon", "technical", "technique", "technology", "teen", "teenager", "telephone", "telescope",
    "television", "tell", "temper", "temperature", "temple", "temporary", "tempt", "tenant", "tend", "tendency",
    "tender", "tennis", "tension", "tent", "term", "terminal", "terms", "terrible", "territory", "terror",
    "test", "testify", "testimony", "text", "textbook", "texture", "thank", "thanks", "theater", "theme",
    "theory", "therapy", "there", "thereafter", "thereby", "therefore", "thick", "thief", "thigh", "thin",
    "thing", "think", "thinking", "third", "thirst", "thirsty", "thirteen", "thirty", "thorough", "though",
    "thought", "thousand", "thread", "threat", "threaten", "three", "threshold", "thrive", "throat", "throne",
    "through", "throughout", "throw", "thrust", "thumb", "thunder", "ticket", "tide", "tidy", "tie", "tiger",
    "tight", "tightly", "tile", "timber", "time", "timeline", "timely", "timer", "timing", "tin", "tiny",
    "tip", "tire", "tired", "tissue", "title", "toast", "tobacco", "today", "toe", "together", "token",
    "tolerance", "tolerate", "toll", "tomato", "tomb", "tomorrow", "tone", "tongue", "tonight", "tool", "tooth",
    "topic", "torch", "total", "totally", "touch", "tough", "tour", "tourism", "tourist", "tournament", "toward",
    "towel", "tower", "town", "toxic", "trace", "track", "trade", "trader", "tradition", "traditional", "traffic",
    "tragedy", "trail", "train", "trainer", "training", "trait", "traitor", "tram", "transaction", "transcript",
    "transfer", "transform", "transition", "translate", "translation", "transmission", "transmit", "transport", "trap",
    "trash", "trauma", "travel", "traveler", "tray", "treasure", "treat", "treatment", "treaty", "tree", "tremendous",
    "trend", "trial", "triangle", "tribe", "trick", "trigger", "trim", "trip", "triumph", "troop", "trophy",
    "tropical", "trouble", "truck", "true", "truly", "trunk", "trust", "truth", "tube", "tuck", "tuition",
    "tumor", "tune", "tunnel", "turkey", "turn", "turnover", "tutor", "twelve", "twenty", "twice", "twin",
    "twist", "two", "type", "typical", "typically", "tyre",

    # U
    "ugly", "ultimate", "ultimately", "umbrella", "unable", "unaware", "uncle", "uncomfortable", "unconscious", "under",
    "undergo", "undergraduate", "underlying", "undermine", "understand", "understanding", "undertake", "unemployed", "unexpected",
    "unfair", "unfold", "unfortunate", "unhappy", "uniform", "union", "unique", "unit", "unite", "unity", "universal",
    "universe", "university", "unknown", "unless", "unlike", "unlikely", "until", "unusual", "update", "upon", "upper",
    "upset", "urban", "urge", "urgent", "user", "usual", "usually", "utility", "utilize", "utter",

    # V
    "vacation", "vacuum", "vague", "vain", "valid", "validity", "valley", "valuable", "value", "valve", "vanish",
    "vapor", "variable", "variation", "variety", "various", "vary", "vast", "vault", "vegetable", "vehicle", "veil",
    "vein", "velocity", "venture", "venue", "verb", "verdict", "verge", "verify", "version", "versus", "vertical",
    "very", "vessel", "veteran", "viable", "vibe", "vibrant", "victim", "victory", "video", "view", "viewer",
    "vigor", "village", "villain", "vine", "violate", "violation", "violence", "violent", "violet", "violin",
    "virtual", "virtue", "virus", "visible", "vision", "visit", "visitor", "visual", "vital", "vitamin", "vivid",
    "vocal", "voice", "volume", "voluntary", "volunteer", "vote", "voter", "vow", "voyage",

    # W
    "wage", "wagon", "waist", "wait", "waiter", "wake", "walk", "wall", "wallet", "wander", "want", "war",
    "warm", "warmth", "warn", "warning", "warrant", "warrior", "wash", "waste", "watch", "water", "wave",
    "weak", "weaken", "weakness", "wealth", "wealthy", "weapon", "wear", "weather", "weave", "web", "website",
    "wedding", "weed", "week", "weekend", "weekly", "weep", "weigh", "weight", "weird", "welcome", "welfare",
    "well", "west", "western", "whale", "what", "whatever", "wheat", "wheel", "when", "whenever", "where",
    "whereas", "wherever", "whether", "which", "while", "whip", "whisper", "whistle", "white", "whole", "wholly",
    "whom", "whose", "wide", "widely", "widespread", "widow", "width", "wife", "wild", "wilderness", "wildlife",
    "will", "willing", "willingness", "wind", "window", "wine", "wing", "winner", "winter", "wipe", "wire",
    "wisdom", "wise", "wish", "with", "withdraw", "withdrawal", "within", "without", "witness", "wolf", "woman",
    "wonder", "wonderful", "wood", "wooden", "wool", "word", "work", "worker", "workforce", "workplace", "workshop",
    "world", "worldwide", "worm", "worry", "worse", "worth", "worthwhile", "worthy", "wound", "wrap", "wreck",
    "wrist", "write", "writer", "writing", "wrong",

    # Y & Z
    "yard", "yarn", "yawn", "year", "yell", "yellow", "yesterday", "yield", "yoga", "yogurt", "young",
    "youngster", "your", "yours", "yourself", "youth", "zeal", "zebra", "zenith", "zero", "zest", "zinc",
    "zone", "zoom"
]

def generate_word_list():
    words = set()
    
    # Common short words (crucial for Boggle 3-4 letter combinations)
    short_words = [
        "ace", "act", "add", "ado", "aft", "age", "ago", "aid", "aim", "air", "ale", "all", "amp", "and", "ant",
        "any", "ape", "apt", "arc", "are", "ark", "arm", "art", "ash", "ask", "asp", "ate", "awe", "axe", "bad",
        "bag", "ban", "bar", "bat", "bay", "bed", "bee", "beg", "bet", "bid", "big", "bin", "bit", "boa", "bob",
        "bog", "boo", "bop", "bow", "box", "boy", "bud", "bug", "bum", "bun", "bus", "but", "buy", "bye", "cab",
        "cad", "cam", "can", "cap", "car", "cat", "caw", "cob", "cod", "cog", "con", "coo", "cop", "cot", "cow",
        "cry", "cub", "cud", "cue", "cup", "cur", "cut", "dab", "dad", "dam", "day", "den", "dew", "did", "die",
        "dig", "dim", "din", "dip", "doe", "dog", "don", "dot", "dry", "dub", "due", "dug", "dye", "ear", "eat",
        "ebb", "eel", "egg", "ego", "elf", "elk", "elm", "end", "era", "eve", "eye", "fan", "far", "fat", "fed",
        "fee", "few", "fib", "fig", "fin", "fit", "fix", "fly", "foe", "fog", "for", "fox", "fry", "fun", "fur",
        "gab", "gag", "gap", "gas", "gel", "gem", "get", "gin", "gnu", "gob", "god", "got", "gum", "gun", "gut",
        "guy", "gym", "had", "ham", "has", "hat", "hay", "hem", "hen", "her", "hew", "hex", "hey", "hid", "him",
        "hip", "his", "hit", "hob", "hog", "hop", "hot", "how", "hub", "hue", "hug", "hum", "hut", "ice", "icy",
        "ill", "imp", "ink", "inn", "ion", "ire", "irk", "its", "ivy", "jab", "jag", "jam", "jar", "jaw", "jay",
        "jet", "jig", "job", "jog", "jot", "joy", "jug", "jut", "keg", "ken", "key", "kid", "kin", "kip", "kit",
        "lab", "lad", "lag", "lap", "law", "lax", "lay", "led", "leg", "let", "lid", "lie", "lip", "lit", "lob",
        "log", "lot", "low", "lug", "lye", "mad", "man", "map", "mar", "mat", "maw", "may", "men", "met", "mew",
        "mid", "mix", "mob", "mop", "mow", "mud", "mug", "mum", "nab", "nag", "nap", "nay", "net", "new", "nib",
        "nil", "nip", "nit", "nod", "nor", "not", "now", "nun", "nut", "oaf", "oak", "oar", "oat", "odd", "ode",
        "off", "oft", "oil", "old", "one", "opt", "orb", "ore", "our", "out", "owe", "owl", "own", "pad", "pal",
        "pan", "par", "pat", "paw", "pay", "pea", "peg", "pen", "pep", "per", "pet", "pew", "pie", "pig", "pin",
        "pip", "pit", "ply", "pod", "pop", "pot", "pro", "pry", "pub", "pug", "pun", "pup", "pus", "put", "rag",
        "ram", "ran", "rap", "rat", "raw", "ray", "red", "rib", "rid", "rig", "rim", "rip", "rob", "rod", "roe",
        "rot", "row", "rub", "rug", "rum", "run", "rut", "rye", "sad", "sag", "sap", "sat", "saw", "say", "sea",
        "see", "set", "sew", "she", "shy", "sin", "sip", "sir", "sit", "six", "ski", "sky", "sly", "sob", "sod",
        "son", "sop", "sow", "soy", "spa", "spy", "sub", "sue", "sum", "sun", "tab", "tag", "tan", "tap", "tar",
        "tax", "tea", "tee", "ten", "the", "thy", "tie", "tin", "tip", "toe", "ton", "too", "top", "tow", "toy",
        "try", "tub", "tug", "two", "urn", "use", "van", "vat", "vet", "vex", "via", "vow", "wad", "wag", "war",
        "was", "wax", "way", "web", "wed", "wee", "wet", "who", "why", "wig", "win", "wit", "woe", "won", "woo",
        "yak", "yam", "yap", "yaw", "yea", "yen", "yep", "yes", "yet", "yew", "yin", "yip", "you", "zap", "zed",
        "zen", "zig", "zip", "zoo"
    ]

    for w in short_words:
        if len(w) >= 3:
            words.add(w.lower())

    for base in BASE_WORDS:
        b = base.lower()
        if len(b) >= 3:
            words.add(b)
            # Automatic inflections
            # Plural / 3rd person singular (-s, -es)
            if b.endswith(('s', 'sh', 'ch', 'x', 'z')):
                words.add(b + "es")
            elif b.endswith('y') and len(b) > 2 and b[-2] not in "aeiou":
                words.add(b[:-1] + "ies")
            else:
                words.add(b + "s")

            # Past tense / participle (-ed, -d)
            if b.endswith('e'):
                words.add(b + "d")
                words.add(b + "r")
                words.add(b[:-1] + "ing")
            elif b.endswith('y') and len(b) > 2 and b[-2] not in "aeiou":
                words.add(b[:-1] + "ied")
                words.add(b + "ing")
            else:
                words.add(b + "ed")
                words.add(b + "er")
                words.add(b + "ing")

            # Adverbs (-ly)
            words.add(b + "ly")

    return sorted(list(words))

if __name__ == "__main__":
    word_list = generate_word_list()
    out_path = os.path.join(os.path.dirname(__file__), "dictionary.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        for w in word_list:
            if len(w) >= 3 and w.isalpha():
                f.write(w + "\n")
    print(f"Generated {len(word_list)} words in {out_path}")

