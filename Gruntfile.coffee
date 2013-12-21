#!
# * Gruntfile
# * @author Alvaro Muir, @alvaromuir
# 
"use strict"

###
Grunt module
###
module.exports = (grunt) ->
  ###
  Dynamically load npm tasks
  ###
  require("matchdep").filterDev("grunt-*").forEach grunt.loadNpmTasks

  ###
  Grunt config
  ###
  grunt.initConfig
    pkg: grunt.file.readJSON("package.json")

    ###
    Set project info
    ###
    project:
      base: "./"
      src: "ui"
      app: "app"
      dist: "<%= project.app %>/static"
      assets: "<%= project.src %>/bower_components"
      coffee: "<%= project.src %>/coffee"
      sass: "<%= project.src %>/sass"
      css: "<%= project.dist %>/css/*.css"
      js: "<%= project.dist %>/js/{,*/}*.js"

    ###
    Project banner
    Dynamically appended to CSS/JS files
    Inherits text from package.json
    ###
    tag:
      banner: "/*!\n" + " * <%= pkg.name %>\n" + " * <%= pkg.title %>\n" + " * <%= pkg.url %>\n" + " * @author <%= pkg.author %>\n" + " * @version <%= pkg.version %>\n" + " * Copyright <%= pkg.copyright %>. <%= pkg.license %> licensed.\n" + " */\n"
    
    ###
    Compile CoffeeScript files to JavaScript
    https://github.com/gruntjs/grunt-contrib-coffee
    Compiles all coffeescript
    ###
    coffee:
      dist:
        files: [
          expand: true
          cwd: "<%= project.coffee %>"
          src: "{,*/}*.coffee"
          dest: "<%= project.dist %>/js/"
          ext: ".js"
        ]

    ###
    Compile sass/SCSS files
    https://github.com/gruntjs/grunt-contrib-compass
    Compile Compass to CSS
    ###
    compass:
      dev:
        options:
          config: "<%= project.sass %>/config.rb"
          basePath: "<%= project.base %>"
          app: "stand_alone"
          sassDir: "<%= project.sass %>"
          specify: "<%= project.sass %>/style.scss"
          cssDir: "<%= project.dist %>/css"
          imagesDir: "<%= project.dist %>/img"
          javascriptsDir: "<%= project.js %>"
          fontsDir: "<%= project.dist %>/img/fonts"
          environment: "development"
          outputStyle: "expanded"

      dist:
        options:
          config: "<%= project.sass %>/config.rb"
          basePath: "<%= project.base %>"
          app: "stand_alone"
          sassDir: "<%= project.sass %>"
          specify: "<%= project.sass %>/style.unprefixed.scss"
          cssDir: "<%= project.dist %>/css"
          imagesDir: "<%= project.dist %>/img"
          javascriptsDir: "<%= project.js %>"
          fontsDir: "<%= project.dist %>/img/fonts"
          environment: "production"
          outputStyle: "compact"



    ###
    Concatenate JavaScript files
    https://github.com/gruntjs/grunt-contrib-concat
    Imports all .js files and appends project banner
    ###
    concat:
      dev:
        files:
          "<%= project.dist %>/js/scripts.js": "<%= project.dist %>/js/components/{,*/}*.js"

      options:
        stripBanners: true
        nonull: true
        banner: "<%= tag.banner %>"


    ###
    Uglify (minify) JavaScript files
    https://github.com/gruntjs/grunt-contrib-uglify
    Compresses and minifies all JavaScript files into one
    ###
    uglify:
      options:
        banner: "<%= tag.banner %>"

      dist:
        files:
          "<%= project.dist %>/js/scripts.min.js": "<%= project.dist %>/js/{,*/}*.js"

    ###
    Autoprefixer
    Adds vendor prefixes if need automatcily
    https://github.com/nDmitry/grunt-autoprefixer
    ###
    autoprefixer:
      options:
        browsers: ["last 2 version", "safari 6", "ie 9", "opera 12.1", "ios 6", "android 4"]

      dev:
        files:
          "<%= project.dist %>/css/style.min.css": ["<%= project.dist %>/css/style.unprefixed.css"]

      dist:
        files:
          "<%= project.dist %>/css/style.prefixed.css": ["<%= project.dist %>/css/style.unprefixed.css"]


    ###
    CSSMin
    CSS minification
    https://github.com/gruntjs/grunt-contrib-cssmin
    ###
    cssmin:
      dev:
        options:
          banner: "<%= tag.banner %>"

        files:
          "<%= project.dist %>/css/style.min.css": ["<%= project.src %>/bower_components/normalize-css/normalize.css", "<%= project.css %>"]

      dist:
        options:
          banner: "<%= tag.banner %>"

        files:
          "<%= project.dist %>/css/style.min.css": ["<%= project.src %>/bower_components/normalize-css/normalize.css", "<%= project.css %>"]

    
    ###
    Build bower components
    https://github.com/yatskevich/grunt-bower-task
    ###
    bower:
      dev:
        dest: "<%= project.dist %>/components/"

      dist:
        dest: "<%= project.dist %>/components/"


    ###
    Clear files and folders
    https://github.com/gruntjs/grunt-contrib-clean
    ###
    clean: {
      default: ["<%= project.js %>", "<%= project.css %>"]
    }

    ###
    Runs tasks against changed watched files
    https://github.com/gruntjs/grunt-contrib-watch
    Watching development files and run concat/compile tasks
    Livereload the browser once complete
    ###
    watch:
      coffee:
        files: ["<%= project.src %>/coffee/{,*/}*.coffee"]
        tasks: ["coffee:dist"]

      compass:
        files: "<%= project.src %>/sass/{,*/}*.{scss,sass}"
        tasks: ["compass:dev", "cssmin:dev", "autoprefixer:dev"]



  ###
  Default task
  Run `grunt` on the command line
  ###
  grunt.registerTask "default", ["compass:dev", "coffee:dist", "autoprefixer:dev", "cssmin:dev", "bower:dev", "concat:dev"]
  

  ###
  Build task
  Run `grunt build` on the command line
  Then compress all JS/CSS files
  ###
  grunt.registerTask "build", ["compass:dist", "coffee:dist", "autoprefixer:dist", "cssmin:dist", "bower:dist",   "clean:dist", "uglify"]

