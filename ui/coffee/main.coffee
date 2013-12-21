require ['config'], (config) ->
  requirejs.config(config)

  require ["app"], (app)->
    "use strict"