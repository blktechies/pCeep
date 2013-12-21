#global define 

@app = window.app ? {}

define ["jquery", "moment", "underscore.string"], ($, datetime) ->
  "use strict"
  app.datetime = datetime
  
  $ ->
    console.log "A wide aray of techies."

    $('.human.datestamp').each () ->
        $(this).text(datetime(_.str.trim($(this).text())).local().fromNow())

    # display content after all scripts are ready
    $('.content').show()