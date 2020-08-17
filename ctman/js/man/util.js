man.util = {
	form: function(d, fname, cb, extra) {
		return CT.dom.div([
			d[fname] && fname,
			CT.layout.form({
				cb: cb,
				extra: extra,
				button: true,
				labels: true,
				bname: "save",
				values: d[fname] || d,
				items: core.config.ctman[fname]
			}),
		], "margined padded bordered round");
	},
	refresher: function(title, buttname, buttcb, bodgen) {
		var n = CT.dom.div(null, "margined padded bordered round"),
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
		], "margined padded bordered round");
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
	}
};