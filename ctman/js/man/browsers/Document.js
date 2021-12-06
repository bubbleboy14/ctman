man.browsers.Document = CT.Class({
	CLASSNAME: "man.browsers.Document",
	builder: function(d, n) {
		return function() {
			CT.net.post({
				spinner: true,
				path: "/_man",
				params: {
					key: d.key
				},
				cb: function(rdata) {
					if (rdata.build.success) {
						d.pdf = rdata.doc.pdf;
						n.refresh();
					}
					man.util.builder(rdata.build);
				}
			});
		};
	},
	build: function(d) {
		return man.util.refresher("pdf build",
			"click here to build/rebuild", n => this.builder(d, n),
			_ => d.pdf && CT.dom.link("click here to download",
				null, d.pdf, "block", null, null, true),
			core.config.ctman.classes.document.build);
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
	seltemp: function(cb, cbstat) {
		CT.modal.choice({
			prompt: "please select a template",
			data: ["default (static)"].concat(this._.templates),
			cb: function(tmp) {
				if (cbstat && tmp == "default (static)")
					return cbstat();
				cb(tmp);
			}
		});
	},
	swaptemp: function(d, n) {
		var _ = this._, bs = this.buildSecs, st = this.seltemp;
		return function() {
			_.templates.length ? st(function(tmp) {
				d.template = (tmp == "default (static)") ? null : tmp.key;
				bs(d);
				CT.db.put({
					key: d.key,
					template: d.template,
					assembly: d.assembly
				}, n.refresh);
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
		if (!d.assembly)
			d.assembly = {};
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
			return s.key;
		});
		for (s of d.sections)
			this.upons(s);
	},
	section: function(d) {
		var cz = CT.dom.choices(d.sections.map(this.section), true),
			ons = this._onmap[d.key];
		this._secmap[d.key] = cz;
		ons && CT.dom.each(cz, function(sel, i) {
			if (ons.includes(sel._id))
				sel.onclick();
		});
		var n = CT.dom.div([
			d.name,
			cz
		]);
		n._id = d.key;
		return n;
	},
	sections: function(d) {
		if (!d.template) return CT.dom.div("default (static)", "centered");
		this.upons({ key: d.template, sections: d.assembly.sections || [] });
		return this.section(CT.data.get(d.template));
	},
	template: function(d) {
		return man.util.refresher("template", "swap",
			n => this.swaptemp(d, n), _ => this.sections(d),
			core.config.ctman.classes.document.template, true);
	},
	scheck: function(d, p, n) {
		n = n || "include " + p.replace(/_/g, " ");
		return CT.dom.checkboxAndLabel(n,
			d[p], null, null, null, function(cb) {
				var evars = { key: d.key };
				evars[p] = cb.checked;
				CT.db.put(evars);
			});
	},
	settings: function(d) {
		var scheck = this.scheck;
		return CT.dom.div([
			man.util.collapser("settings"),
			["signup_sheet", "table_of_contents", "declaration_page", "section_page_breaks"].map(function(p) {
				return scheck(d, p);
			}).concat([scheck(d, "pretty_filenames",
				"use pretty (titled and revisioned) filenames")])
		], core.config.ctman.classes.document.settings);
	},
	declarations: function(d, cb) {
		CT.modal.prompt({
			prompt: CT.dom.div("please provide the following information",
				"padded"),
			style: "form",
			labels: true,
			data: core.config.ctman.declarations,
			cb: function(data) {
				d.declarations = data;
				cb();
			}
		});
	},
	firstview: function(d) {
		var _ = this._, view = this.view, ed = _.edit,
			bs = this.buildSecs, st = this.seltemp;
		this.declarations(d, function() {
			if (!_.templates.length)
				return view(d);
			st(function(tmp) {
				d.template = tmp.key;
				bs(d);
				ed(d);
			}, v => view(d));
		});
	},
	view: function(d) {
		var _ = this._,// haz = this.hazards(d),
			mcfg = core.config.ctman,
			classes = mcfg.classes.document,
			view = this.view, bs = this.buildSecs;
		CT.dom.setContent(_.nodes.content, [
			this.namer(d, classes.title),
			d.key && this.template(d),
//			CT.dom.div([
//				"hazards",
//				haz
//			], classes.hazards),
			man.util.form(d, "injections", function(vals) {
				d.injections = vals;
//				d.assembly = {
//					hazards: {
//						chemical: haz.value.map(v => mcfg.hazards.chemical[v])
//					}
//				};
				bs(d); // adds assembly.sections[]
				_.edit(d.key ? {
					key: d.key,
					assembly: d.assembly,
					injections: d.injections
				} : d);
			}, null, d.template && man.injections.fields(CT.data.get(d.template)),
				true),
			d.key && man.util.image(d, "logo", "client logo", true),
			d.key && this.settings(d),
			d.key && this.build(d)
		]);
	},
	defaults: function() {
		return {
			injections: {},
			assembly: {
//				hazards: {
//					chemical: []
//				}
			}
		};
	},
	init: function(opts) {
		var _ = this._;
		this.opts = CT.merge(opts, {
			modelName: "document",
			opener: "Step 1. Start New HASP Here",
			blurs: ["project name", "document title", "project/document name"],
			prebuild: function(items) {
				CT.db.get("template", function(tz) {
					_.templates = tz;
					_.build(items);
				}, 1000, 0, null, null, null, null, "unrolled");
			}
		}, this.opts);
		man.injections.init();
	}
}, CT.Browser);