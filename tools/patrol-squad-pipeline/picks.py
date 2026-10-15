# Best-cut selection for every Patrol Squad asset.
# Each entry maps an output name to the source cut chosen after comparing every
# duplicate across the master sheet ("master_###") and the per-character sheets.
# Rule applied: complete silhouette > no neighbour fragments > on-model identity
# > not clipped by the sheet edge > higher native resolution.
# "split:<cut>:<left|right>" splits a merged component at its widest alpha gap.

PICKS = {
  "coach-control": {
    "poses": {
      "thumbs-up": "coach_000",          # 164px, per-character sheet (sharpest)
      "wave": "master_001",
      "point": "master_002",
      "explain": "master_003",
      "cheer": "master_005",
      "thinking": "master_007",
      "power-stance": "coach_001",       # full feet kept (small-sheet copy is cropped)
    },
    "expressions": {
      "smile": "coach_002", "calm-smile": "coach_003", "grin": "coach_004",
      "talk": "coach_005", "laugh": "coach_006", "talk-wide": "coach_007",
      "skeptical": "master_013", "headset-whistle": "coach_016",
    },
    "rig": {
      "torso": "master_026", "torso-alt": "master_024", "jacket": "coach_012",
      "vest-belt": "coach_014", "torso-side": "coach_015",
      "legs-standing": "master_028", "legs-wide": "master_027",
      "leg-a": "master_029", "leg-b": "master_030", "shin-shoe": "master_032",
      "leg-bent": "coach_030", "leg-c": "coach_032", "leg-d": "coach_034", "leg-boot": "coach_028",
      "arm": "master_031", "forearm-hand": "master_038", "forearm-hand-b": "coach_018", "forearm-glove": "coach_019",
      "glove": "master_033", "shoe-a": "master_036", "shoe-b": "master_037", "hair": "master_021",
      "hand-open": "coach_023", "hand-thumb": "coach_025", "hand-point": "coach_029", "hand-fist": "coach_026",
      "hand-a": "master_035", "hand-b": "master_039", "hand-c": "master_040", "hand-d": "master_041",
      "hand-watch": "master_042", "hand-e": "coach_011", "hand-f": "coach_017", "hand-g": "coach_022", "hand-h": "coach_027",
      "mouth": "coach_020",
    },
    "accessories": {
      "headset": "coach_013", "clipboard": "coach_033", "clipboard-angled": "coach_031",
      "whistle": "rows:coach_016:129", "whistle-small": "master_025", "lanyard-ring": "coach_035", "whistle-b": "master_034",
    },
  },
  "captain-calm": {
    "poses": {
      "idle": "calm_a_001", "open-palms": "calm_a_002", "breathing": "calm_a_005",
      "heart-hands": "master_049", "meditate-eyes-closed": "master_051", "meditate": "calm_a_003",
      "celebrate": "calm_a_004", "crouch-ready": "calm_a_000",
    },
    "expressions": {
      "neutral": "master_044", "smile": "master_048", "soft": "master_050",
      "eyes-closed": "master_047", "gentle": "master_052", "happy": "master_054",
      "portrait-smile": "calm_a_006", "portrait-soft": "calm_a_007", "portrait-glance": "calm_a_015",
    },
    "rig": {
      "cap": "split:master_056:left", "hair": "split:master_056:right",
      "torso": "calm_a_013", "vest": "calm_a_014", "sleeve": "calm_a_016",
      "arm-a": "calm_a_018", "arm-b": "calm_a_019", "arm-c": "calm_a_020", "arm-d": "calm_a_021",
      "arm-bent-hand": "master_066", "arm-bent": "master_060", "arm-upper": "master_061",
      "leg-a": "calm_a_028", "leg-b": "calm_a_029", "leg-c": "calm_a_030", "legs-pair": "calm_a_032",
      "shin-shoe-a": "calm_a_034", "shin-shoe-b": "calm_a_035", "shoe-a": "calm_a_037", "shoe-b": "calm_a_039",
      "hand-a": "calm_a_017", "hand-b": "calm_a_022", "hand-c": "calm_a_023", "hand-d": "calm_a_024",
      "hand-e": "calm_a_025", "hand-f": "calm_a_026", "hand-g": "calm_a_027",
    },
    "accessories": {"compass": "master_080", "belt": "calm_a_033"},
  },
  "sergeant-pause": {
    "poses": {
      "stop-sign": "master_081", "stop-hand": "master_082", "idle": "master_087",
      "ready": "master_083", "alert": "master_084", "approve-flex": "pause_002",
      "point": "pause_003", "run": "master_085", "lookout": "master_086",
    },
    "expressions": {
      "neutral": "pause_009", "smile": "pause_007", "grin": "pause_005", "talk": "pause_008",
      "wink": "pause_006", "squint": "pause_010", "portrait": "pause_004", "portrait-smile": "pause_017",
    },
    "rig": {
      "head": "split:master_101:left", "hair": "split:master_101:right",
      "torso": "pause_011", "vest": "pause_012",
      "arm-a": "master_104", "arm-b": "master_105", "arm-c": "master_106", "arm-d": "pause_013", "arm-e": "pause_014",
      "leg-a": "pause_031", "leg-b": "pause_032", "legs-bent": "pause_030", "legs-pair": "master_123",
      "leg-c": "master_118", "leg-d": "master_119", "leg-e": "master_120", "leg-f": "master_121", "leg-g": "master_122",
      "boot-a": "pause_037", "boot-b": "pause_038", "boot-c": "pause_039", "boot-d": "master_124",
      "hand-a": "master_107", "hand-b": "master_114", "hand-c": "master_115", "hand-d": "master_116", "hand-e": "master_117",
      "hand-f": "pause_018", "hand-g": "pause_026", "hand-h": "pause_027", "hand-i": "pause_028", "hand-j": "pause_015",
      "glove": "master_126", "glove-point": "pause_040",
      "mouth-a": "master_110", "mouth-b": "master_111", "mouth-c": "master_113", "mouth-d": "pause_033", "mouth-e": "pause_034",
    },
    "accessories": {"stop-paddle": "pause_035", "stop-paddle-small": "master_099", "headset": "master_100"},
  },
  "detective-think": {
    "poses": {
      "magnifier": "master_128", "notebook": "master_129", "idle": "master_130", "thinking": "master_131",
      "wave": "master_132", "inspect": "master_133", "idea": "master_134", "discover": "master_135",
      "investigate": "master_136", "explain-book": "master_137",
    },
    "expressions": {
      "smile": "master_138", "gentle": "master_139", "glance": "master_140", "skeptical": "master_141",
      "smirk": "master_142", "neutral": "master_143", "curious": "master_144", "surprised": "master_145",
      "happy": "master_146", "sly": "master_147", "cheerful": "master_148",
    },
    "rig": {
      "hat": "master_149", "glasses": "master_150", "hair": "master_151", "torso": "master_152",
      "arm-a": "master_153", "arm-b": "master_154", "arm-c": "master_155",
      "hand-a": "master_156", "hand-b": "master_157", "hand-c": "master_158",
      "leg-a": "master_162", "leg-b": "master_163", "leg-c": "master_164",
    },
    "accessories": {"magnifier": "master_159", "notebook": "master_160", "clipboard": "master_161"},
  },
  "commander-flex": {
    "poses": {
      "idle": "master_167", "ready": "flex_000", "power-stance": "master_166", "point": "master_168",
      "recovery-bounce": "master_169", "change-direction": "master_170", "celebrate": "master_171",
      "thumbs-up-map": "flex_001",
    },
    "expressions": {
      "smile": "master_173", "grin": "master_175", "open-grin": "master_177", "happy": "master_179",
      "laugh": "master_183", "excited": "master_188", "soft": "master_191", "neutral": "master_196",
      "portrait": "flex_002", "wink": "flex_007",
    },
    "rig": {
      "cap-goggles": "master_172", "hair": "master_174", "torso": "flex_009", "vest": "flex_010",
      "arm-a": "flex_012", "arm-b": "flex_013", "arm-c": "flex_014", "arm-d": "flex_015",
      "arm-e": "master_180", "arm-f": "master_181", "arm-g": "master_182", "arm-h": "master_184",
      "leg-a": "flex_026", "leg-b": "flex_027", "leg-c": "flex_028", "leg-d": "flex_031", "leg-e": "flex_032",
      "boot-a": "flex_029", "boot-b": "flex_033", "gloves": "flex_022", "gloves-b": "master_195",
    },
    "accessories": {"map": "flex_030", "backpack": "master_198", "rope": "master_199", "carabiner-line": "master_200", "belt": "flex_035"},
  },
  "officer-focus": {
    "poses": {
      "point-clipboard": "focus_000", "binoculars": "focus_001", "binoculars-ready": "focus_002",
      "kneel-binoculars": "master_204", "point-up": "focus_005", "clipboard": "master_206",
      "walk-clipboard": "master_202", "scout": "master_209", "run-point": "master_212",
    },
    "expressions": {
      "neutral": "focus_007", "smile": "focus_009", "open-smile": "focus_008", "grin": "focus_011",
      "happy": "focus_010", "soft": "focus_012", "portrait": "focus_006", "portrait-ponytail": "focus_013",
    },
    "rig": {
      "cap": "master_214", "hair": "focus_016", "ponytail": "master_216", "torso": "focus_015", "vest": "focus_014",
      "arm-a": "focus_018", "sleeve": "focus_017", "arm-b": "master_218", "arm-c": "master_219", "arm-d": "master_220",
      "arm-e": "master_221", "arm-f": "master_222",
      "leg-a": "focus_032", "leg-b": "focus_034", "leg-c": "focus_035", "leg-d": "focus_036", "leg-e": "focus_037",
      "leg-f": "master_230", "leg-g": "master_231", "leg-h": "master_232", "leg-i": "master_233",
      "boot-a": "focus_038", "boot-b": "focus_039",
      "hand-a": "focus_020", "hand-b": "master_224", "hand-c": "master_225", "hand-d": "master_226",
      "hand-e": "master_227", "hand-f": "master_228",
    },
    "accessories": {"binoculars": "master_229", "binoculars-b": "master_234", "clipboard": "focus_033", "clipboard-small": "focus_003"},
  },
}

