man.dash = {
	build: function(dox) {
		CT.dom.setContent("ctmain", CT.dom.flex([
			CT.dom.flex(["name", "template", "revision"],
				"row jccenter big bold")
		].concat(dox.map(d => CT.dom.flex([
			d.name, d.template, d.revision
		], "row jccenter"))), "col margined"));
	},
	init: function() {
		CT.db.get("document", man.dash.build, null, null, null, {
			owner: user.core.get("key")
		}, null, null, "summary");
	}
}