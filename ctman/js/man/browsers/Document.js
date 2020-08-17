man.browsers.Document = CT.Class({
	CLASSNAME: "man.browsers.Document",
	builder: function(d, n) {
		return function() {
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
		};
	},
	build: function(d) {
		return man.util.refresher("pdf build",
			"click here to build/rebuild", n => this.builder(d, n),
			_ => d.pdf && CT.dom.link("click here to download",
				null, d.pdf, "block", null, null, true));
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
	swaptemp: function(d, n) {
		var _ = this._, bs = this.buildSecs;
		return function() {
			_.templates.length ? CT.modal.choice({
				prompt: "please select a template",
				data: ["default (static)"].concat(_.templates),
				cb: function(tmp) {
					var upobj = { key: d.key };
					d.template = (tmp == "default (static)") ? null : tmp.key;
					bs(d);
					upobj.template = d.template;
					upobj.assembly = d.assembly;
					CT.db.put(upobj, n.refresh);
				}
			}) : alert("create a template on the templates page");
		};
	},
	_bs: function(d) {
		var cz = this._secmap[d.key], actives = cz && cz.value;
		return {
			key: d.key,
			sections: d.sections.filter(function(sec, i) {
				return actives && actives.includes(i);
			}).map(this._bs)
		};
	},
	buildSecs: function(d) {
		if (!d.template) {
			delete d.assembly.sections;
			return;
		}
		d.assembly.sections = this._bs(CT.data.get(d.template)).sections;
	},
	_secmap: {},
	_onmap: {},
	upons: function(d) {
		var s;
		this._onmap[d.key] = d.sections.map(function(s, i) {
			return i;
		});
		for (s of d.sections)
			this.upons(s);
	},
	section: function(d) {
		var cz = CT.dom.choices(d.sections.map(this.section), true),
			ons = this._onmap[d.key];
		this._secmap[d.key] = cz;
		ons && CT.dom.each(cz, function(sel, i) {
			if (ons.includes(i))
				sel.onclick();
		});
		return CT.dom.div([
			d.name,
			cz
		]);
	},
	sections: function(d) {
		if (!d.template) return CT.dom.div("default (static)", "centered");
		this.upons({ key: d.template, sections: d.assembly.sections || [] });
		return this.section(CT.data.get(d.template));
	},
	template: function(d) {
		return man.util.refresher("template", "swap",
			n => this.swaptemp(d, n), _ => this.sections(d));
	},
	view: function(d) {
		var _ = this._, haz = this.hazards(d),
			mcfg = core.config.ctman, view = this.view,
			bs = this.buildSecs;
		CT.dom.setContent(_.nodes.content, [
			CT.dom.div(d.name, "bigger centered"),
			d.key && this.template(d),
			CT.dom.div([
				"hazards",
				haz
			], "margined padded bordered round"),
			man.util.form(d, "injections", function(vals) {
				d.injections = vals;
				d.assembly = {
					hazards: {
						chemical: haz.value.map(v => mcfg.hazards.chemical[v])
					}
				};
				bs(d); // adds assembly.sections[]
				_.edit(d.key ? {
					key: d.key,
					assembly: d.assembly,
					injections: d.injections
				} : d);
			}),
			d.key && man.util.image(d, "logo", "client logo"),
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
		var _ = this._;
		this.opts = CT.merge(opts, {
			modelName: "document",
			blurs: ["project name", "document title", "project/document name"]
		}, this.opts);
		CT.db.get("template", function(tz) {
			_.templates = tz;
		}, 1000, 0, null, null, null, null, "unrolled");
	}
}, CT.Browser);