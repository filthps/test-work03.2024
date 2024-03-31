"  Поддержка ~= ES5 "
var API_GET_TEXT_URL = get_urls()["text_gen"];
var XHR_API_URL = get_urls()["page_url"];
var STATIC_URL = get_static_url();
var CSRF_TOKEN = get_token();

document.onload = function() {
    function check_configuration() {
    if (!CSRF_TOKEN) {
        throw new Error();
    }
    if (USE_API_FAKER && USE_BROWSER_FAKER && USE_SUBMIT_AND_PAGE_RELOAD) {
        throw new Error();
    }
    if (!USE_API_FAKER && !USE_BROWSER_FAKER && !USE_SUBMIT_AND_PAGE_RELOAD) {
        throw new Error();
    }
    };
    check_configuration();

    (function(){
        function xhr_load_text_from_api(ev) {};
        function xhr_send_text_to_api() {
            function dumps() {};

            var request = new XMLHttpRequest();
            request.open("POST", XHR_API_URL);
            request.setRequestHeader("x-csrf-token", CSRF_TOKEN);
            request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            request.setRequestHeader("Content-Type", "application/json");
        };
        if (document.attachEvent) {
            document.querySelector(".generate").attachEvent("click", xhr_load_text_from_api);
        } else {
            document.querySelector(".generate").addEventListener("click", xhr_load_text_from_api);
        }
    })();
};
