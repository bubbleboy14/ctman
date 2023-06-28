man.relations = {
	_: {
		parentage: {},
		selector: function(cb) {
			var iz = man.relations._.images;
			if (!iz.length) return alert("no images uploaded yet!");
			CT.modal.prompt({
				prompt: "please select an image",
				style: "icon",
				recenter: true,
				className: "basicpopup mosthigh flex col galimg h400p",
				data: iz,
				cb: cb
			});
		},
		uploader: function(cb) {
			CT.modal.prompt({
				prompt: "select the file you wish to upload",
				style: "file",
				cb: function(ctfile) {
					ctfile.upload("/_db", function(ilink) {
						man.relations._.images.push(ilink);
						cb(ilink);
					}, {
						action: "blob"
					});
				}
			});
		}
	},
	images: function(cb) {
		var _ = man.relations._;
		CT.modal.choice({
			prompt: "select existing image or upload a new one?",
			data: ["select", "upload"],
			cb: function(sel) {
				if (sel == "select")
					_.selector(cb);
				else
					_.uploader(cb);
			}
		});
	},
	ancestors: function(key) {
		var p, pg = man.relations._.parentage, az = [];
		if (pg[key]) {
			az = az.concat(pg[key]);
			for (p of pg[key])
				az = az.concat(man.relations.ancestors(p));
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
	},
	init: function() {
		CT.db.blobs("image", function(iz) {
			man.relations._.images = iz;
		});
	}
};