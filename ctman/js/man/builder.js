man.builder = {
	build: function(d, cb) {
		man.util.m(d, cb, "build");
	},
	assemble: function(d, secmap) {
		var cz = secmap && secmap[d.key], actives = cz && cz.value;
		return {
			key: d.key,
			sections: d.sections.filter(function(sec, i) {
				return !actives || (actives && actives.includes(i));
			}).map(s => man.builder.assemble(s, secmap))
		};
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
	_: {
		current: {}
	},
	advance: function() {
		var od = this.opts.ondone;
		this.index += 1;
		(this.index < this.sections.length) ? this.buildNext() : (od && od());
	},
	increment: function(build) {
		var cur = this._.current, sec = cur.section, od = this.opts.ondone;
		if (build) {
			var worked = build.success, node = this.nodes[this.index];
			node.classList.add(worked ? "green" : "red");
			if (!worked) return od && od();
			if (sec.sections.length) {
				var assembly = this.assemSecs.length
					? this.assemSecs[this.assemKeys.indexOf(sec.key)]
					:  man.builder.assemble(sec);
				cur.subseq = new man.builder.Sequential({
					assembly: assembly,
					ondone: this.advance
				});
				return node.after(cur.subseq.node);
			}
		}
		this.advance();
	},
	buildNext: function() {
		var sec = this._.current.section = this.sections[this.index];
		if (this.assemSecs.length && !this.assemKeys.includes(sec.key))
			this.increment();
		else
			man.builder.build(sec, this.increment);
	},
	launch: function() {
		if (this.document)
			CT.modal.modal(this.nodes);
		else
			this.node = CT.dom.div(this.nodes, "tabbed");
		this.buildNext();
	},
	load: function() {
		var oz = this.opts;
		this.index = 0;
		if (oz.document) {
			this.document = oz.document;
			this.template = CT.data.get(this.document.template);
			this.sections = this.template.sections;
			this.assembly = this.document.assembly;
		} else {
			this.assembly = oz.assembly;
			this.section = CT.data.get(this.assembly.key);
			this.sections = this.section.sections;
		}
		this.assemSecs = this.assembly.sections;
		this.assemKeys = this.assemSecs.map(s => s.key);
		this.nodes = this.sections.map(s => CT.dom.div(s.name));
	},
	init: function(opts) { // document OR (assembly AND ondone())
		this.opts = opts;
		this.load();
		this.launch();
	}
});