"use strict";


module.exports = function(grunt) {

    // Project configuration
    grunt.initConfig({

        pkg: grunt.file.readJSON("package.json"),

        handlebars: {
            compile: {
                options: {
                    namespace: "Handlebars.templates",

                    // We take only the file names
                    processName: function(filePath) {
                        var pieces = filePath.split("/");
                        var fileName = pieces[pieces.length - 1];
                        return fileName.split(".")[0];
                    },
                    processPartialName: function(filePath) {
                        var pieces = filePath.split("/");
                        return pieces[pieces.length - 1];
                    },

                    // Remove leading/trailing spaces in templates
                    processContent: function(content) {
                        content = content.replace(/^[\x20\t]+/mg, "")
                                         .replace(/[\x20\t]+$/mg, "")
                                         .replace(/^[\r\n]+/, "")
                                         .replace(/[\r\n]*$/, "\n");
                        return content;
                    }
                },
                files: {
                    "app/templates.js": ["handlebars/**/*.handlebars"]
                }
            }
        },

        uglify: {
            options: {
                banner: "/*! <%= pkg.name %> <%= grunt.template.today(\"yyyy-mm-dd\") %> */\n",
                sourceMap: grunt.option("source-map", true)
            },
            build: {

                // Keep in mind the the order matters, do not re-arrange these
                // unless you know the file does not depend on a prior one.
                src: [

                    // Namespaces
                    "app/namespace.js",

                    // Templates - Note this file is generated with Handlebars
                    "app/templates.js",

                    // Models
                    "app/models/session.js",
                    "app/models/user.js",
                    "app/models/error.js",

                    // Collections

                    // Views
                    "app/views/common.js",
                    "app/views/errors.js",
                    "app/views/menus.js",
                    "app/views/login.js",
                    "app/views/home.js",
                    "app/views/settings.js",
                    "app/views/manageusers.js",
                    "app/views/notfound.js",

                    // Routers
                    "app/router.js",

                    // Main app
                    "app/sonar.js"
                ],
                dest: "../static/js/<%= pkg.name %>.min.js"
            }
        },

        retire: {
            js: [

                // Application code
                "app/**/*.js",

                // Libraries
                "../static/js/**/*.js"
            ],
            node: ["."],
            options: {
                verbose: false,
                packageOnly: true,
                jsRepository: "https://raw.github.com/RetireJS/retire.js/master/repository/jsrepository.json",
                nodeRepository: "https://raw.github.com/RetireJS/retire.js/master/repository/npmrepository.json"
            }
        }

    });

    // Plugins
    grunt.loadNpmTasks("grunt-contrib-uglify");
    grunt.loadNpmTasks("grunt-contrib-handlebars");
    grunt.loadNpmTasks("grunt-retire");

    // Default tasks
    grunt.registerTask("default", ["handlebars", "uglify", "retire"]);

};
