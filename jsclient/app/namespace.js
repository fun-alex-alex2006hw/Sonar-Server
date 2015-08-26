"use strict";


// Sonar Global Namespace
window.Sonar = {
    Models: {},
    Collections: {},
    Views: {},
    Router: {},
    Events: _.extend({}, Backbone.Events)
};


// Template Helper Functions
Handlebars.registerHelper("toHex", function(number) {
    return "0x" + parseInt(number, 10).toString(16);
});

Handlebars.registerHelper("inc", function(value) {
    return parseInt(value) + 1;
});

Handlebars.registerHelper("dec", function(value) {
    return parseInt(value) - 1;
});

Handlebars.registerHelper("floor", function(value) {
    return Math.floor(parseInt(value));
});


// Helper to fire events on keypresses
$(document).keyup(function(event) {

    // <enter>
    if (event.keyCode === 13) {
        Sonar.Events.trigger("keypress:enter");
    }

});


// Helper function so we don't have to parse cookies
window.getCookie = function(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }
};

// Save the original method, and add a CSRF token to every request
Backbone._sync = Backbone.sync;
Backbone.sync = function(method, model, options, error) {

    options.beforeSend = function(xhr) {
        if (!window.session) {
            xhr.setRequestHeader("X-SONAR", "unauthenticated");
        } else {
            xhr.setRequestHeader("X-SONAR", window.session.get("data"));
        }
        xhr.setRequestHeader("X-Xsrftoken", window.getCookie("_xsrf"));
    };

    options.complete = function(xhr) {
        if (xhr.status === 403) {
            console.log("[sync] API call failed authentication");
            Sonar.Events.trigger("router:logout");
        }
    };

    // Call the original method, with our extra options
    return Backbone._sync(method, model, options, error);
};


// Additional methods for Views that use the whole page
// ------------------------------------------------------
Sonar.Views.BaseView = Backbone.View.extend({

    tagName: "div",
    attributes: {
        "class": "container"
    },

    cleanup: function() {

    }

});


Sonar.Views.BaseSubView = Backbone.View.extend({

    tagName: "div",
    cleanup: function() {

    }

});