# Cuts examined and deliberately NOT used (reported in the manifest).
REJECTED = {
  "master_000": "Coach row pose wearing a blue cap — off-model (Coach's identity is the headset, no cap)",
  "master_004": "Coach row pose wearing a blue cap — off-model",
  "master_006": "Coach row pose wearing a blue cap — off-model",
  "master_009": "Coach row pose with cap and megaphone — off-model",
  "master_008": "Coach row pose drawn as a girl with a ponytail — not Coach Control",
  "coach_small_000": "Duplicate of coach_000 (identical cut)",
  "coach_small_001": "Duplicate of coach_001 with feet cropped",
  "calm_b_*": "Sheet calm_b is pixel-identical to calm_a; calm_a used",
  "master_045": "Lower-resolution variant of Captain Calm standing pose; calm_a_001 used",
  "master_053": "Captain Calm open-palms pose cropped at the knees on the master sheet; calm_a_002 (complete) used",
  "master_055": "Captain Calm pose carries a stray fragment from a neighbouring sprite",
  "pause_000": "Neighbouring sprite fragment attached at the left edge; clean master_082 used",
  "pause_001": "Clipped by the sheet edge and carries fragments of the row below",
  "master_088": "Lower-resolution duplicate of the pointing pose; pause_003 used",
  "master_165": "Detective Think leg merged with a pair of binoculars; cannot be separated cleanly",
  "master_215": "Officer Focus hair clipped by the sheet edge; focus_016 used",
  "master_237": "Officer Focus arm clipped by the sheet edge",
  "focus_004": "Officer Focus kneeling pose is sliced off at the knees on the per-character sheet; the complete master_204 kneel is used",
  "coach_035 (as whistle)": "Gold lanyard ring, not a whistle; kept as 'lanyard-ring'. The whistle prop is cut from the bottom of coach_016 (lanyard whistle, sharpest copy)",
  "master_130 (board/state use)": "Detective Think drawn with a monocle instead of her round glasses; extracted but never shown",
  "master_145 (state use)": "Detective Think face drawn without her glasses; extracted but never shown",
  "master_089..098": "Sergeant Pause master heads mix capped and uncapped versions with a lighter skin tone; consistent capped per-character heads used",
  "master_010..020": "Several Coach master heads drop the headset; per-character heads used (master_013 kept for its unique skeptical brow)",
}
