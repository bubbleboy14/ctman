man.injections = {
	_: {},
	button: function(d, n) {
		return function() {
			CT.modal.choice({
				style: "multiple-choice",
				data: man.injections._.injections,
				selections: d.injections.map(i => CT.data.get(i)),
				cb: function(iz) {
					d.injections = iz.map(i => i.key);
					CT.db.put({
						key: d.key,
						injections: d.injections
					}, n.refresh);
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