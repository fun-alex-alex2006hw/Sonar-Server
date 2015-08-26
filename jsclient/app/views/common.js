"use strict";


// Select From Collection View
// -----------------------------
Sonar.Views.SelectFromCollection = Backbone.View.extend({

    tagName: "div",
    template: Handlebars.templates.SelectFromCollection,
    attributes: {
        "class": "form-group"
    },

    initialize: function(options) {
        this.options = options;
        this.collection.on("reset", this.render, this);
        this.collection.on("update", this.render, this);
        this.collection.fetch();
    },

    render: function() {
        this.$el.html(this.template({
            "select-id": this.options["select-id"],
            "title": this.options.title,
            "models": this.collection.toJSON()
        }));
        return this;
    }

});
