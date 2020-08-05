# ctman
Manual generation framework.


# Back (Init Config)

    syms = {
    	".": ["_man.py"],
    	"html": ["man"],
    	"js": ["man"]
    }
    model = {
    	"ctman.model": ["*"]
    }
    routes = {
    	"/_man": "_man.py"
    }
    requires = ["ctuser"]
    

# Front (JS Config)

## core.config.ctman
### Import line: 'CT.require("core.config");'
    {
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
        }
    }