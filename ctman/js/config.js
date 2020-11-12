{
	"classes": {
		"document": {
			"title": "bigger centered document_title",
			"template": "margined padded bordered round document_template",
			"hazards": "margined padded bordered round document_hazards",
			"form": "margined padded bordered round document_form",
			"image": "margined padded bordered round document_image",
			"settings": "margined padded bordered round document_settings",
			"build": "margined padded bordered round document_build"
		},
		"section": {
			"form": "margined padded bordered round section_form",
			"image": "margined padded bordered round section_image",
			"sections": "margined padded bordered round section_sections"
		},
		"template": {
			"form": "margined padded bordered round template_form",
			"image": "margined padded bordered round template_image",
			"sections": "margined padded bordered round template_sections",
			"injections": "margined padded bordered round template_injections",
			"injection": "margined padded bordered round inline-block template_injection"
		}
	},
	"help": {
		"templates": [
			"Menus",
			"Template and section menus are on the left side. Click 'new template' or 'new section' to start a fresh one.",
			"Templates",
			"Each template has a description, which you can write up using the embedded rich text editor. Bold, italics, and colors should all work.",
			"Click 'inject variable' to pop in a variable.",
			"Templates - Sections",
			"Click 'add section' to add a new section to the template. For a given section in the template's listing, click 'move' to adjust position or remove.",
			"Sections",
			"As is the case with templates, each section has a rich text description that supports variable injection.",
			"Also after the manner of templates, sections may have other sections embedded within them.",
			"Click 'headerless' to omit the section title from the final document.",
			"Any image file that you drag onto the 'image' section will be injected into the final document.",
			"--",
			"Terry Notes: see document page notes regarding variables; rich text editor may need work -- let me know if anything is broken!"
		],
		"documents": [
			"Menu",
			"The document selection menu is on the left. Click 'new document' to start a fresh one.",
			"Template",
			"Click 'swap' to select a template. Templates are created on the templates page. Sections and subsections can be clicked on and off.",
			"Client Logo",
			"Drag your image onto the 'drag file here' section, or click for an upload dialog. This image will appear on the first page of the final document.",
			"PDF Build",
			"Click the button to rebuild your document. Click the link to view/download it.",
			"Injections",
			"The values you provide for these fields will be injected into the final document. You can add injection flags to a document section via the 'inject variable' button in the section editor (or manually, by typing the variable name surrounded by double curly brackets, e.g. {{manager}} - see templates page)",
			"Hazards",
			"The hazards you select will end up in a table (with full information) in the final document.",
			"--",
			"Terry Note: currently, injections and hazards are defined in the configuration - would you like to provide us with appropriate lists, or would you prefer a away to define these yourself on the fly? We may, for instance, consider creating an interface for defining table-ish (hazard-like) categories and populating them with data."
		]
	},
	"declarations": [{
		"name": "CLIENT"
	}, {
		"isTA": true,
		"name": "SITE"
	}, {
		"name": "ICS PROJECT NO."
	}],
	"template": [{
		"isTA": true,
		"wyz": "nonbsp restricted tables spellcheck fullscreen charmap",
		"name": "description",
		"blurs": ["please describe", "please expand", "tell all here"]
	}],
	"injections": [{
		"name": "manager",
		"blurs": ["manager's name", "who is the manager?"]
	}, {
		"name": "location",
		"blurs": ["where is it?", "location"]
	}, {
		"isTA": true,
		"name": "description",
		"blurs": ["what's the big idea?", "please describe", "tell me more"]
	}],
	"hazards": {
		"chemical": ["Arsenic", "Lead", "4,4 DDE"]
	},
	"subs": {
		"one month": "10.00",
		"one year": "100.00"
	}
}