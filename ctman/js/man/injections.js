man.injections = {
	_: {
		names: {},
		inew: function(cb) {
			CT.modal.prompt({
				prompt: "what's the new insertion variable's name?",
				cb: function(name) {
					CT.modal.choice({
						prompt: "what kind of variable is it?",
						data: ["text", "text block"],
						cb: function(variety) {
							CT.db.put({
								modelName: "injection",
								name: name,
								variety: variety
							}, function(ivar) {
								man.injections._.injections.push(ivar);
								cb(ivar);
							});
						}
					});
				}
			})
		},
		d2iz: function(d) {
			return d.split("{{").filter(p => p.includes("}}")).map(i => i.split("}}")[0]);
		}
	},
	get: function(name) {
		return man.injections._.names[name];
	},
	pushit = function(iz, d) {
		d.injections = iz.map(i => i.key);
		CT.db.put({
			key: d.key,
			injections: d.injections
		}, _.n && _.n.refresh);
	},
	fields: function(template) {
		return template.injections.map(function(ikey) {
			var i = CT.data.get(ikey), d = {
				name: i.name
			};
			if (i.variety == "text block")
				d.isTA = true;
			return d;
		});
	},
	button: function(d, n) {
		var _ = man.injections._, niv = "new insertion variable";
		_.node = n;
		return function() {
			CT.modal.choice({
				style: "multiple-choice",
				data: [niv].concat(_.injections),
				selections: d.injections.map(i => CT.data.get(i).name),
				cb: function(iz) {
					if (iz.includes(niv)) {
						_.inew(function(ivar) {
							CT.data.remove(iz, niv);
							iz.push(ivar);
							man.injections.pushit(iz, d);
						});
					} else
						man.injections.pushit(iz, d);
				}
			});
		};
	},
	inode: function(i) {
		var classes = core.config.ctman.classes.template,
			itag = "{{" + i.name + "}}";
		return CT.dom.div(i.name + " (" + (i.variety || "core") + ")",
			classes.injection, null, {
				draggable: true,
				onclick: () => man.util.inject(itag),
				ondragstart: function(ev) {
					ev.dataTransfer.dropEffect = "copy";
					ev.dataTransfer.setData("text/plain", itag);
				}
			});
	},
	editor: function(d) {
		var mcfg = core.config.ctman,
			classes = mcfg.classes.template,
			titnode = CT.dom.div(null, "left w195p pl10");
		return man.util.refresher(titnode, "edit insertion variables",
			n => this.button(d, n), function() {
				var inodez = d.injections.map(function(ikey) {
					return man.injections.inode(CT.data.get(ikey));
				});
				if (mcfg.injeclarations)
					inodez = inodez.concat(mcfg.declarations.map(man.injections.inode));
				var ilist = CT.dom.div(inodez, classes.injections);
				CT.dom.setContent(titnode, CT.dom.filter(ilist,
					"filter insertion variables", "inline-block"));
				return ilist;
			}, "block", null, "abs l0 b0 w160p ml10");
	},
	extract: function(secs) {
		var injections = [], sec,
			ex = man.injections.extract,
			d2iz = man.injections._.d2iz;
		for (sec of secs) {
			injections = injections.concat(d2iz(sec.description));
			if (sec.sections.length)
				injections = injections.concat(ex(CT.data.getSet(sec.sections)));
		}
		return injections;
	},
	init: function() {
		var _ = man.injections._;
		CT.db.get("injection", function(iz) {
			_.injections = iz;
			iz.forEach(function(i) {
				_.names[i.name] = i;
			});
		});
	}
};