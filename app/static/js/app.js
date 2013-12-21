(function() {
  var _ref;

  this.app = (_ref = window.app) != null ? _ref : {};

  define(["jquery", "moment", "underscore.string"], function($, datetime) {
    "use strict";
    app.datetime = datetime;
    return $(function() {
      console.log("A wide aray of techies.");
      $('.human.datestamp').each(function() {
        return $(this).text(datetime(_.str.trim($(this).text())).local().fromNow());
      });
      return $('.content').show();
    });
  });

}).call(this);
