man.injections = {
	_: {
		inew: function(cb) {
			CT.modal.prompt({
				prompt: "what's the new injection variable's name?",
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
		}, niv = "new injection variable";
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
		return man.util.refresher("injections", "edit injection variables",
			n => this.button(d, n), function() {
				return d.injections.map(function(ikey) {
					var i = CT.data.get(ikey);
					return CT.dom.div(i.name + " (" + i.variety + ")",
						"margined padded bordered round inline-block");
				});
			});
	},
	init: function() {
		CT.db.get("injection", function(iz) {
			man.injections._.injections = iz;
		});
	}
};