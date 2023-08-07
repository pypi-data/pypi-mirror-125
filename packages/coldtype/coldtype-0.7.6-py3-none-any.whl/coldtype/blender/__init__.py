# to be loaded from within Blender

import os, math, json
from pathlib import Path
from coldtype.geometry import curve

from coldtype.geometry.rect import Rect
from coldtype.pens.datpen import DATPen, DATPens
from coldtype.pens.blenderpen import BlenderPen, BPH
from coldtype.color import hsl

from coldtype.time import Frame, Timeline
from coldtype.renderable import renderable, Overlay, Action, runnable
from coldtype.renderable.animation import animation

from coldtype.blender.render import blend_source
from coldtype.time.sequence import ClipTrack, Clip, Sequence

from coldtype.blender.fluent import BpyWorld, BpyObj, BpyCollection


try:
    import bpy # noqa
except ImportError:
    bpy = None
    pass


class BlenderTimeline(Sequence):
    __name__ = "Blender"
    
    def __init__(self, duration, fps, data,
        workarea_track=1,
        ):
        tracks = []
        for t in data.get("tracks", []):
            clips = []
            for cidx, clip in enumerate(t["clips"]):
                clips.append(Clip(
                    clip["text"],
                    clip["start"],
                    clip["end"],
                    idx=cidx,
                    track=t["index"]))
            
            tracks.append(ClipTrack(self, clips, []))
        
        self.workarea = range(
            data.get("start", 0),
            data.get("end", duration-1)+1)

        super().__init__(
            duration,
            fps,
            [data.get("current_frame", 0)],
            tracks,
            workarea_track=workarea_track-1)


def b3d(collection,
    callback=None,
    plane=False,
    dn=False,
    cyclic=True,
    material=None,
    zero=False,
    upright=False,
    tag_prefix=None,
    ):
    if not bpy: # short-circuit if this is meaningless
        return lambda x: x

    if not isinstance(collection, str):
        callback = collection
        collection = "Coldtype"

    pen_mod = None
    if callback and not callable(callback):
        pen_mod = callback[0]
        callback = callback[1]

    def annotate(pen:DATPen):
        if bpy and pen_mod:
            pen_mod(pen)
        
        prev = pen.data.get("b3d", {})
        if prev:
            callbacks = [*prev.get("callbacks"), callback]
        else:
            callbacks = [callback]

        #c = None
        #if zero:
        #    c = pen.ambit().pc
        #    pen.translate(-c.x, -c.y)

        pen.add_data("b3d", dict(
            collection=(collection
                or prev.get("collection", "Coldtype")),
            callbacks=callbacks,
            material=(material
                or prev.get("material", "ColdtypeDefault")),
            tag_prefix=(tag_prefix or prev.get("tag_prefix")),
            dn=dn,
            cyclic=cyclic,
            plane=plane,
            zero=zero,
            #reposition=c,
            upright=upright))
    
    return annotate


def b3d_post(callback):
    if not bpy: # short-circuit for non-bpy
        return lambda x: x

    def _b3d_post(pen:DATPen):
        prev = pen.data.get("b3d_post")
        if prev:
            callbacks = [*prev, callback]
        else:
            callbacks = [callback]
        pen.data["b3d_post"] = callbacks
    
    return _b3d_post


def b3d_pre(callback):
    def _cast(pen:DATPen):
        if bpy:
            callback(pen)
    return _cast


def walk_to_b3d(result:DATPens,
    dn=False,
    renderable=None,
    ):
    built = {}

    center = renderable.center
    center_rect = renderable.rect

    def walker(p:DATPen, pos, data):
        bp = None

        if pos == 0:
            bdata = p.data.get("b3d")
            if not bdata:
                p.ch(b3d(lambda bp: bp.extrude(0.01)))
                bdata = p.data.get("b3d")
            
            zero = bdata.get("zero", False)

            if center and True:
                cx = -center_rect.w/2*(1-center[0])
                cy = -center_rect.h/2*(1-center[1])
                p.translate(cx, cy)

            pc = p.ambit().pc
            if zero:
                p.translate(-pc.x, -pc.y)
            
            if p.tag() == "?" and data.get("idx"):
                tag = "_".join([str(i) for i in data["idx"]])
                if bdata.get("tag_prefix"):
                    tag = bdata.get("tag_prefix") + tag
                else:
                    tag = "ct_autotag_" + tag
                p.tag(tag)

            if bdata:
                coll = BPH.Collection(bdata["collection"])
                material = bdata.get("material", "ColdtypeDefault")

                if len(p.value) == 0:
                    p.v(0)
                
                denovo = bdata.get("dn", dn)
                cyclic = bdata.get("cyclic", True)

                if bdata.get("plane"):
                    bp = p.cast(BlenderPen).draw(coll, plane=True, material=material, dn=True)
                else:
                    bp = p.cast(BlenderPen).draw(coll, dn=denovo, material=material, cyclic=cyclic)
                
                bp.rotate(0)
                
                if bdata.get("callbacks"):
                    for cb in bdata.get("callbacks"):
                        cb(bp)

                bp.hide(not p._visible)

                # if center and False:
                #     cx = -center_rect.w/2*(1-center[0])
                #     cy = -center_rect.h/2*(1-center[1])
                #     bp.locate_relative(cx/100, cy/100)

                if renderable:
                    if renderable.upright:
                        bp.rotate(90)

                if zero: #bdata.get("reposition"):
                    pt = pc #bdata.get("reposition")
                    if bdata.get("upright"):
                        bp.locate_relative(pt.x/100, 0, pt.y/100)
                    else:
                        bp.locate_relative(pt.x/100, pt.y/100)
                
                built[p.tag()] = (p, bp)

        if pos == 0 or pos == 1:
            b3d_post = p.data.get("b3d_post")
            if b3d_post:
                for post in b3d_post:
                    post(bp)
                
    result.walk(walker)


