man.builder = {
	build: function(d, cb) {
		man.util.m(d, cb, "build");
	},
	sequential(d) {
		man.util.current.sequential = new man.builder.Sequential({ document: d });
	},
	failer: function(d) {
		return function() {
			CT.modal.choice({
				prompt: "perform sequential build?",
				data: ["yes", "no"],
				cb: (sel) => (sel == "yes") && man.builder.sequential(d)
			});
		};
	},
	builder: function(bdata, onfail, d) {
		if (onfail == true)
			onfail = man.builder.failer(d);
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

man.builder.Sequential = CT.Class({
	CLASSNAME: "man.builder.Sequential",
	increment: function(build) {
		if (build) {
			var worked = build.success;
			this.nodes[this.index].classList.add(worked ? "green" : "red");
			if (!worked) return;
		}
		this.index += 1;
		(this.index < this.sections.length) && this.buildNext();
	},
	buildNext: function() {
		var sec = this.sections[this.index];
		if (this.assemSecs.length && !this.assemKeys.includes(sec.key))
			this.increment();
		else
			man.builder.build(sec, this.increment);
	},
	launch: function() {
		CT.modal.modal(this.nodes);
		this.buildNext();
	},
	load: function() {
		this.index = 0;
		this.document = this.opts.document;
		this.template = CT.data.get(this.document.template);
		this.sections = this.template.sections;
		this.assemSecs = this.document.assembly.sections;
		this.assemKeys = this.assemSecs.map(s => s.key);
		this.nodes = this.sections.map(s => CT.dom.div(s.name));
	},
	init: function(opts) {
		this.opts = opts;
		this.load();
		this.launch();
	}
});