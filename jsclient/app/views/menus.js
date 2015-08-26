"use strict";


// Admin Menu View
// -----------------
Sonar.Views.AdminMenu = Backbone.View.extend({

    tagName: "li",
    template: Handlebars.templates.AdminMenu,
    attributes: {
        "class": "dropdown"
    },

    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },

    cleanup: function() {
        // Required method
    }

});


// User Menu View
// ----------------
Sonar.Views.UserMenu = Backbone.View.extend({

    tagName: "div",
    template: Handlebars.templates.UserMenu,

    render: function() {
        var data = this.model.toJSON();
        this.$el.html(this.template(data));
        if (this.model.get("is_admin")) {
            var submenu = new Sonar.Views.AdminMenu({
                model: this.model
            });
            this.$("#top-menu-rightnav").prepend(submenu.render().el);
        }
        return this;
    },

    cleanup: function() {
        // Required method
    }

});


// Public Menu View
// ------------------
Sonar.Views.PublicMenu = Backbone.View.extend({

    tagName: "div",
    template: Handlebars.templates.PublicMenu,

    render: function() {
        this.$el.html(this.template());
        return this;
    },

    cleanup: function() {
        // Required method
    }

});
