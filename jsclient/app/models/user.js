// User Model
// --------------
Sonar.Models.User = Backbone.Model.extend({

    urlRoot: "users",
    defaults: {
        "created": "",
        "name": "",
        "jobs": [],
        "organizations": [],
        "is_admin": false
    }

});

// Me Model
// ----------
// This model is the current user
Sonar.Models.Me = AllIsDust.Models.User.extend({

    urlRoot: "me"

});
