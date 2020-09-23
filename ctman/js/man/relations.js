man.relations = {
	_: { parentage: {} },
	images: function(cb) {
		CT.modal.prompt({
			prompt: "please select an image",
			style: "icon",
			recenter: true,
			className: "basicpopup mosthight galimg",
			data: man.relations._.images,
			cb: cb
		});
	},
	imaginate: function(items) {
		var _ = man.relations._;
		_.images = items.filter(i => i.image).map(i => i.image);
	},
	ancestors: function(key) {
		var p, pg = man.relations._.parentage, az = [];
		if (pg[key]) {
			az = az.concat(pg[key]);
			for (p of pg[key])
				az = az.concat(man.util.ancestors(p));
		}
		return az;
	},
	geneologize: function(items) {
		var par = man.relations._.parentage, item, section;
		for (item of items) {
			for (section of item.sections) {
				if (!par[section])
					par[section] = [];
				par[section].push(item.key);
			}
		}
	}
};