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
	move: function(key, d, shnode) {
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
	},
	section: function(key, d) {
		var oz = this.opts, n = CT.dom.div(null, "choice_cell", null, {
			onclick: function() {
				CT.dom.id("tl" + key).trigger();
				oz.onsection && oz.onsection();
			}
		}), mover = this.move;
		CT.db.one(key, function(s) { // meh shouldn't be necessary...
			CT.dom.setContent(n, [
				CT.dom.button("move", _ => mover(key, d, n), "right"),
				s.name
			]);
		});
		return n;
	},
	sections: function(d) {
		var sec = this.section;
		return man.util.refresher("sections", "add section",
			n => this.asec(d, n), function() {
				return d.sections.map(s => sec(s, d));
			}, core.config.ctman.classes[d.modelName].sections);
	},
	unheader: function(d) {
		var _ = this._;
		if (!d.key || !this.opts.headerlessness) return;
		return CT.dom.checkboxAndLabel("headerless", d.headerless,
			null, null, "abs ctr bordered round shiftup", function(cb) {
				_.edit({
					key: d.key,
					headerless: cb.checked
				});
			});
	},
	choosevar: function(d, cb) {
		CT.modal.prompt({
			prompt: "what's the injection variable?",
			cb: cb
		})
	},
	inject: function(ta, d) {
		var cvar = this.choosevar;
		return CT.dom.button("inject variable", function() {
			cvar(d, function(ivar) {
				tinyMCE.activeEditor.selection.setContent("{{" + ivar + "}}");
			});
		}, "right");
	},
	namer: function(d) {
		var n = CT.dom.div(d.name, "bigger centered pointer");
		n.onclick = function() {
			var sf = CT.dom.smartField({
				value: d.name,
				cb: function(name) {
					if (name == d.name) return;
					CT.db.put({
						key: d.key,
						name: name
					}, function(newd) {
						d.name = newd.name;
						d.label = newd.label;
						CT.dom.setContent(n, d.name);
						CT.dom.setContent(CT.dom.id("tl" + d.key).firstChild,
							d.label);
					});
				}
			});
			CT.dom.setContent(n, sf);
			sf.focus();
		};
		return n;
	},
	view: function(d) {
		var _ = this._, mcfg = core.config.ctman, val;
		CT.dom.setContent(_.nodes.content, [
			this.unheader(d),
			this.namer(d),
			man.util.form(d, "template", function(vals) {
				for (val in vals)
					d[val] = vals[val];
				_.edit(d.key ? CT.merge({
					key: d.key
				}, vals) : d);
			}, {
				description: ta => this.inject(ta, d)
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
			headerlessness: true,
			modelName: "section",
			blurs: ["section name", "section title", "name that section"]
		}, this.opts);
	}
}, CT.Browser);