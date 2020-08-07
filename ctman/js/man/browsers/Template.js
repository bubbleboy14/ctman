man.browsers.Template = CT.Class({
	CLASSNAME: "man.browsers.Template",
	view: function(d) {
		var _ = this._, mcfg = core.config.ctman, val;
		CT.dom.setContent(_.nodes.content, [
			CT.dom.div(d.name, "bigger centered"),
			CT.layout.form({
				button: true,
				labels: true,
				bname: "save",
				values: d,
				items: mcfg.template, // just desc for now...
				cb: function(vals) {
					for (val in vals)
						d[val] = vals[val];
					_.edit(d.key ? CT.merge({
						key: d.key
					}, vals) : d);
				}
			})
		]);
	},
	defaults: function() {
		return {
			sections: []
		};
	},
	init: function(opts) {
		this.opts = CT.merge(opts, {
			modelName: "template",
			blurs: ["template name", "template title", "name that template"]
		}, this.opts);
	}
}, CT.Browser);