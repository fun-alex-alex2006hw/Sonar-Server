"use strict";


// Alert Error View
// ------------------------
Sonar.Views.AlertError = Backbone.View.extend({

    tagName: "div",
    template: Handlebars.templates.ErrorAlert,
    attributes: {
        "class": "alert alert-danger alert-dismissible",
        "role": "alert"
    },

    initialize: function() {
        this.render();
    },

    render: function() {
        console.log(this.model.toJSON());
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }

});
