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
		}), name = title || iprop;
		return CT.dom.div([
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
	minmax: function(top, bottom) {
		var fullt = function() {
			top.style.height = "90%";
			bottom.style.height = "10%";
		}, fullb = function() {
			top.style.height = "10%";
			bottom.style.height = "90%";
		}, same = function() {
			top.style.height = bottom.style.height = "50%";
		}, n = CT.dom.div([
			CT.dom.button("templates", fullt),
			CT.dom.button("sections", fullb),
			CT.dom.button("equal", same)
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
	}
};