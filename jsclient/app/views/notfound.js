"use strict";


// The AllIsDust 404 View
// -------------------------
Sonar.Views.NotFound = Sonar.Views.BaseView.extend({

    template: Handlebars.templates.NotFound,

    initialize: function() {
        this.renderViewWithFade();
        Sonar.Events.on("router:notfound", this.renderViewWithFade, this);
    },

    render: function() {
        var template = this.template();
        this.$el.html(template);
        return this;
    }

});
