"use strict";


// Settings View
// ---------------
Sonar.Views.Settings = Sonar.Views.BaseView.extend({

    template: Handlebars.templates.Settings,
    events: {
        "click #change-password": "changePassword"
    },

    initialize: function() {
        this.model.on("change", this.render, this);
        this.model.fetch();
    },

    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },

    changePassword: function() {
        this.model.set("password", $("#new-password").val());
        this.model.save(null, {
            success: function(model, response) {
                console.log("[Settings] Change password success!");
                this.showSuccess(response.responseJSON);
            },
            error: function(model, response) {
                console.log("[Settings] Change password error!");
                this.showError(response.responseJSON);
            }
        });
    }

});
