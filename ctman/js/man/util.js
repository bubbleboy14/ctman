man.util = {
	form: function(d, fname, cb, extra, items) {
		return CT.dom.div([
			d[fname] && fname,
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
	refresher: function(title, buttname, buttcb, bodgen, classes) {
		var n = CT.dom.div(null, classes || "margined padded bordered round"),
			section = this.section, asec = this.asec;
		n.refresh = function() {
			CT.dom.setContent(n, [
				CT.dom.button(buttname, buttcb(n), "right"),
				title,
				bodgen()
			]);
		};
		n.refresh();
		return n;
	},
	image: function(d, iprop, title) {
		iprop = iprop || "image";
		var inode = CT.dom.img(d[iprop], "w1"), dd = CT.file.dragdrop(function(ctfile) {
			ctfile.upload("/_db", function(ilink) {
				inode.src = d[iprop] = ilink;
			}, {
				action: "blob",
				key: d.key,
				property: iprop
			});
		});
		return CT.dom.div([
			title || iprop,
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
	}
};