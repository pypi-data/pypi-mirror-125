import json
from pathlib import Path
from coldtype.geometry import Point
from coldtype.renderable import Action


class RendererStateEncoder(json.JSONEncoder):
    def default(self, o):
        return {
            "controller_values": o.controller_values
        }


class RendererState():
    def __init__(self, renderer):
        self.renderer = renderer
        self.previewing = False
        self.preview_scale = 1
        self.controller_values = {}
        self.overlays = {}
        self._frame_offsets = {}
        self._initial_frame_offsets = {}
        self.canvas = None
        self._last_filepath = None
        self.cv2caps = {}
        self.inputs = []
        self.memory = {}
        self.playing = False

        self.cursor = Point(0, 0)
        self.cursor_history = []

        for c in renderer.args.last_cursor.split(";"):
            cp = Point([float(p) for p in c.split(",")])
            self.cursor_history.append(cp)
        
        if len(self.cursor_history) > 0:
            self.cursor = self.cursor_history[-1]

        self.reset()
    
    def reset(self, ignore_current_state=False):
        if self.filepath == self._last_filepath and not ignore_current_state:
            return
        
        if self.filepath:
            self._last_filepath = self.filepath
            try:
                deserial = json.loads(self.filepath.read_text())
                cv = deserial.get("controller_values")
                if cv:
                    self.controller_values = cv
            except json.decoder.JSONDecodeError:
                self.controller_values = {}
            except FileNotFoundError:
                self.controller_values = {}
    
    def clear(self):
        if self.filepath:
            self.filepath.write_text("")
        self.reset()
    
    @property
    def filepath(self):
        if self.renderer and self.renderer.source_reader.filepath:
            return Path(str(self.renderer.source_reader.filepath).replace(".py", "") + "_state.json")
        else:
            return None
    
    @property
    def midi(self):
        return self.controller_values
    
    def persist(self):
        if self.filepath:
            print("Saving Controller State...")
            self.filepath.write_text(RendererStateEncoder().encode(self))
        else:
            print("No source; cannot persist state")
    
    def record_cursor(self, pos):
        self.cursor = pos.scale(1/self.preview_scale).round_to(1)
        return self.cursor
        #return Action.PreviewStoryboard
    
    def on_mouse_button(self, pos, btn, action, mods):
        if not self.playing and action == 0:
            p = self.record_cursor(pos)
            #if self.cursor_history[-1] != p:
            self.cursor_history.append(p)
            return Action.PreviewStoryboard
    
    def on_mouse_move(self, pos):
        if self.playing:
            self.record_cursor(pos)
    
    def mod_preview_scale(self, inc, absolute=0):
        if absolute > 0:
            ps = absolute
        else:
            ps = self.preview_scale + inc
        self.preview_scale = max(0.1, min(5, ps))
    
    def add_frame_offset(self, key, offset):
        if key in self._frame_offsets:
            offsets = self._frame_offsets[key]
            initials = self._initial_frame_offsets[key]
            offsets.append(offset)
            initials.append(offset)
        else:
            self._frame_offsets[key] = [offset]
            self._initial_frame_offsets[key] = [offset]
    
    def get_frame_offsets(self, key):
        return self._frame_offsets.get(key, [0])
    
    def adjust_all_frame_offsets(self, adj, absolute=False):
        if absolute:
            for k, v in self._frame_offsets.items():
                for i, o in enumerate(v):
                    v[i] = adj
        else:
            for k, v in self._frame_offsets.items():
                for i, o in enumerate(v):
                    v[i] = o + adj
    
    def adjust_keyed_frame_offsets(self, key, fn):
        offs = self.get_frame_offsets(key)
        for i, o in enumerate(offs):
            offs[i] = fn(i, o)
    
    def toggle_overlay(self, overlay, force=None):
        if force is not None:
            v = force
        else:
            v = not self.overlays.get(overlay, False)
        if not v:
            if overlay in self.overlays:
                del self.overlays[overlay]
        else:
            self.overlays[overlay] = True