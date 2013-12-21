# Some frontend utilities

currentTimeLive = () ->
  setInterval () ->
    $('.current-date').text(datetime().format('MMMM Do YYYY, h:mm:ss a'))
  , 1000