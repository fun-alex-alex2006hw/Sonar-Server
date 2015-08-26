"use strict";


// Initialize and start the application
$(document).ready(function() {

    window.app = new Sonar.Views.AppView();
    window.menu = new Sonar.Views.MenuView();

    // Either restore saved session data, or start unauthenticated
    if (window.localStorage.session !== undefined) {
        try {
            var data = JSON.parse(window.localStorage.session);
            window.session = new Sonar.Models.Session(data);
            var menu = new Sonar.Views.UserMenu({ model: window.session });
            window.menu.renderMenu(menu);
            console.log("[Sonar] Restored saved session data");
        } catch (error) {
            console.log("[Sonar] Failed to parse local session data");
            delete window.localStorage.session;
            window.session = new Sonar.Models.Session();
        }
    } else {
        window.session = new Sonar.Models.Session();
    }

    // Start the router
    console.log("[Sonar] Starting router ...");
    window.router = new Sonar.Router();
    Backbone.history.start();
});



// This view wraps all the others and handles the cleanup/etc
// ------------------------------------------------------------
Sonar.Views.MenuView = Backbone.View.extend({

    el: "#page-menu-wrapper",

    initialize: function() {
        this.currentMenu = null;
    },

    renderMenu: function(menu) {
        console.log("[MenuView] Rendering menu");
        if (this.currentMenu) {
            console.log("[MenuView] Cleaning up old menu");
            this.currentMenu.cleanup();
            this.currentMenu.remove();
        }
        this.addFadeIn();
        this.$el.html(menu.render().el);
        this.currentMenu = menu;
    },

    addFadeIn: function() {
        this.$el.addClass("fadeIn");
        var _this = this;  // That's right, JS is terrible
        setTimeout(function() {
            _this.$el.removeClass("fadeIn");
        }, 500);
    }

});


// This view wraps all the others and handles the cleanup/etc
// ------------------------------------------------------------
Sonar.Views.AppView = Backbone.View.extend({

    el: "#page-content-wrapper",
    tagName: "div",

    initialize: function() {
        console.log("[AppView] Initializing main app view");
        this.menu = new Sonar.Views.MenuView();
        this.currentView = null;
        var _this = this;

        // Login Page
        Sonar.Events.on("router:login", function() {
            delete window.session;
            delete window.localStorage.session;
            var menu = new Sonar.Views.PublicMenu();
            _this.menu.renderMenu(menu);
            var session = new Sonar.Models.Session();
            var view = new Sonar.Views.Login({ model: session });
            _this.renderView(view);
        });

        // Home Page
        Sonar.Events.on("router:home", function() {
            var recentJobs = new Sonar.Collections.RecentJobs();
            var view = new Sonar.Views.Home({ collection: recentJobs });
            _this.renderView(view);
        });

        // Not Found
        Sonar.Events.on("router:notfound", function() {
            var view = new Sonar.Views.NotFound();
            _this.renderView(view);
        });

        // Settings
        Sonar.Events.on("router:settings", function() {
            var me = new Sonar.Models.Me();  // The current user model
            var view = new Sonar.Views.Settings({ model: me });
            _this.renderView(view);
        });

        // Logout
        Sonar.Events.on("router:logout", function() {
            delete window.session;
            delete window.localStorage.session;
            window.router.navigate("#login", { trigger: false });
            location.reload(true);
        });

        // Admin
        Sonar.Events.on("router:manageusers", function() {
            var users = new Sonar.Collections.AllUsers();
            var view = new Sonar.Views.ManageUsers({ collection: users });
            _this.renderView(view);
        });
    },

    // This method takes a view and renders it with a fancy CSS3 animation
    renderView: function(view) {
        console.log("[AppView] Rendering new view");
        var _this = this;
        this.fadeViewOut(function() {
            console.log("[AppView] Rendering new view");
            _this.$el.html(view.render().el);
            _this.currentView = view;
        });
    },

    fadeViewOut: function(next) {
        console.log("[AppView] Fading out old view");
        this.$el.addClass("fadeOut");
        var _this = this;  // That's right, JS is terrible
        setTimeout(function() {
            // Okay the old view has been faded out, now clean it up before
            // rendering the new view.
            if (_this.currentView) {
                console.log("[AppView] Cleaning up current view");
                _this.currentView.cleanup();
                _this.currentView.remove();
            }
            _this.$el.removeClass("fadeOut");
            _this.fadeViewIn(next);
        }, 500);
    },

    fadeViewIn: function(next) {
        console.log("[AppView] Fading in new view");
        this.$el.addClass("fadeIn");
        var _this = this;  // That's right, JS is terrible
        setTimeout(function() {
            _this.$el.removeClass("fadeIn");
        }, 500);
        if (next) {
            next();
        }
    }

});
