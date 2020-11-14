man.injections = {
	_: {
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
		var _ = man.injections._, pushit = function(iz) {
			d.injections = iz.map(i => i.key);
			CT.db.put({
				key: d.key,
				injections: d.injections
			}, n.refresh);
		}, niv = "new insertion variable";
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
							pushit(iz);
						});
					} else
						pushit(iz);
				}
			});
		};
	},
	editor: function(d) {
		var classes = core.config.ctman.classes.template;
		return man.util.refresher("injections", "edit insertion variables",
			n => this.button(d, n), function() {
				return d.injections.map(function(ikey) {
					var i = CT.data.get(ikey);
					return CT.dom.div(i.name + " (" + i.variety + ")",
						classes.injection);
				});
			}, classes.injections);
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
		CT.db.get("injection", function(iz) {
			man.injections._.injections = iz;
		});
	}
};