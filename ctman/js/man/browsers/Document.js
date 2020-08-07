man.browsers.Document = CT.Class({
	CLASSNAME: "man.browsers.Document",
	build: function(d) {
		var n = CT.dom.div(null, "margined padded bordered round");
		n.refresh = function() {
			CT.dom.setContent(n, [
				"pdf build",
				d.pdf && CT.dom.link("click here to download", null, d.pdf, "block"),
				CT.dom.button("click here to build/rebuild", function() {
					CT.net.post({
						path: "/_man",
						params: {
							key: d.key
						},
						cb: function(newd) {
							d.pdf = newd.pdf;
							n.refresh();
						}
					});
				})
			]);
		};
		n.refresh();
		return n;
	},
	hazards: function(d) {
		var hcfg = core.config.ctman.hazards.chemical,
			cz = CT.dom.choices(hcfg.map(h => CT.dom.div(h)), true),
			selz = d.assembly.hazards.chemical;
		selz && CT.dom.each(cz, function(sel) {
			if (selz.includes(sel.innerHTML))
				sel.onclick();
		});
		return cz;
	},
	view: function(d) {
		var _ = this._, haz = this.hazards(d),
			mcfg = core.config.ctman, view = this.view;
		CT.dom.setContent(_.nodes.content, [
			CT.dom.div(d.name, "bigger centered"),
			CT.dom.div([
				"hazards",
				haz
			], "margined padded bordered round"),
			CT.dom.div([
				"injections",
				CT.layout.form({
					button: true,
					labels: true,
					bname: "save",
					values: d.injections,
					items: mcfg.injections,
					cb: function(vals) {
						d.injections = vals;
						d.assembly = {
							hazards: {
								chemical: haz.value.map(v => mcfg.hazards.chemical[v])
							}
						};
						_.edit(d.key ? {
							key: d.key,
							assembly: d.assembly,
							injections: d.injections
						} : d);
					}
				}),
			], "margined padded bordered round"),
			d.key && this.build(d)
		]);
	},
	defaults: function() {
		return {
			assembly: {
				hazards: {
					chemical: []
				}
			}
		};
	},
	init: function(opts) {
		this.opts = CT.merge(opts, {
			modelName: "document",
			blurs: ["project name", "document title", "project/document name"]
		}, this.opts);
	}
}, CT.Browser);