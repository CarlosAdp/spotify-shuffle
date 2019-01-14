from utils.spotify_utils import SpotifyUtils
from operator import add
from utils.constants import Constants
from pprint import pprint

def get_section_distance(parameter, item):
    f1 = [parameter.get("features").get("tempo")] + parameter.get("features").get("pitches") + parameter.get("features").get("timbre")
    f2 = [item.get("features").get("tempo")] + item.get("features").get("pitches") + item.get("features").get("timbre")

    return sum([(i1 - i2) * (i1 - i2) for i1, i2 in zip(f1, f2)])

Constants.init()
SpotifyUtils.authenticate()
sp = SpotifyUtils._spotify_connection
aa = sp.audio_analysis("1Bd6dyt1HJCNqBXD9Rh2TR")
sections = aa.get("sections")
segments = aa.get("segments")
s_infos = []
seg_index = 0

for section in sections:
    s_info = {
            "start": section.get("start"),
            "end": section.get("start") + section.get("duration"),
            "song": "TE ENCONTREI",
            "features" : {
                    "tempo" : section.get("tempo") / 500.0
                    }
            }

    n_segments = 0
    pitches = [0,0,0,0,0,0,0,0,0,0,0,0]
    timbre = [0,0,0,0,0,0,0,0,0,0,0,0]

    while True:
        pitches = list(map(add, pitches, segments[seg_index].get("pitches")))
        timbre = list(map(add, timbre, segments[seg_index].get("timbre")))
        n_segments += 1
        seg_index += 1

        if seg_index == len(segments) or segments[seg_index].get("start") > s_info.get("end"):
            pitches = [item / (10 * float(n_segments)) for item in pitches]
            timbre = [item / (1000 * float(n_segments)) for item in timbre]
            break

    s_info.get("features")["pitches"] = pitches
    s_info.get("features")["timbre"] = timbre

    s_infos.append(s_info)

aa2 = sp.audio_analysis("4BcsD7X41Kb68V2SMZy6MH")
sections = aa2.get("sections")
segments = aa2.get("segments")
seg_index = 0

for section in sections:
    s_info = {
            "start": section.get("start"),
            "end": section.get("start") + section.get("duration"),
            "song": "GHULEH",
            "features" : {
                    "tempo" : section.get("tempo") / 500.0
                    }
            }

    n_segments = 0
    pitches = [0,0,0,0,0,0,0,0,0,0,0,0]
    timbre = [0,0,0,0,0,0,0,0,0,0,0,0]

    while True:
        pitches = list(map(add, pitches, segments[seg_index].get("pitches")))
        timbre = list(map(add, timbre, segments[seg_index].get("timbre")))
        n_segments += 1
        seg_index += 1

        if seg_index == len(segments) or segments[seg_index].get("start") > s_info.get("end"):
            pitches = [item / (10 * float(n_segments)) for item in pitches]
            timbre = [item / (1000 * float(n_segments)) for item in timbre]
            break

    s_info.get("features")["pitches"] = pitches
    s_info.get("features")["timbre"] = timbre

    s_infos.append(s_info)


parameter = s_infos[1]
s_sorted = sorted(s_infos, key = lambda item : get_section_distance(parameter, item))
for s_info in s_sorted:
    print(s_info.get("song"), s_info.get("start"), s_info.get("end"))
