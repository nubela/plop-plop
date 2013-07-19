PLOP_URL = ""
CONTENT_CACHE = {}

loadUrl = (url) ->
    window.open url, "_system"

initTemplates = ->
    #panel
    panel_html = $("#panel-template").html()
    panel_template = Handlebars.compile(panel_html)
    $(".panel").html panel_template()

    #footer
    #    footer_html = $("#footer-template").html()
    #    footer_template = Handlebars.compile(footer_html)
    #    $(".footer").html(footer_template())

    #triffer changes
    $($.mobile.activePage).trigger "create"

initPhonegap = ->
    $.mobile.allowCrossDomainPages = true
    $.support.cors = true
    $.mobile.phonegapNavigationEnabled = true
    $.mobile.defaultPageTransition = 'slide'
    $.mobile.page.prototype.options.domCache = true

$(document).on 'pageinit', ->
    $('img').retina("@2x")
    FastClick.attach document.body
    initPhonegap()

    $(document).on 'pageshow', ->
        initTemplates()

    $(document).delegate ".link", "vclick", ->
        url = $(this).attr("href")
        loadUrl(url)

    $.ajax
        url: PLOP_URL
        timeout: 10