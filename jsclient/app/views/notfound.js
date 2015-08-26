"use strict";


// The AllIsDust 404 View
// -------------------------
Sonar.Views.NotFound = AllIsDust.Views.BaseView.extend({

    template: Handlebars.templates.NotFound,

    initialize: function() {
        this.renderViewWithFade();
        AllIsDust.Events.on("router:notfound", this.renderViewWithFade, this);
    },

    render: function() {
        var template = this.template();
        this.$el.html(template);
        return this;
    }

});
