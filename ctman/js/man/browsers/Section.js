man.browsers.Section = CT.Class({
	CLASSNAME: "man.browsers.Section",
	view: function(d) {
		var _ = this._, mcfg = core.config.ctman, val;
		CT.dom.setContent(_.nodes.content, [
			CT.dom.div(d.name, "bigger centered"),
			man.util.form(d, "template", function(vals) {
				for (val in vals)
					d[val] = vals[val];
				_.edit(d.key ? CT.merge({
					key: d.key
				}, vals) : d);
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
			owner: false,
			modelName: "section",
			blurs: ["section name", "section title", "name that section"]
		}, this.opts);
	}
}, CT.Browser);