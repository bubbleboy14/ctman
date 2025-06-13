man.browsers.Document = CT.Class({
	CLASSNAME: "man.browsers.Document",
	builder: function(d, n) {
		var _ = this._, doBuild = function() {
			man.builder.build(d, function(rdata) {
				if (rdata.build.success) {
					d.pdf = rdata.doc.pdf;
					n.refresh();
				}
				man.builder.builder(rdata.build, true, d);
			});
		}, saver = this.save;
		return function() {
			_.shouldSave ? saver(d, doBuild) : doBuild();
		};
	},
	build: function(d) {
		return man.util.refresher("pdf build",
			"click here to build/rebuild", n => this.builder(d, n),
			_ => d.pdf && CT.dom.link("click here to download",
				null, d.pdf, "block", null, null, true),
			core.config.ctman.classes.document.build, false, null, true);
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
	buildSecs: function(d) {
		if (!d.assembly)
			d.assembly = {};
		if (!d.template) {
			delete d.assembly.sections;
			return;
		}
		d.assembly.sections = man.builder.assemble(CT.data.get(d.template), this._secmap).sections;
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
		var cz = CT.dom.choices(d.sections.map(this.section), true, null, null, function() {
			_.shouldSave = true;
		}), ons = this._onmap[d.key], _ = this._;
		this._secmap[d.key] = cz;
		CT.data.add(d);
		ons && CT.dom.each(cz, function(sel, i) {
			if (ons.includes(sel._id))
				sel.onclick();
		});
		var n = CT.dom.div([
			d.name,
			cz
		]);
		cz.clickable = this.opts.canedit;
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
			core.config.ctman.classes.document.template, true, null, this.opts.canedit);
	},
	scheck: function(d, p, n) {
		n = n || "include " + p.replace(/_/g, " ");
		if (!this.opts.canedit)
			return CT.dom.div(p + ": " + d[p]);
		return CT.dom.checkboxAndLabel(n,
			d[p], null, null, null, function(cb) {
				var evars = { key: d.key };
				evars[p] = cb.checked;
				CT.db.put(evars);
			});
	},
	settings: function(d) {
		var scheck = this.scheck, mcfg = core.config.ctman,
			fcfg = mcfg.fonts, fz = fcfg.options;
		var cont = [
			man.util.collapser("settings"),
			["signup_sheet", "table_of_contents", "declaration_page", "section_page_breaks"].map(function(p) {
				return scheck(d, p);
			}).concat([scheck(d, "pretty_filenames",
				"use pretty (titled and revisioned) filenames")])
		];
		if (this.opts.canedit) {
			cont.push(CT.dom.select(fz.map(f => f.replace(/-/g, " ")), fz, null, d.font, fcfg.default, function(fname) {
				CT.db.put({
					key: d.key,
					font: fname
				});
			}, null, true));
		} else
			cont.push(scheck(d, "font"));
		return CT.dom.div(cont, mcfg.classes.document.settings);
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
	save: function(d, cb, noreview) {
		var _ = this._;
		this.log("saving");
		_.shouldSave = false;
		this.buildSecs(d); // adds assembly.sections[]
		_.edit(d.key ? {
			key: d.key,
			assembly: d.assembly,
			injections: d.injections
		} : d, noreview, cb);
	},
	image: function(d) {
		return this.opts.canedit ? man.util.image(d, "logo", "client logo", true) : CT.dom.img(d.logo, "w1");
	},
	injections: function(d) {
		var save = this.save;
		if (!this.opts.canedit) {
			return CT.dom.div([
				CT.dom.div("injections", "big"),
				Object.keys(d.injections).map(k => k + ": " + d.injections[k])
			], "bordered padded margined round");
		}
		return man.util.form(d, "injections", function(vals) {
			d.injections = vals;
			save(d);
		}, null, d.template && man.injections.fields(CT.data.get(d.template)), true);
	},
	view: function(d) {
		var _ = this._,// haz = this.hazards(d),
			mcfg = core.config.ctman, mu = man.util,
			classes = mcfg.classes.document;
		mu.current.document = d;
		CT.dom.setContent(_.nodes.content, [
			this.namer(d, classes.title),
			d.key && this.template(d),
//			CT.dom.div([
//				"hazards",
//				haz
//			], classes.hazards),
			this.injections(d),
			d.key && this.image(d),
			d.key && this.settings(d),
			d.key && mu.can("build") && this.build(d)
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
			canedit: man.util.can("edit document"),
			cancreate: man.util.can("create document"),
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