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
	}
};