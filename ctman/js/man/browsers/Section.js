man.browsers.Section = CT.Class({
	CLASSNAME: "man.browsers.Section",
	goodsecs: function(d, secs) {
		return true;
	},
	asec: function(d, n) {
		var sbro = this.opts.sections || this,
			nonoz = [d.key].concat(d.sections),
			goodsecs = this.goodsecs;
		nonoz = nonoz.concat(man.relations.ancestors(d.key));
		return function() {
			items = sbro._.items.filter(i => !nonoz.includes(i.key));
			items.length ? CT.modal.choice({
				prompt: "please select a section",
				data: items,
				style: "multiple-choice",
				cb: function(sz) {
					if (!goodsecs(d, sz)) return;
					d.sections = d.sections.concat(sz.map(s => s.key));
					CT.db.put({
						key: d.key,
						sections: d.sections
					}, n.refresh);
				}
			}) : alert('click "new section" to create a new section');
		};
	},
	move: function(key, d, shnode, e) {
		var options = [], freshies = this.refreshers;
		if (key != d.sections[0])
			options.push("up");
		options.push("remove");
		if (key != d.sections[d.sections.length - 1])
			options.push("down");
		CT.modal.choice({
			prompt: "shift or remove?",
			data: options,
			cb: function(move) {
				var i = CT.dom.childNum(shnode),
					el = d.sections.splice(i, 1)[0];
				if (move == "remove")
					shnode.remove();
				else if (move == "up") {
					d.sections.splice(i - 1, 0, el);
					shnode.parentNode.insertBefore(shnode, shnode.previousSibling);
				} else {
					d.sections.splice(i + 1, 0, el);
					if (shnode.nextSibling.nextSibling)
						shnode.parentNode.insertBefore(shnode, shnode.nextSibling.nextSibling);
					else
						shnode.parentNode.appendChild(shnode);
				}
				CT.db.put({
					key: d.key,
					sections: d.sections
				});
			}
		});
		e && e.stopPropagation();
	},
	section: function(key, d) {
		var oz = this.opts, n = CT.dom.div(null, "choice_cell", null, {
			onclick: function() {
				CT.dom.id("tl" + key).trigger();
				oz.onsection && oz.onsection();
			}
		});
		CT.db.one(key, function(s) { // meh shouldn't be necessary...
			CT.dom.setContent(n, [
//				CT.dom.button("move", e => mover(key, d, n, e), "right"),
				oz.canedit && CT.dom.button("remove", function(e) {
					d.sections.splice(CT.dom.childNum(n), 1);
					n.remove();
					CT.db.put({
						key: d.key,
						sections: d.sections
					});
					e.stopPropagation();
				}, "right"),
				s.name
			]);
		});
		return n;
	},
	sections: function(d) {
		var sec = this.section, canedit = this.opts.canedit;
		return man.util.refresher("sections", "add section",
			n => this.asec(d, n), function() {
//				return d.sections.map(s => sec(s, d));
				if (!canedit)
					return CT.dom.div(d.sections.map(sec));
				return CT.dom.dragList(d.sections, k => sec(k, d), function(secs) {
					d.sections = secs;
					CT.db.put({
						key: d.key,
						sections: d.sections
					});
				});
			}, core.config.ctman.classes[d.modelName].sections, false, null, canedit);
	},
	prebutt: function(d) {
		var _ = this._, pbutt = CT.dom.button("PDF Preview", function() {
			pbutt.disabled = true;
			man.builder.build(d, function(bdata) {
				man.builder.builder(bdata);
				pbutt.disabled = false;
			});
		});
		return pbutt;
	},
	delbutt: function(d) {
		return CT.dom.button("delete", function() {
			man.util.m(d, function(embedders) {
				CT.modal.modal([
					CT.dom.div("this section is embedded in " + embedders.length + " places",
						"bigger"),
					embedders.map(e => e.name),
					CT.dom.button("click here to delete it anyway", function() {
						if (!(confirm("really delete this section?") && confirm("really?")))
							return;
						CT.db.put(d.key, function() {
							alert("ok, you asked for it!");
							location.reload(); // meh
						}, "delete", "key");
					}, "big red w1")
				]);
			}, "embedders");
		}, "red");
	},
	boolcheck: function(d, name) {
		var _ = this._, eoz, saveThen = this.saveThen;
		return CT.dom.checkboxAndLabel(name, d[name],
			null, null, "inline rmargined", function(cb) {
				CT.log("saving pre bool set");
				saveThen(function() {
					CT.log("setting bool");
					eoz = { key: d.key };
					d[name] = eoz[name] = cb.checked;
					_.edit(eoz, true, null, true);
				});
			}
		);
	},
	rightbutts: function(d) {
		if (!d.key || !this.opts.rightbutts) return;
		var cont = [
			this.boolcheck(d, "headerless"),
			this.boolcheck(d, "landscape")
		];
		man.util.can("build") && cont.push(this.prebutt(d));
		return CT.dom.div(cont, "abs ctr bordered round shiftup");
	},
	leftbutts: function(d) {
		if (!d.key || !this.opts.leftbutts) return;
		return CT.dom.div([
			this.delbutt(d)
		], "abs ctl bordered round shiftup");
	},
	choosevar: function(d, cb) {
		CT.modal.prompt({
			prompt: "what's the insertion variable?",
			cb: cb
		})
	},
	injectors: function(d) {
		var cvar = this.choosevar;
		return CT.dom.div([
//			CT.dom.button("insert variable", function() {
//				cvar(d, function(ivar) {
//					man.util.inject("{{" + ivar + "}}");
//				});
//			}),
			CT.dom.button("insert image", function() {
				man.relations.images(function(img) {
					man.util.inject("<img style='display: block; max-width: 100%' src='" + img + "'>");
				});
			}),
			man.tables.button(),
			man.tables.chembutt()
		], "right");
	},
	saveThen: function(cb) {
		this._afterSave = cb;
		this.formWrapper.form.continue();
	},
	doAfterSave: function() {
		if (this._afterSave) {
			this._afterSave();
			delete this._afterSave;
		}
	},
	saveMe: function(vals) {
		var d = man.util.current[this.opts.modelName];
		for (val in vals)
			d[val] = vals[val];
		this._.edit(d.key ? CT.merge({
			key: d.key
		}, vals) : d, true, this.doAfterSave);
	},
	view: function(d) {
		man.util.current[this.opts.modelName] = d;
		if (this.opts.canedit) {
			this.formWrapper = man.util.form(d, "template", this.saveMe, {
				description: ta => this.injectors(d)
			});
		} else
			this.formWrapper = CT.dom.div(d.description);
		CT.dom.setContent(this._.nodes.content, [
			this.leftbutts(d),
			this.rightbutts(d),
			this.namer(d),
			this.formWrapper,
			this.extra(d)
		]);
	},
	extra: function(d) {
		return d.key && [
			this.opts.canedit ? man.util.image(d) : CT.dom.img(d.image, "w1"),
			this.sections(d)
		];
	},
	defaults: function() {
		return {
			sections: []
		};
	},
	items: function(items) {
		man.relations.geneologize(items);
	},
	onFresh: function(data) {
		var g = man.util.group(), gset = this.gset, eobj = {};
		if (!g) return;
		g[gset].push(data.key);
		eobj[gset] = g[gset];
		eobj.key = g.key;
		CT.db.put(eobj);
	},
	init: function(opts) {
		this.opts = CT.merge(opts, {
			owner: false,
			leftbutts: true,
			rightbutts: true,
			modelName: "section",
			saveMessage: "you saved!",
			keys: man.util.group("sections"),
			canedit: man.util.can("edit section"),
			cancreate: man.util.can("create section"),
			blurs: ["section name", "section title", "name that section"]
		}, this.opts);
		man.tables.init();
		man.relations.init();
		this.gset = "sections";
	}
}, CT.Browser);