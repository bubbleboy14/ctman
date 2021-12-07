man.util = {
	collapser: function(title) {
		var n = CT.dom.div(title, "pointer");
		n.onclick = function() {
			n._collapsed = !n._collapsed;
			n.parentNode.classList[n._collapsed ? "add" : "remove"]("collapsed");
		};
		setTimeout(function() {
			n.parentNode.classList.add("collapsible");
		});
		return n;
	},
	form: function(d, fname, cb, extra, items, collapsible) {
		var title = d[fname] && fname;
		return CT.dom.div([
			collapsible ? man.util.collapser(title) : title,
			CT.layout.form({
				cb: cb,
				extra: extra,
				button: true,
				labels: true,
				bname: "save",
				values: d[fname] || d,
				items: items || core.config.ctman[fname]
			}),
		], core.config.ctman.classes[d.modelName].form);
	},
	refresher: function(title, buttname, buttcb, bodgen, classes, collapsible) {
		var n = CT.dom.div(null, classes || "margined padded bordered round"),
			section = this.section, asec = this.asec;
		n.refresh = function() {
			CT.dom.setContent(n, [
				CT.dom.button(buttname, buttcb(n), "right"),
				collapsible ? man.util.collapser(title) : title,
				bodgen()
			]);
		};
		n.refresh();
		return n;
	},
	image: function(d, iprop, title, collapsible) {
		iprop = iprop || "image";
		var inode = CT.dom.img(d[iprop], "w1"), dd = CT.file.dragdrop(function(ctfile) {
			ctfile.upload("/_db", function(ilink) {
				inode.src = d[iprop] = ilink;
			}, {
				action: "blob",
				key: d.key,
				property: iprop
			});
		}), name = title || iprop, dbutt = CT.dom.button("remove",
			function() {
				var edata = { key: d.key };
				d[iprop] = edata[iprop] = null;
				CT.db.put(edata, function(newd) {
					inode.src = "";
				});
			}, "right");
		return CT.dom.div([
			dbutt,
			collapsible ? man.util.collapser(name) : name,
			inode,
			dd
		], core.config.ctman.classes[d.modelName].image);
	},
	sideslide: function() {
		var b = CT.dom.button("retract side bar", function() {
			b._re = !b._re;
			b.innerHTML = (b._re ? "expand" : "retract") + " side bar";
			CT.dom.className("ctcontent").forEach(function(n) {
				n.classList[b._re ? "add" : "remove"]("noside");
			});
		}, "abs cbl");
		return b;
	},
	minmax: function(top, mid, bottom) {
		var fullt = function() {
			mid.style.top = top.style.height = "calc(90% - 15px)";
			bottom.style.height = "calc(10% - 15px)";
		}, fullb = function() {
			mid.style.top = top.style.height = "calc(10% - 15px)";
			bottom.style.height = "calc(90% - 15px)";
		}, same = function() {
			mid.style.top = top.style.height = bottom.style.height = "calc(50% - 15px)";
		}, n = CT.dom.div([
			CT.dom.button("Template Screen", fullt),
			CT.dom.button("Section Screen", fullb),
			CT.dom.button("Split Screen", same)
		], "abs ctr");
		n.top = fullt;
		n.bottom = fullb;
		n.same = same;
		return n;
	},
	help: function() {
		var hcfg = core.config.ctman.help,
			pname = location.pathname.slice(5, -5) || "documents";
		CT.modal.modal([
			CT.dom.div(pname + " page", "biggest centered"),
			CT.dom.div(hcfg[pname], "kidvp")
		]);
	},
	inject: function(content) {
		tinyMCE.activeEditor.selection.setContent(content);
	},
	builder: function(bdata) {
		var showBuild = function() {
			var bp = "/" + bdata.build;
			CT.modal.modal([
				CT.dom.iframe(bp),
				CT.dom.link("click here to open in a new tab",
					null, bp, "centered block", null, null, true)
			]);
		}, showMessage = function() {
			CT.modal.modal([
				CT.dom.div("Issues Encountered", "big centered"),
				bdata.message
			], bdata.success && showBuild);
		};
		bdata.message ? showMessage() : showBuild();
	}
};