"use strict";


// User Table View
// -----------------
Sonar.Views.UserTableRow = Backbone.View.extend({

    tagName: "tr",
    template: Handlebars.templates.UserTableRow,

    render: function() {
        var data = this.model.toJSON();
        this.$el.html(this.template(data));
        return this;
    }

});


// Edit User View
// ----------------
Sonar.Views.EditUser = Backbone.View.extend({

    tagName: "div",
    template: Handlebars.templates.EditUser,

    render: function() {
        var data = this.model.toJSON();
        this.$el.html(this.template(data));
        return this;
    }

});


// All Users View
// ----------------
Sonar.Views.ManageUsers = Sonar.Views.BaseView.extend({

    template: Handlebars.templates.ManageUsers,
    events: {
        "click #show-new-user-modal": "showCreateUser",
        "click #create-new-user": "createUser",
        "click #show-edit-user-modal": "showEditUser",
        "click #edit-user": "editUser",
        "click #show-delete-user": "showDeleteUser",
        "click #delete-user": "deleteUser"
    },

    initialize: function() {
        this.collection.on("reset", this.render, this);
        this.collection.on("update", this.render, this);
        this.collection.fetch();
    },

    render: function() {
        this.$el.html(this.template());
        this.collection.each(function(user) {
            var row = new Sonar.Views.UserTableRow({ model: user });
            this.$("#all-users").append(row.render().el);
        }, this);
        return this;
    },

    // TODO: Make this function more generic
    showError: function(resp) {
        var error = new Sonar.Models.Error(resp);
        var view = new Sonar.Views.AlertError({ model: error });
        this.$("#create-new-user-errors").html("");
        this.$("#create-new-user-errors").append( view.el );
    },

    showCreateUser: function() {
        // Autofocus on form when the modal is displayed
        this.$("#create-new-user-modal").on("shown.bs.modal", function() {
            $("#new-user-name").focus();
        });
        this.$("#create-new-user-modal").modal("show");
    },

    createUser: function() {
        var user = new Sonar.Models.User();
        user.set("name", this.$("#new-user-name").val());
        user.set("password", this.$("#new-user-password").val());
        user.set("is_admin", this.$("#new-user-is-admin").checked);
        var _this = this;  // How do people put up with this crap?
        user.save(null, {
            success: function() {
                console.log("[ManageUsers] Successfully created new user");
                // Toggling the modal doesn't remove the body properties
                // I blame JS, not bootstrap for this shit behavoir
                _this.$("#create-new-user-modal").modal("toggle");
                $("body").removeClass("modal-open");
                $(".modal-backdrop").remove();
                _this.collection.fetch();
            },
            error: function(model, response) {
                console.log("[ManageUsers] Error while creating new user");
                _this.showError(response.responseJSON);
            }
        });
    },

    showEditUser: function() {

    },

    editUser: function() {

    },

    showDeleteUser: function() {

    },

    deleteUser: function() {

    }

});
