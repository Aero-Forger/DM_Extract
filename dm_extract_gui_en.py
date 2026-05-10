#!/usr/bin/env python3
"""dm_extract GUI — drone_metadata_c 2.6.1 — Windows/Linux/macOS"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import subprocess, threading, queue, os, sys, platform, shutil, time, re
from pathlib import Path

IS_WIN  = platform.system() == "Windows"
IS_MAC  = platform.system() == "Darwin"
BINARY  = "dm_extract.exe" if IS_WIN else "dm_extract"
MONO    = ("Consolas",10) if IS_WIN else ("Menlo",11) if IS_MAC else ("Monospace",10)

C = {
    "bg":"#2B1D52","panel":"#3A2768","card":"#4E3880","border":"#6A50A0",
    "accent":"#C084FC","accent2":"#A78BFA","text":"#F0EAFF","muted":"#B9A8E0",
    "success":"#86EFAC","warning":"#FDE68A","error":"#FCA5A5","info":"#BAE6FD",
    "con_bg":"#1A0F33","stdout":"#E9D5FF","stderr":"#FCA5A5",
    "cmd":"#93C5FD","sep":"#5B4486",
    "btn_csv":"#5B21B6","btn_geo":"#065F46","btn_raw":"#7C2D8C",
    "btn_inf":"#374151","btn_clr":"#4A3570","btn_exit":"#9D174D",
}

class App:
    def __init__(self, root):
        self.root = root
        root.title("dm_extract GUI  —  drone_metadata_c 2.6.1")
        root.geometry("1200x720"); root.minsize(900,550)
        root.configure(bg=C["bg"])

        self.bin_var   = tk.StringVar()
        self.dir_var   = tk.StringVar()
        self.csv_var   = tk.StringVar()   # chemin sortie CSV
        self.geo_var   = tk.StringVar()   # chemin sortie GeoJSON — SÉPARÉ
        self.disp_var  = tk.StringVar()   # variable affichée dans l'Entry
        self.noheader  = tk.BooleanVar()
        self.quiet     = tk.BooleanVar()
        self.save_file = tk.BooleanVar()
        self._mode     = "csv"
        self._running  = False
        self._start_t  = 0.0    # timestamp début de traitement
        self._n_images = 0      # nombre d'images de la commande courante
        self._q        = queue.Queue()

        self._auto_detect()
        self._build()
        self._poll()
        if self.bin_var.get():
            root.after(300, self._chk_bin_silent)

    # ── auto-detect ──────────────────────────────────────────────────────────
    def _auto_detect(self):
        for c in [Path(sys.argv[0]).parent/BINARY, Path(".")/BINARY,
                  Path.home()/"drone_metadata_c"/"src"/BINARY,
                  Path("/usr/local/bin")/"dm_extract",
                  Path("/usr/bin")/"dm_extract"]:
            if c.exists(): self.bin_var.set(str(c)); return
        f = shutil.which(BINARY) or shutil.which("dm_extract")
        if f: self.bin_var.set(f)

    # ── UI ───────────────────────────────────────────────────────────────────
    def _build(self):
        pw = tk.PanedWindow(self.root, orient=tk.HORIZONTAL,
                            bg=C["bg"], sashwidth=6)
        pw.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        left = tk.Frame(pw, bg=C["panel"], padx=10, pady=10)
        pw.add(left, minsize=285, width=315)

        # Header
        h = tk.Frame(left, bg=C["accent2"], pady=6, padx=8)
        h.pack(fill=tk.X, pady=(0,10))
        tk.Label(h, text="dm_extract  GUI", bg=C["accent2"],
                 fg="#FFF", font=("",12,"bold")).pack(anchor="w")

        # Binaire
        self._lbl(left,"dm_extract binary")
        r = tk.Frame(left, bg=C["panel"]); r.pack(fill=tk.X, pady=3)
        tk.Entry(r, textvariable=self.bin_var, bg=C["card"], fg=C["text"],
                 insertbackground=C["text"], relief=tk.FLAT, bd=4,
                 font=("",9)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._btn(r,"…",self._brw_bin,w=3).pack(side=tk.LEFT,padx=(4,0))
        self._btn(r,"⟳",self._chk_bin,w=3).pack(side=tk.LEFT,padx=(3,0))
        self.lbl_bin = tk.Label(left, text="Not verified", bg=C["panel"],
                                 fg=C["muted"], font=("",9), anchor="w")
        self.lbl_bin.pack(fill=tk.X)
        self._div(left)

        # Répertoire
        self._lbl(left,"Image directory")
        r2 = tk.Frame(left, bg=C["panel"]); r2.pack(fill=tk.X, pady=3)
        tk.Entry(r2, textvariable=self.dir_var, bg=C["card"], fg=C["text"],
                 insertbackground=C["text"], relief=tk.FLAT, bd=4,
                 font=("",9)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._btn(r2,"…",self._brw_dir,w=3).pack(side=tk.LEFT,padx=(4,0))
        self.lbl_img = tk.Label(left, text="", bg=C["panel"],
                                 fg=C["muted"], font=("",9), anchor="w")
        self.lbl_img.pack(fill=tk.X)
        self.dir_var.trace_add("write", lambda *_: self._upd_count())
        self._div(left)

        # Commands
        self._lbl(left,"Commands")
        for txt, bg, fn in [
            ("Extract →  CSV",     C["btn_csv"],  self._csv),
            ("Extract →  GeoJSON", C["btn_geo"],  self._geo),
            ("Dump  --raw",          C["btn_raw"],  self._raw),
            ("--version",            C["btn_inf"],  self._ver),
            ("--help",               C["btn_inf"],  self._hlp),
        ]:
            self._btn(left,txt,fn,bg=bg,pady=5).pack(fill=tk.X,pady=2)
        self._div(left)

        # Options
        self._lbl(left,"Options")
        s = ttk.Style(); s.configure("V.TCheckbutton",
            background=C["panel"],foreground=C["text"],font=("",9))
        ttk.Checkbutton(left, text="--no-header  (CSV without header)",
                        variable=self.noheader,
                        style="V.TCheckbutton").pack(anchor="w",pady=1)
        ttk.Checkbutton(left, text="--quiet  (no progress)",
                        variable=self.quiet,
                        style="V.TCheckbutton").pack(anchor="w",pady=1)
        self._div(left)

        # Output file
        self._lbl(left,"Output file")
        ttk.Checkbutton(left, text="Save to file",
                        variable=self.save_file, style="V.TCheckbutton",
                        command=self._tog_out).pack(anchor="w",pady=1)
        of = tk.Frame(left, bg=C["panel"]); of.pack(fill=tk.X,pady=(4,0))
        self.ent_out = tk.Entry(of, textvariable=self.disp_var,
                                 bg=C["card"], fg=C["text"],
                                 insertbackground=C["text"],
                                 relief=tk.FLAT, bd=4, font=("",9),
                                 state=tk.DISABLED)
        self.ent_out.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.disp_var.trace_add("write", self._sync_out)
        self.btn_out = self._btn(of,"…",self._brw_out,w=3,state=tk.DISABLED)
        self.btn_out.pack(side=tk.LEFT,padx=(4,0))
        self.lbl_fmt = tk.Label(left, text="Active format : CSV  (.csv)",
                                 bg=C["panel"], fg=C["accent"],
                                 font=("",9), anchor="w")
        self.lbl_fmt.pack(fill=tk.X,pady=(2,0))

        # Bas
        tk.Frame(left, bg=C["panel"]).pack(fill=tk.BOTH, expand=True)
        btm = tk.Frame(left, bg=C["panel"]); btm.pack(fill=tk.X,pady=(6,0))
        self._btn(btm,"Clear console",self._clr,bg=C["btn_clr"]
                  ).pack(fill=tk.X,pady=(0,5))
        self._btn(btm,"✕  EXIT",self._exit,bg=C["btn_exit"],
                  bold=True,pady=6).pack(fill=tk.X)

        # Console
        right = tk.Frame(pw, bg=C["bg"]); pw.add(right, minsize=500)

        # Ligne titre + statut
        hd = tk.Frame(right, bg=C["bg"]); hd.pack(fill=tk.X,padx=4,pady=(4,2))
        tk.Label(hd, text="Console", bg=C["bg"],
                 fg=C["text"], font=("",11,"bold")).pack(side=tk.LEFT)
        self.lbl_st = tk.Label(hd, text="Ready", bg=C["bg"],
                                fg=C["muted"], font=("",9))
        self.lbl_st.pack(side=tk.RIGHT)

        # Barre de progression
        prg = tk.Frame(right, bg=C["bg"]); prg.pack(fill=tk.X,padx=4,pady=(0,3))
        s2 = ttk.Style()
        s2.configure("Violet.Horizontal.TProgressbar",
                      troughcolor=C["con_bg"],
                      background=C["accent"],
                      bordercolor=C["panel"],
                      lightcolor=C["accent"],
                      darkcolor=C["accent2"])
        self.pb = ttk.Progressbar(prg, orient=tk.HORIZONTAL,
                                   mode="determinate", length=100,
                                   style="Violet.Horizontal.TProgressbar")
        self.pb.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.pb["value"] = 0

        # Label progression + temps
        self.lbl_prg = tk.Label(prg, text="", bg=C["bg"],
                                 fg=C["muted"], font=("",9),
                                 width=22, anchor="e")
        self.lbl_prg.pack(side=tk.RIGHT, padx=(6,0))

        self.con = scrolledtext.ScrolledText(
            right, font=MONO, wrap=tk.WORD,
            bg=C["con_bg"], fg=C["stdout"],
            insertbackground=C["text"], selectbackground=C["card"],
            relief=tk.FLAT, bd=0, padx=10, pady=8, state=tk.DISABLED)
        self.con.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0,4))
        for t,col in [("stdout",C["stdout"]),("stderr",C["stderr"]),
                      ("info",C["success"]),("warning",C["warning"]),
                      ("error",C["error"]),("cmd",C["cmd"]),("sep",C["sep"])]:
            self.con.tag_config(t, foreground=col)

        self._cw("dm_extract GUI  —  drone_metadata_c 2.6.1\n","info")
        self._cw(f"Platform: {platform.system()} {platform.machine()}\n","sep")
        self._cw("─"*60+"\n","sep")

    # ── helpers UI ───────────────────────────────────────────────────────────
    def _lbl(self, p, t):
        tk.Label(p, text=t, bg=C["panel"], fg=C["muted"],
                 font=("",9)).pack(anchor="w")
    def _div(self, p):
        tk.Frame(p, bg=C["border"], height=1).pack(fill=tk.X, pady=7)
    def _btn(self, p, t, fn, bg=None, fg="#FFF", w=None,
             pady=4, bold=False, state=tk.NORMAL):
        b = tk.Button(p, text=t, command=fn,
                      bg=bg or C["card"], fg=fg,
                      relief=tk.FLAT, bd=0, padx=10, pady=pady,
                      cursor="hand2", activebackground=bg or C["card"],
                      activeforeground=fg, state=state,
                      font=("",10,"bold") if bold else ("",10))
        if w: b.config(width=w)
        return b

    # ── sortie fichier ────────────────────────────────────────────────────────
    def _set_mode(self, mode):
        self._mode = mode
        if mode == "geojson":
            self.disp_var.set(self.geo_var.get())
            self.lbl_fmt.config(
                text="Active format : GeoJSON  (.geojson)", fg=C["success"])
        else:
            self.disp_var.set(self.csv_var.get())
            self.lbl_fmt.config(
                text="Active format : CSV  (.csv)", fg=C["accent"])

    def _sync_out(self, *_):
        v = self.disp_var.get()
        if self._mode == "geojson": self.geo_var.set(v)
        else: self.csv_var.set(v)

    def _tog_out(self):
        s = tk.NORMAL if self.save_file.get() else tk.DISABLED
        self.ent_out.config(state=s); self.btn_out.config(state=s)

    def _brw_out(self):
        if self._mode == "geojson":
            ext=".geojson"; types=[("GeoJSON","*.geojson"),("Tous","*")]
            ini=self.geo_var.get() or "export.geojson"
        else:
            ext=".csv"; types=[("CSV","*.csv"),("Tous","*")]
            ini=self.csv_var.get() or "rapport.csv"
        p = filedialog.asksaveasfilename(title="Output file",
            defaultextension=ext, initialfile=os.path.basename(ini),
            filetypes=types)
        if p: self.disp_var.set(p)

    # ── navigation ───────────────────────────────────────────────────────────
    def _brw_bin(self):
        types=[("Executables","*.exe"),("Tous","*")] if IS_WIN \
              else [("All files","*")]
        p = filedialog.askopenfilename(title="Select dm_extract",
                                       filetypes=types)
        if p: self.bin_var.set(p); self._chk_bin()

    def _brw_dir(self):
        p = filedialog.askdirectory(title="Select directory")
        if p: self.dir_var.set(p)

    def _chk_bin(self):
        bp = self.bin_var.get()
        if not bp or not os.path.isfile(bp):
            self.lbl_bin.config(text="✗ Not found", fg=C["error"]); return
        try:
            r = subprocess.run([bp,"--version"],capture_output=True,
                               text=True,timeout=5)
            self.lbl_bin.config(
                text=f"✓ {(r.stdout or r.stderr).strip()}", fg=C["success"])
        except Exception as e:
            self.lbl_bin.config(text=f"✗ {e}", fg=C["error"])

    def _chk_bin_silent(self):
        bp = self.bin_var.get()
        if not bp or not os.path.isfile(bp):
            self.lbl_bin.config(text="✗ Not found", fg=C["warning"]); return
        try:
            r = subprocess.run([bp,"--version"],capture_output=True,
                               text=True,timeout=5)
            ver=(r.stdout or r.stderr).strip()
            self.lbl_bin.config(text=f"✓ {ver}", fg=C["success"])
            self._cw(f"Binaire : {bp}\nVersion : {ver}\n\n","info")
        except Exception:
            self.lbl_bin.config(text="✗ Execution error", fg=C["error"])

    def _upd_count(self):
        d = self.dir_var.get()
        if not d or not os.path.isdir(d):
            self.lbl_img.config(text=""); return
        try:
            n = len([f for f in os.listdir(d)
                     if f.lower().endswith((".jpg",".jpeg"))])
            self.lbl_img.config(
                text=f"{n} image{'s' if n>1 else ''} JPEG",
                fg=C["success"] if n>0 else C["warning"])
        except Exception:
            self.lbl_img.config(text="Read error", fg=C["error"])

    # ── Commands ────────────────────────────────────────────────────────────
    def _csv(self): self._set_mode("csv");     self._run("csv")
    def _geo(self): self._set_mode("geojson"); self._run("geojson")
    def _raw(self): self._set_mode("raw");     self._run("raw")
    def _ver(self): self._run("version")
    def _hlp(self): self._run("help")

    def _get_imgs(self):
        d = self.dir_var.get()
        if not d: messagebox.showerror("Erreur","Aucun répertoire."); return None
        if not os.path.isdir(d):
            messagebox.showerror("Erreur",f"not found:\n{d}"); return None
        imgs = sorted([os.path.join(d,f) for f in os.listdir(d)
                       if f.lower().endswith((".jpg",".jpeg"))])
        if not imgs:
            messagebox.showwarning("Attention",f"No JPEG in :\n{d}")
            return None
        return imgs

    def _build_cmd(self, mode):
        bp = self.bin_var.get()
        if not bp or not os.path.isfile(bp):
            messagebox.showerror("Erreur","dm_extract binary not found.")
            return None
        if mode in ("version","help"): return [bp, f"--{mode}"]
        imgs = self._get_imgs()
        if imgs is None: return None

        cmd = [bp]
        if mode == "geojson": cmd.append("--geojson")
        elif mode == "raw":   cmd.append("--raw")
        if mode == "csv" and self.noheader.get(): cmd.append("--no-header")
        if self.quiet.get(): cmd.append("--quiet")

        if self.save_file.get():
            # Chemin distinct par format — évite l'écrasement CSV↔GeoJSON
            if mode == "geojson":
                out = self.geo_var.get()
                if out and out.lower().endswith(".csv"):
                    out = str(Path(out).with_suffix(".geojson"))
                    self.geo_var.set(out); self.disp_var.set(out)
                    self._cw(f"Info : extension corrected → {out}\n","warning")
            else:
                out = self.csv_var.get()
                if out and out.lower().endswith(".geojson"):
                    out = str(Path(out).with_suffix(".csv"))
                    self.csv_var.set(out); self.disp_var.set(out)
                    self._cw(f"Info : extension corrected → {out}\n","warning")
            if out: cmd += ["-o", out]

        cmd += imgs
        return cmd

    def _run(self, mode):
        if self._running:
            messagebox.showwarning("Running","Command already running."); return
        cmd = self._build_cmd(mode)
        if not cmd: return

        self._cw("\n"+"─"*60+"\n","sep")
        disp = [os.path.basename(cmd[0])] + cmd[1:]
        shown = " ".join(disp[:7]) + (f"  … ({len(disp)-1} fichiers)"
                                       if len(disp)>7 else "")
        self._cw(f"$ {shown}\n","cmd")
        self._cw("─"*60+"\n","sep")
        self._running = True
        self._start_t = time.time()
        self._n_images = len(cmd) - cmd.index(cmd[-1]) if mode not in ("version","help") else 0
        # Counting the images in the command (anything that is not an option)
        self._n_images = sum(1 for a in cmd[1:] if not a.startswith("-")
                             and a.lower().endswith((".jpg",".jpeg")))
        self.pb.config(mode="determinate", maximum=max(self._n_images,1))
        self.pb["value"] = 0
        self.lbl_prg.config(text="0 / " + str(self._n_images) if self._n_images else "")
        self.lbl_st.config(text="⏳ In progress…", fg=C["warning"])
        threading.Thread(target=self._exec, args=(cmd,), daemon=True).start()

    def _exec(self, cmd):
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True, errors="replace")
            def rd(s, t):
                for l in s: self._q.put((t, l.rstrip("\n")))
                self._q.put((t, None))
            t1=threading.Thread(target=rd,args=(p.stdout,"stdout"),daemon=True)
            t2=threading.Thread(target=rd,args=(p.stderr,"stderr"),daemon=True)
            t1.start(); t2.start(); t1.join(); t2.join(); p.wait()
            self._q.put(("__done__", p.returncode))
        except FileNotFoundError:
            self._q.put(("error", f"Binary not found : {cmd[0]}"))
            self._q.put(("__done__", -1))
        except Exception as e:
            self._q.put(("error", str(e))); self._q.put(("__done__", -1))

    def _poll(self):
        try:
            while True:
                tag, data = self._q.get_nowait()
                if tag == "__done__":
                    rc = data; self._running = False
                    elapsed = time.time() - self._start_t
                    n = self._n_images

                    # Barre à 100%
                    self.pb["value"] = self.pb["maximum"]

                    # Statut + timing
                    if rc == 0:
                        self.lbl_st.config(text="✓ Success (0", fg=C["success"])
                    elif rc == 1:
                        self.lbl_st.config(text="⚠ 	Partial (1)", fg=C["warning"])
                    else:
                        self.lbl_st.config(text=f"✗ Error  ({rc})", fg=C["error"])

                    # Label final progress
                    if n > 0:
                        rate = n / elapsed if elapsed > 0 else 0
                        self.lbl_prg.config(
                            text=f"{n}/{n}  •  {elapsed:.1f}s",
                            fg=C["success"] if rc==0 else C["warning"])
                    else:
                        self.lbl_prg.config(text=f"{elapsed:.1f}s", fg=C["muted"])

                    # Résumé en console
                    tag_rc = "info" if rc==0 else "warning" if rc==1 else "error"
                    self._cw(f"\n→ Exit code : {rc}\n", tag_rc)
                    if n > 0:
                        rate = n / elapsed if elapsed > 0 else 0
                        self._cw(
                            f"⏱  {n} image{'s' if n>1 else ''} processed{'s' if n>1 else ''}"
                            f" en {elapsed:.2f} s"
                            f"  ({rate:.1f} img/s)\n",
                            "info" if rc==0 else "warning")

                elif data is not None:
                    # Parser [N/M] dans stderr pour mettre à jour la barre
                    if tag == "stderr":
                        m = re.match(r"^\[(\d+)/(\d+)\]", data)
                        if m:
                            cur, tot = int(m.group(1)), int(m.group(2))
                            self.pb.config(maximum=tot)
                            self.pb["value"] = cur
                            elapsed = time.time() - self._start_t
                            # Estimation temps restant
                            if cur > 0 and elapsed > 0:
                                eta = (tot - cur) * elapsed / cur
                                self.lbl_prg.config(
                                    text=f"{cur}/{tot}  •  -{eta:.0f}s",
                                    fg=C["accent"])
                            else:
                                self.lbl_prg.config(
                                    text=f"{cur}/{tot}", fg=C["accent"])
                    self._cw(data+"\n", tag)
        except queue.Empty:
            pass
        self.root.after(40, self._poll)

    # ── console ───────────────────────────────────────────────────────────────
    def _cw(self, txt, tag="stdout"):
        self.con.config(state=tk.NORMAL)
        self.con.insert(tk.END, txt, tag)
        self.con.see(tk.END)
        self.con.config(state=tk.DISABLED)

    def _clr(self):
        self.con.config(state=tk.NORMAL)
        self.con.delete("1.0", tk.END)
        self.con.config(state=tk.DISABLED)
        self.lbl_st.config(text="Ready", fg=C["muted"])
        self.pb["value"] = 0
        self.lbl_prg.config(text="")

    def _exit(self):
        if messagebox.askokcancel("Exit ","Exit dm_extract GUI ?",
                                   parent=self.root):
            self.root.destroy()


def main():
    root = tk.Tk()
    root.configure(bg=C["bg"])
    s = ttk.Style(root)
    try: s.theme_use("clam")
    except Exception: pass
    s.configure(".", background=C["panel"], foreground=C["text"])
    s.configure("TPanedwindow", background=C["bg"])
    s.configure("TScrollbar", background=C["card"],
                 troughcolor=C["con_bg"], arrowcolor=C["muted"])
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app._exit)
    root.mainloop()

if __name__ == "__main__":
    main()


