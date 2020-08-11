man.browsers.Section = CT.Class({
	CLASSNAME: "man.browsers.Section",
	asec: function(d, n) {
		var sbro = this.opts.sections || this,
			nonoz = [d.key].concat(d.sections);
		return function() {
			items = sbro._.items.filter(i => !nonoz.includes(i.key));
			items.length ? CT.modal.choice({
				prompt: "please select a section",
				data: items,
				style: "multiple-choice",
				cb: function(sz) {
					d.sections = d.sections.concat(sz.map(s => s.key));
					CT.db.put({
						key: d.key,
						sections: d.sections
					}, n.refresh);
				}
			}) : alert('click "new section" to create a new section');
		};
	},
	section: function(key) {
		var s = CT.data.get(key);
		return CT.dom.div(s.name, "choice_cell", null, {
			onclick: function() {
				CT.dom.id("tl" + key).trigger();
			}
		});
	},
	sections: function(d) {
		return man.util.refresher("sections", "add section",
			n => this.asec(d, n), _ => d.sections.map(this.section));
	},
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
			}),
			this.extra(d)
		]);
	},
	extra: function(d) {
		return d.key && [
			man.util.image(d),
			this.sections(d)
		];
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