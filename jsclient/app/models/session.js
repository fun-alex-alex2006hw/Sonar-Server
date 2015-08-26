"use strict";


// Session Model
// ---------------
Sonar.Models.Session = Backbone.Model.extend({

    urlRoot: "session",
    defaults: {
        "username": "",
        "password": "",
        "data": "",
        "expires": null,
        "is_admin": false,
        "debug": false
    },

    isValid: function() {
        // TODO: Better checks for this, like actually checking the timestamp
        return this.get("expires") !== null ? true : false;
    }

});
