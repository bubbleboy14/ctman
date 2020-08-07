man.util = {
	form: function(d, fname, cb) {
		return CT.dom.div([
			d[fname] && fname,
			CT.layout.form({
				cb: cb,
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
	}
};