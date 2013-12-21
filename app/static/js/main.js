(function() {
  require(['config'], function(config) {
    requirejs.config(config);
    return require(["app"], function(app) {
      return "use strict";
    });
  });

}).call(this);
