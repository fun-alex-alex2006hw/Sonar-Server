"use strict";


// AllIsDust Base Router
// -----------------------
// Extended to redirect user to #login if no valid session exists on the server
var BaseRouter = Backbone.Router.extend({

    execute: function(callback, args, name) {

        // Check to see if our current session is valid
        if (name !== "login" && !window.session.isValid()) {
            window.router.navigate("#login", { trigger: true });
            return false;
        }

        // Execute the route
        if (callback) {
            callback.apply(this, args);
        }
    }

});


// AllIsDust Router
// -----------------
Sonar.Router = BaseRouter.extend({

    BASE_TITLE: "Sonar: ",

    routes: {

        // Home routes
        "": "index",
        "login": "login",
        "home": "home",

        // User settings
        "settings": "settings",

        // Admin
        "manageusers": "manageusers",

        // Logout
        "logout": "logout",

        // Catch all
        "*other": "notfound"
    },

    index: function() {
        this.login();  // Identical to #login for now
    },

    login: function() {
        console.log("[Router] -> login");
        document.title = this.BASE_TITLE + "Login";
        Sonar.Events.trigger("router:login");
    },

    home: function() {
        console.log("[Router] -> home");
        document.title = this.BASE_TITLE + "Home";
        Sonar.Events.trigger("router:home");
    },

    settings: function() {
        console.log("[Router] -> settings");
        document.title = this.BASE_TITLE + "Settings";
        Sonar.Events.trigger("router:settings");
    },

    manageusers: function() {
        console.log("[Router] -> manageusers");
        document.title = this.BASE_TITLE + "Manage Users";
        Sonar.Events.trigger("router:manageusers");
    },

    logout: function() {
        console.log("[Router] -> logout");
        Sonar.Events.trigger("router:logout");
    },

    notfound: function() {
        console.log("[Router] -> notfound");
        document.title = this.BASE_TITLE + "Not Found";
        Sonar.Events.trigger("router:notfound");
    }

});
