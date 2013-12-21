(function() {
  var currentTimeLive;

  currentTimeLive = function() {
    return setInterval(function() {
      return $('.current-date').text(datetime().format('MMMM Do YYYY, h:mm:ss a'));
    }, 1000);
  };

}).call(this);
