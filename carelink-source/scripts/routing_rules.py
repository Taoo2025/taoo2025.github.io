"""Motorcar rules and sparse via-node turn state expansion."""
import re

def access_allowed(tags):
    value=next((tags[k] for k in ('motorcar','motor_vehicle','vehicle','access') if k in tags),'yes')
    return value not in ('no','private','agricultural','forestry')

def blocked_node(tags):
    if not access_allowed(tags): return True
    explicit=any(tags.get(k) in ('yes','permissive','designated','destination') for k in ('motorcar','motor_vehicle','vehicle','access'))
    return not explicit and tags.get('barrier') in ('bollard','block','cycle_barrier','kissing_gate','stile','bus_trap')

def directions(tags):
    d=tags.get('oneway:motorcar',tags.get('oneway:motor_vehicle',tags.get('oneway','yes' if tags.get('junction')=='roundabout' or tags.get('highway') in ('motorway','motorway_link') else 'no')))
    return (False,True) if d in ('-1','reverse') else ((True,False) if d in ('yes','1','true') else (True,True))

def speed_kmh(value, default):
    match=re.fullmatch(r'\s*(\d+(?:\.\d+)?)\s*(mph|km/h|kmh)?\s*',value or '')
    if not match:return default
    speed=float(match[1])*(1.609344 if match[2]=='mph' else 1)
    return min(default,speed) if speed>0 else default

def turn_allowed(previous, via, following, incoming_way, outgoing_way, rules):
    active=[r for r in rules if r['from']==incoming_way]
    only=[r for r in active if r['kind'].startswith('only_')]
    def matches(r):
        if r['to']!=outgoing_way:return False
        # A same-way U turn means returning along the incoming segment.
        if r['kind'].endswith('u_turn'):return previous==following
        return True
    if only and not any(matches(r) for r in only):return False
    return not any(r['kind'].startswith('no_') and matches(r) for r in active)

def expand_turns(edges, rules):
    """edges[(a,b)] = (metres, seconds, way ID). Only restricted junctions expand.
    State (previous, via) remembers approach; no shortcut via the base junction.
    Endpoints must snap to ordinary nodes, not restricted junction base nodes.
    """
    incoming={v:[] for v in rules};outgoing={v:[] for v in rules}
    for (a,b),value in edges.items():
        if b in incoming:incoming[b].append((a,value))
        if a in outgoing:outgoing[a].append((b,value))
    for (a,b),value in edges.items():
        if a not in rules:
            yield a, (a,b) if b in rules else b, value
    for via, entries in incoming.items():
        for previous, inc in entries:
            for following, out in outgoing[via]:
                if turn_allowed(previous,via,following,inc[2],out[2],rules[via]):
                    yield (previous,via), (via,following) if following in rules else following, out
