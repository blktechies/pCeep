(function() {
  require.config({
    paths: {
      'jquery': '../components/jquery',
      'underscore': '../components/lodash',
      'moment': '../components/moment',
      'socket-io': '../components/socket.io',
      'underscore.string': '../components/underscore.string'
    },
    shim: {
      'socket-io': {
        exports: 'io'
      },
      'underscore.string': {
        exports: '_',
        deps: ['underscore'],
        init: function(UnderscoreString) {
          return _.mixin(UnderscoreString);
        }
      }
    }
  });

}).call(this);
