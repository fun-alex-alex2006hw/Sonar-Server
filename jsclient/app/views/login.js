"use strict";


// Login View
// ------------
Sonar.Views.Login = Sonar.Views.BaseView.extend({

    template: Handlebars.templates.Login,
    events: {
        "click #login-button": "loginAttempt"
    },

    initialize: function() {
        Sonar.Events.on("keypress:enter", this.loginAttempt, this);
    },

    render: function() {
        $(document.body).addClass("eldrazi-splash");
        this.$el.html(this.template());
        return this;
    },

    showError: function(resp) {
        var error = new Sonar.Models.Error(resp);
        var view = new Sonar.Views.AlertError({ model: error });
        this.$("#login-errors").html( view.el );
    },

    loginAttempt: function() {
        console.log("[LoginView] Creating new session");
        var session = new Sonar.Models.Session({
            "username": this.$("#login-username").val(),
            "password": this.$("#login-password").val()
        });
        var _this = this;
        session.save(null, {
            success: function(model, response) {
                _this.loginSuccess(model, response);
            },
            error: function(model, response) {
                _this.showError(response.responseJSON);
            },
            wait: true
        });
    },

    loginSuccess: function(model) {
        console.log("[LoginView] Login success!");
        window.localStorage.session = JSON.stringify(model.toJSON());
        window.session = model;

        // Remove body splash
        if ($(document.body).hasClass("eldrazi-splash")) {
            $(document.body).removeClass("eldrazi-splash");
        }
        var menu = new Sonar.Views.UserMenu({ model: window.session });
        window.menu.renderMenu(menu);
        window.router.navigate("#home", { trigger: true });
    }

});