class b3d_runnable(runnable):
    def __init__(self, solo=False, cond=None):
        if cond is not None:
            cond = lambda: cond and bool(bpy)
        else:
            cond = bool(bpy)
        
        super().__init__(solo=solo, cond=cond)
    def run(self):
        if not bpy:
            return None
        else:
            return self.func(BpyWorld().deselect_all())


class b3d_renderable(renderable):
    def __init__(self,
        rect=(1080, 1080),
        center=(0, 0),
        upright=False,
        post_run=None,
        **kwargs
        ):
        self.center = center
        self.upright = upright
        self.post_run = post_run
        self.blender_file = None
        super().__init__(rect, **kwargs)


class b3d_animation(animation):
    def __init__(self,
        rect=(1080, 1080),
        samples=-1,
        denoise=False,
        match_length=True,
        match_output=True,
        match_fps=True,
        bake=False,
        center=(0, 0),
        upright=False,
        create_timeline=False,
        autosave=False,
        renderer="b3d",
        **kwargs
        ):
        self.func = None
        self.name = None
        self.current_frame = -1
        self.samples = samples
        self.denoise = denoise
        self.bake = bake
        self.center = center
        self.upright = upright
        self.match_length = match_length
        self.match_output = match_output
        self.match_fps = match_fps
        self.renderer = renderer
        self.create_timeline = create_timeline
        self.autosave = autosave
        self._bt = False
        self.blender_file = None

        if "timeline" not in kwargs:
            kwargs["timeline"] = Timeline(30)
        
        super().__init__(rect=rect, **kwargs)
    
    def post_read(self):
        out = self.reread_timeline(reset=True)
        super().post_read()

        if bpy and self.match_output:
            bpy.data.scenes[0].render.filepath = str(self.pass_path(""))
        
        return out
    
    def reread_timeline(self, reset=False):
        if self.create_timeline:
            if not self.data_path().exists():
                self.data_path().write_text("{}")

        if self.data_path().exists():
            self._bt = True
            bt = BlenderTimeline(
                self.timeline.duration,
                self.timeline.fps,
                self.data())
            if reset:
                self.reset_timeline(bt)
            else:
                self.timeline = bt
                self.t = self.timeline
            return bt.storyboard
    
    def reset_timeline(self, timeline):
        super().reset_timeline(timeline)

        do_match_length = self.match_length
        if isinstance(self.timeline, BlenderTimeline) and len(self.timeline.tracks) == 0:
            do_match_length = True

        if bpy and do_match_length:
            bpy.data.scenes[0].frame_start = 0
            bpy.data.scenes[0].frame_end = self.t.duration-1
        
        if bpy and self.match_fps:
            # don't think this is totally accurate but good enough for now
            if isinstance(self.t.fps, float):
                bpy.data.scenes[0].render.fps = round(self.t.fps)
                bpy.data.scenes[0].render.fps_base = 1.001
            else:
                bpy.data.scenes[0].render.fps = self.t.fps
                bpy.data.scenes[0].render.fps_base = 1
        
    def running_in_viewer(self):
        return not bpy
    
    def rasterize(self, config, content, rp):
        if self.renderer == "skia":
            return super().rasterize(config, content, rp)
        
        fi = rp.args[0].i
        blend_source(config.blender_app_path, self.filepath, self.blender_file, fi, self.pass_path(""), self.samples, denoise=self.denoise)
        return True
    
    def baked_frames(self):
        def bakewalk(p, pos, data):
            if pos == 0:
                fi = data["idx"][0]
                (p.ch(b3d(f"CTBakedAnimation_{self.name}",
                    lambda bp: bp
                        .show_on_frame(fi)
                        .print(f"Baking frame {fi}..."),
                    dn=True,
                    tag_prefix=f"ct_baked_frame_{fi}_{self.name}")))
        
        to_bake = DATPens([])
        for ps in self.passes(Action.RenderAll, None)[:]:
            to_bake += self.run_normal(ps, None)
        
        return to_bake.walk(bakewalk)
    
    def data_path(self):
        return Path(str(self.blender_file) + ".json")
    
    def data(self):
        return json.loads(self.data_path().read_text())


class b3d_sequencer(b3d_animation):
    def __init__(self,
        rect=Rect(1080, 1080),
        autosave=True,
        **kwargs
        ):
        super().__init__(
            rect=rect,
            match_fps=True,
            match_length=False,
            match_output=False,
            create_timeline=True,
            autosave=autosave,
            renderer="skia",
            **kwargs)
    
    def post_read(self):
        out = super().post_read()
        if self._bt:
            self.add_watchee(self.data_path(), "soft")
        return out