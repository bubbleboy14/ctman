man.builder = {
	build: function(d, cb) {
		man.util.m(d, cb, "build");
	},
	sequential(d) {
		var sindex = 0, sec, worked, incBuild = function(build) {
			if (build) {
				worked = build.success;
				secnodes[sindex].classList.add(worked ? "green" : "red");
				if (!worked) return;
			}
			sindex += 1;
			(sindex < secs.length) && buildNext();
		}, buildNext = function() {
			sec = secs[sindex];
			if (asez.length && !askeys.includes(sec.key))
				incBuild();
			else
				man.builder.build(sec, incBuild);
		}, asez = d.assembly.sections, askeys = asez.map(s => s.key),
			secs = CT.data.get(d.template).sections,
			secnodes = secs.map(s => CT.dom.div(s.name));
		CT.modal.modal(secnodes);
		buildNext();
	},
	onfail: function() {
		CT.modal.choice({
			prompt: "perform sequential build?",
			data: ["yes", "no"],
			cb: (sel) => (sel == "yes") && man.builder.sequential(d)
		});
	},
	builder: function(bdata, onfail) {
		if (onfail == true)
			onfail = man.builder.onfail;
		var showBuild = function() {
			var bp = "/" + bdata.build;
			CT.modal.modal([
				CT.dom.iframe(bp),
				CT.dom.link("click here to open in a new tab",
					null, bp, "centered block", null, null, true)
			]);
		}, showMessage = function() {
			CT.modal.modal([
				CT.dom.div("Issues Encountered", "big centered"),
				bdata.message
			], bdata.success ? showBuild : onfail);
		};
		bdata.message ? showMessage() : showBuild();
	}
};