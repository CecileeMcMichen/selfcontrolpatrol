"""Generate the Patrol Squad character manifest.

Writes:
  game/data/patrol-squad.js                 (runtime; plain script so it also works from file://)
  game/assets/patrol-squad/manifest.json    (machine-readable documentation copy)
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hf import HF
from picks import REJECTED

GAME = 'game'
report = json.load(open('seg/asset_report.json'))
board = json.load(open('seg/board_plan.json'))

# Art-style family of each pose: 'm' = master Patrol sheet (rounder proportions),
# 'c' = per-character sheet (slimmer proportions). Sequences stay inside one family.
def family(src):
    return 'm' if src.startswith('master_') else 'c'

CHAR = {
 'coach': dict(id='coach-control', name='Coach Control', role='Team Leader and Mission Guide',
   personality='Confident, motivational, energetic, charismatic, supportive',
   identity='Royal blue and gold uniform, whistle, headset, leadership insignia',
   motionProfile='energetic', accent='#3c7bff', accent2='#ffc94e', voice=dict(pitch=1.0, rate=1.02),
   boardIdle=['thumbs-up'], boardAlt=[],
   states={
    'idle':            dict(poses=[['thumbs-up',0]], badge=['smile'], motion='breathe'),
    'attention':       dict(poses=[['point',0]], badge=['talk','smile'], motion='pop'),
    'greeting':        dict(poses=[['wave',0],['cheer',1300]], badge=['talk-wide','smile'], motion='wave', prop=['whistle','tweet']),
    'thinking':        dict(poses=[['thinking',0]], badge=['skeptical'], motion='tilt'),
    'speaking':        dict(poses=[['explain',0],['point',1100]], badge=['talk','calm-smile'], motion='talk'),
    'encouraging':     dict(poses=[['thumbs-up',0]], badge=['grin','smile'], motion='nod'),
    'coaching':        dict(poses=[['explain',0],['point',1200]], badge=['talk','calm-smile'], motion='talk', prop=['clipboard','check']),
    'retry':           dict(poses=[['thumbs-up',0]], badge=['smile','calm-smile'], motion='nod'),
    'celebrating':     dict(poses=[['cheer',0],['wave',900],['cheer',1700]], badge=['laugh','grin'], motion='jump'),
    'missionAlert':    dict(poses=[['point',0]], badge=['talk-wide','talk'], motion='pop', prop=['whistle','tweet']),
    'missionComplete': dict(poses=[['cheer',0],['wave',1000]], badge=['laugh','grin'], motion='jump'),
   },
   lines={
    'welcome':['Welcome to Patrol Headquarters! Let’s hear the briefing first.','Patrol Squad, welcome! Listen to the mission briefing.'],
    'turn':['{name}, you’re up!','Patrol Squad — {name} is on patrol!'],
    'power':['Power Talk! Speak up — calm and strong.','Use your Power Talk formula!'],
    'free':['Self-Control FREE turn! Roll again!','Bonus patrol turn — nice!'],
    'finale':['Mission complete! Great teamwork, Patrol Squad!'],
    'idle':['Patrol ready!'],
   }),
 'calm': dict(id='captain-calm', name='Captain Calm', role='Emotional Regulation Specialist',
   personality='Patient, reassuring, compassionate, composed, dependable',
   identity='Teal and silver uniform, calming compass, gentle expressions',
   motionProfile='smooth', accent='#2fc7b0', accent2='#d7f4ef', voice=dict(pitch=1.08, rate=.9),
   boardIdle=['meditate','breathing'], boardAlt=[],
   states={
    'idle':            dict(poses=[['meditate',0]], badge=['soft'], motion='breathe-slow'),
    'attention':       dict(poses=[['open-palms',0]], badge=['gentle','soft'], motion='settle'),
    'greeting':        dict(poses=[['idle',0],['open-palms',1300]], badge=['smile','soft'], motion='settle'),
    'thinking':        dict(poses=[['meditate',0]], badge=['portrait-glance'], motion='breathe-slow'),
    'speaking':        dict(poses=[['open-palms',0]], badge=['happy','soft'], motion='sway-slow'),
    'encouraging':     dict(poses=[['open-palms',0]], badge=['happy','smile'], motion='nod-slow'),
    'coaching':        dict(poses=[['meditate',0],['breathing',1100],['meditate',2400]], badge=['soft','eyes-closed'], motion='breathe-slow', prop=['compass','swing']),
    'retry':           dict(poses=[['open-palms',0]], badge=['gentle','soft'], motion='nod-slow'),
    'celebrating':     dict(poses=[['idle',0],['celebrate',700]], badge=['happy','smile'], motion='float'),
    'missionAlert':    dict(poses=[['crouch-ready',0]], badge=['gentle','soft'], motion='settle'),
    'missionComplete': dict(poses=[['celebrate',0]], badge=['happy','smile'], motion='float'),
   },
   lines={
    'plusLoss':['That’s okay. Take a breath and keep going.','Breathe in, breathe out. You’ve got this.'],
    'incorrect':['Take your time. Let’s look at the helpful answer together.','It’s okay. Breathe, learn it, and use it next time.'],
    'cue':['Notice your body. Take a slow breath.','Calm body, clear mind. What do you notice?'],
    'info':['Anger is normal. We get to choose what we do with it.','Feelings are okay. Calm choices help.'],
    'detour':['Take a breath. You’ll be back on patrol soon.','A quick reset. Calm and ready for next time.'],
    'reflection':['Nice reflection. That’s how we reset.'],
    'idle':['Calm body. Clear mind.'],
   }),
 'pause': dict(id='sergeant-pause', name='Sergeant Pause', role='Impulse Control Specialist',
   personality='Alert, disciplined, observant, protective, firm but friendly',
   identity='Orange and charcoal uniform, STOP paddle, rank insignia',
   motionProfile='crisp', accent='#ff8a2a', accent2='#2a2f38', voice=dict(pitch=.92, rate=.94),
   boardIdle=['stop-sign'], boardAlt=['lookout','ready'],
   states={
    'idle':            dict(poses=[['stop-sign',0]], badge=['neutral'], motion='hold'),
    'attention':       dict(poses=[['alert',0]], badge=['neutral','talk'], motion='snap'),
    'greeting':        dict(poses=[['ready',0]], badge=['smile','grin'], motion='snap'),
    'thinking':        dict(poses=[['idle',0],['lookout',1000]], badge=['squint','neutral'], motion='look'),
    'speaking':        dict(poses=[['ready',0]], badge=['talk','neutral'], motion='hold'),
    'encouraging':     dict(poses=[['approve-flex',0]], badge=['grin','smile'], motion='nod'),
    'coaching':        dict(poses=[['stop-hand',0],['ready',1600]], badge=['talk','smile'], motion='raise-hold', prop=['stop-paddle','raise']),
    'retry':           dict(poses=[['stop-hand',0],['lookout',1500]], badge=['talk','neutral'], motion='raise-hold', prop=['stop-paddle','raise']),
    'celebrating':     dict(poses=[['approve-flex',0]], badge=['grin','wink'], motion='pump'),
    'missionAlert':    dict(poses=[['alert',0],['stop-sign',450]], badge=['talk','neutral'], motion='raise-hold'),
    'missionComplete': dict(poses=[['approve-flex',0]], badge=['grin','wink'], motion='pump'),
   },
   lines={
    'situation':['Stop. Think. Then choose.','Freeze! Think before you act.'],
    'encounter':['Stop and notice. Then choose a calm response.','Pause first — you stay in control.'],
    'idle':['Stop. Pause. Choose.'],
   }),
 'think': dict(id='detective-think', name='Detective Think', role='Problem-Solving Specialist',
   personality='Curious, clever, analytical, creative, thoughtful',
   identity='Purple and gold detective outfit, glasses, magnifying glass, notebook',
   motionProfile='inquisitive', accent='#9b5cff', accent2='#f0c24a', voice=dict(pitch=1.15, rate=1.0),
   boardIdle=['magnifier'], boardAlt=['inspect','thinking'], neverOnBoard=['idle'],
   states={
    'idle':            dict(poses=[['magnifier',0]], badge=['smile'], motion='tilt'),
    'attention':       dict(poses=[['idea',0]], badge=['curious','smile'], motion='pop'),
    'greeting':        dict(poses=[['wave',0]], badge=['cheerful','smile'], motion='wave'),
    'thinking':        dict(poses=[['thinking',0],['inspect',1200]], badge=['curious','skeptical'], motion='tilt', prop=['magnifier','sweep']),
    'speaking':        dict(poses=[['explain-book',0]], badge=['happy','smile'], motion='talk'),
    'encouraging':     dict(poses=[['idea',0]], badge=['happy','smile'], motion='nod'),
    'coaching':        dict(poses=[['notebook',0],['explain-book',1300]], badge=['happy','gentle'], motion='talk', prop=['notebook','flip']),
    'retry':           dict(poses=[['investigate',0]], badge=['curious','smile'], motion='tilt'),
    'celebrating':     dict(poses=[['discover',0],['idea',900]], badge=['cheerful','happy'], motion='eureka'),
    'missionAlert':    dict(poses=[['magnifier',0],['inspect',1100]], badge=['curious','skeptical'], motion='tilt', prop=['magnifier','sweep']),
    'missionComplete': dict(poses=[['discover',0],['wave',900]], badge=['cheerful','happy'], motion='eureka'),
   },
   lines={
    'payoff':['What could happen next? Compare the choices.','Let’s look for clues about the best payoff.'],
    'question':['What clues can help us decide?','Read each choice like a detective.'],
    'firstTry':['Great detective work — you found it!','Clue solved on the first try!'],
    'teaching':['Compare these ideas like clues. Which one could work best in a different situation, and why?'],
    'idle':['Look for the clue.'],
   }),
 'flex': dict(id='commander-flex', name='Commander Flex', role='Flexibility and Resilience Specialist',
   personality='Adventurous, optimistic, resourceful, adaptable, resilient',
   identity='Emerald green and navy adventure uniform, goggles, mission gear',
   motionProfile='springy', accent='#3fd16b', accent2='#173a63', voice=dict(pitch=1.1, rate=1.06),
   boardIdle=['idle'], boardAlt=['point','change-direction'],
   states={
    'idle':            dict(poses=[['idle',0]], badge=['smile'], motion='spring'),
    'attention':       dict(poses=[['ready',0]], badge=['grin','smile'], motion='spring'),
    'greeting':        dict(poses=[['thumbs-up-map',0]], badge=['portrait','smile'], motion='spring'),
    'thinking':        dict(poses=[['idle',0],['point',1100]], badge=['neutral','smile'], motion='tilt', prop=['map','unfold']),
    'speaking':        dict(poses=[['point',0]], badge=['open-grin','smile'], motion='talk'),
    'encouraging':     dict(poses=[['thumbs-up-map',0]], badge=['grin','smile'], motion='spring'),
    'coaching':        dict(poses=[['change-direction',0],['recovery-bounce',1300]], badge=['open-grin','smile'], motion='spring', prop=['map','unfold']),
    'retry':           dict(poses=[['change-direction',0],['recovery-bounce',1300]], badge=['open-grin','grin'], motion='spring', prop=['map','unfold']),
    'celebrating':     dict(poses=[['recovery-bounce',0],['celebrate',600]], badge=['laugh','excited'], motion='bounce'),
    'missionAlert':    dict(poses=[['power-stance',0]], badge=['grin','smile'], motion='spring'),
    'missionComplete': dict(poses=[['celebrate',0],['power-stance',1000]], badge=['laugh','excited'], motion='bounce'),
   },
   lines={
    'retry':['New strategy! You’ve got this!','Plans can change. Look again and try once more!'],
    'recovery':['You adjusted and got it! Nice recovery!','That’s flexible thinking!'],
    'exact':['Plans change! You’ll get your exact roll soon.','Not this time — stay flexible!'],
    'charades':['Charades time! Get creative!','Act it out — be flexible and have fun!'],
    'idle':['Plans can change. You can handle it.'],
   }),
 'focus': dict(id='officer-focus', name='Officer Focus', role='Attention and Persistence Specialist',
   personality='Determined, observant, organized, reliable, attentive',
   identity='Navy and cyan officer uniform, binoculars, checklist',
   motionProfile='precise', accent='#38b6ff', accent2='#13306b', voice=dict(pitch=1.12, rate=.98),
   boardIdle=['binoculars'], boardAlt=['binoculars-ready'],
   states={
    'idle':            dict(poses=[['binoculars',0]], badge=['neutral'], motion='scan'),
    'attention':       dict(poses=[['binoculars-ready',0]], badge=['neutral','smile'], motion='snap'),
    'greeting':        dict(poses=[['point-clipboard',0]], badge=['portrait','smile'], motion='nod'),
    'thinking':        dict(poses=[['binoculars',0]], badge=['neutral','soft'], motion='scan', prop=['binoculars','scan']),
    'speaking':        dict(poses=[['point-clipboard',0]], badge=['open-smile','smile'], motion='talk'),
    'encouraging':     dict(poses=[['point-clipboard',0]], badge=['grin','smile'], motion='nod', prop=['clipboard','check']),
    'coaching':        dict(poses=[['point-clipboard',0]], badge=['open-smile','smile'], motion='nod', prop=['clipboard','check']),
    'retry':           dict(poses=[['binoculars-ready',0]], badge=['soft','smile'], motion='nod'),
    'celebrating':     dict(poses=[['point-up',0]], badge=['happy','grin'], motion='quiet-pop', prop=['clipboard','check']),
    'missionAlert':    dict(poses=[['binoculars',0],['binoculars-ready',1100]], badge=['neutral','open-smile'], motion='scan', prop=['binoculars','scan']),
    'missionComplete': dict(poses=[['point-up',0]], badge=['happy','grin'], motion='quiet-pop'),
   },
   lines={
    'plus':['Patrol chip check — let’s see this card.'],
    'plusGain':['Chips earned! Nice work.','Bank it! Great patrol work.'],
    'reward':['Chips earned! Your effort paid off.','Great job — chips earned!'],
    'persist':['You stayed with it. That’s persistence!','Task complete! Nice focus.'],
    'social':['Eyes on the mission. Share a social skill!'],
    'timer':['Stay with it. You’re making progress!','Focus time — one minute on the clock.'],
    'timeUp':['Time! Great focus — let’s talk about it.'],
    'idle':['Eyes on the mission.'],
   }),
}

# Gameplay event -> reaction. closeup:false keeps the reaction on the board
# (used where another overlay already carries the moment, e.g. turn spotlight).
EVENTS = {
 'welcome':   dict(char='coach', state='greeting',     line='welcome',  priority=70),
 'turn':      dict(char='coach', state='attention',    line='turn',     priority=40, closeup=False),
 'situation': dict(char='pause', state='missionAlert', line='situation',priority=60),
 'payoff':    dict(char='think', state='thinking',     line='payoff',   priority=60),
 'power':     dict(char='coach', state='coaching',     line='power',    priority=60),
 'plus':      dict(char='focus', state='attention',    line='plus',     priority=52),
 'plusGain':  dict(char='focus', state='celebrating',  line='plusGain', priority=58),
 'plusLoss':  dict(char='calm',  state='coaching',     line='plusLoss', priority=58),
 'question':  dict(char='think', state='thinking',     line='question', priority=55),
 'firstTry':  dict(char='think', state='celebrating',  line='firstTry', priority=80),
 'retry':     dict(char='flex',  state='retry',        line='retry',    priority=80),
 'recovery':  dict(char='flex',  state='celebrating',  line='recovery', priority=80),
 'incorrect': dict(char='calm',  state='coaching',     line='incorrect',priority=80),
 'teaching':  dict(char='think', state='speaking',     line='teaching', priority=45, closeup=False),
 'reward':    dict(char='focus', state='encouraging',  line='reward',   priority=65),
 'persist':   dict(char='focus', state='encouraging',  line='persist',  priority=66),
 'reflection':dict(char='calm',  state='encouraging',  line='reflection',priority=60),
 'cue':       dict(char='calm',  state='coaching',     line='cue',      priority=55),
 'info':      dict(char='calm',  state='speaking',     line='info',     priority=55),
 'social':    dict(char='focus', state='speaking',     line='social',   priority=55),
 'encounter': dict(char='pause', state='coaching',     line='encounter',priority=55),
 'charades':  dict(char='flex',  state='encouraging',  line='charades', priority=55),
 'free':      dict(char='coach', state='celebrating',  line='free',     priority=55),
 'detour':    dict(char='calm',  state='coaching',     line='detour',   priority=55),
 'exact':     dict(char='flex',  state='encouraging',  line='exact',    priority=50),
 'timer':     dict(char='focus', state='attention',    line='timer',    priority=35),
 'timeUp':    dict(char='focus', state='encouraging',  line='timeUp',   priority=45),
 'finale':    dict(char='*',     state='missionComplete', line='finale', priority=100),
}

STATE_PRIORITY = ['idle','attention','greeting','thinking','speaking','encouraging','coaching','retry','celebrating','missionAlert','missionComplete']
BOARD_W, BOARD_H = 1448, 1086

def asset_rows(cid, group):
    return report['characters'][cid].get(group, {})

out = {'version': 1, 'board': {'width': BOARD_W, 'height': BOARD_H},
       # Close-up geometry in board pixels. The clear zone between the printed spaces is
       # T-shaped: a band across the title logo and a channel down to the THINK sign.
       # Every rectangle keeps >=10 px from the measured edge of every space tile.
       'closeup': {'note': 'T-shaped close-up: speech bubble over the title logo, character card in the open channel below it. Covers decorative art only; no playable space, pawn, card or control.',
                   'x': 300, 'y': 136, 'w': 425, 'h': 396,
                   'bubble': {'x': 300, 'y': 136, 'w': 425, 'h': 116},
                   'card': {'x': 448, 'y': 240, 'w': 207, 'h': 292}},
       'states': STATE_PRIORITY, 'events': EVENTS, 'characters': {}}
runtime_files = set()
for key, c in CHAR.items():
    cid = c['id']
    poses = {}
    for name, row in asset_rows(cid, 'poses').items():
        poses[name] = {'src': row['file'], 'display': row['display'], 'w': row['w'], 'h': row['h'],
                       'heightFactor': HF[cid][name], 'family': family(row['source']), 'sourceCut': row['source']}
    exprs = {n: {'src': r['file'], 'display': r['display'], 'sourceCut': r['source']} for n, r in asset_rows(cid, 'expressions').items()}
    accs = {n: {'src': r['file'], 'display': r['display'], 'sourceCut': r['source']} for n, r in asset_rows(cid, 'accessories').items()}
    rig = {n: {'src': r['file'], 'w': r['w'], 'h': r['h'], 'sourceCut': r['source'], **({'note': r['note']} if r.get('note') else {})}
           for n, r in asset_rows(cid, 'rig').items()}
    # validate state references
    for sname, st in c['states'].items():
        for p, _ in st['poses']:
            assert p in poses, (cid, sname, p)
        for e in st['badge']:
            assert e in exprs, (cid, sname, e)
        if st.get('prop'):
            assert st['prop'][0] in accs, (cid, sname, st['prop'])
        fams = {poses[p]['family'] for p, _ in st['poses']}
        assert len(fams) == 1, ('mixed art family in sequence', cid, sname, fams)
    bp = board[cid]
    safe = set(bp['safe']) - set(c.get('neverOnBoard', []))
    idle_fam = poses[c['boardIdle'][0]]['family']
    board_states = {}
    for sname, st in c['states'].items():
        ok = [p for p, _ in st['poses'] if p in safe and poses[p]['family'] == idle_fam]
        board_states[sname] = ok[0] if ok else c['boardIdle'][0]
    for p in c['boardIdle'] + c['boardAlt']:
        assert p in safe, ('board pose not safe', cid, p)
    out['characters'][key] = {
        'key': key, 'id': cid, 'name': c['name'], 'role': c['role'], 'personality': c['personality'],
        'visualIdentity': c['identity'], 'motionProfile': c['motionProfile'], 'accent': c['accent'], 'accent2': c['accent2'],
        'voice': c['voice'], 'defaultIdlePose': c['boardIdle'][0],
        'board': {'x': bp['cx'], 'baseline': bp['by'], 'height': bp['h'], 'unit': bp['unit'],
                  'idle': c['boardIdle'], 'alternates': c['boardAlt'], 'safePoses': sorted(safe),
                  'statePose': board_states},
        'states': c['states'], 'lines': c['lines'],
        'poses': poses, 'expressions': exprs, 'accessories': accs, 'rig': rig,
        'animationMethod': {
            'fullBody': 'pose swapping (cross-fade between supplied full-body poses)',
            'head': 'independent expression-head layer (comm badge): talk cycles, blinks, expression changes',
            'props': 'independent accessory layer with its own pivot animation',
            'rig': 'body-part sprites extracted and documented; not assembled into a skeleton (see limitations)'},
    }
    for st in c['states'].values():
        for p, _ in st['poses']: runtime_files.add(poses[p]['display'])
        for e in st['badge']: runtime_files.add(exprs[e]['display'])
        if st.get('prop'): runtime_files.add(accs[st['prop'][0]]['display'])
    for p in c['boardIdle'] + c['boardAlt'] + list(board_states.values()):
        runtime_files.add(poses[p]['display'])
    runtime_files.add(exprs[c['states']['idle']['badge'][0]]['display'])

# extra runtime art used outside the board (spotlight, intro/finale lineups, teaching panel, commendations)
EXTRA = [('coach','poses','point'),('coach','poses','thumbs-up'),('think','poses','idea'),('think','expressions','happy'),
         ('flex','expressions','grin'),('calm','expressions','soft'),
         ('coach','poses','cheer'),('calm','poses','celebrate'),('pause','poses','approve-flex'),('think','poses','discover'),
         ('flex','poses','celebrate'),('focus','poses','run-point'),
         ('pause','poses','stop-sign'),('think','poses','magnifier'),('calm','poses','idle'),('flex','poses','thumbs-up-map'),('focus','poses','binoculars')]
for k, g, n in EXTRA:
    runtime_files.add(out['characters'][k][{'poses':'poses','expressions':'expressions'}[g]][n]['display'])
out['runtimeFiles'] = sorted(runtime_files)
out['rejectedCuts'] = REJECTED
out['sourceSheets'] = {
  'master': 'Self-Control_Patrol_Sprite_Sheet_sheet_sheet.png (2088x1680, RGBA)',
  'coach': 'Cartoon_Team_Character_Sprite_Sheet_crop_1_3_509x510_sheet.png (3168x168, RGBA)',
  'coach_small': 'Cartoon_Team_Character_Sprite_Sheet_crop_8_4_493x248_sheet.png (176x168, RGBA)',
  'calm_a': 'Cartoon_Team_Character_Sprite_Sheet_crop_520_0_504x515_sheet_sheet.png (4920x224, RGBA)',
  'calm_b': 'Cartoon_Team_Character_Sprite_Sheet_crop_520_0_504x515_sheet_sheet_1.png (4704x160, RGBA; pixel-identical sprites to calm_a)',
  'pause': 'Cartoon_Team_Character_Sprite_Sheet_crop_0_515_509x542_sheet.png (5760x176, RGBA)',
  'flex': 'Cartoon_Team_Character_Sprite_Sheet_crop_2_1044_508x492_sheet.png (6336x280, RGBA)',
  'focus': 'Cartoon_Team_Character_Sprite_Sheet_crop_514_1055_507x475_sheet.png (4480x192, RGBA)'}

for f in out['runtimeFiles']:
    assert os.path.exists(os.path.join(GAME, f)), f
json.dump(out, open(f'{GAME}/assets/patrol-squad/manifest.json', 'w'), indent=1, ensure_ascii=False)
js = ('/* Patrol Squad character manifest — generated from the supplied sprite sheets. */\n'
      '(function(root){root.PATROL_SQUAD=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) +
      ';})(typeof self!=="undefined"?self:window);\n')
open(f'{GAME}/data/patrol-squad.js', 'w').write(js)
print('characters', len(out['characters']), 'runtime files', len(out['runtimeFiles']), 'js bytes', len(js))
