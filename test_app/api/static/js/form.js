"  Использовать ресурсы броузера для генерации текста и его разделения по словам. "
" Если броузер не работает с библиотекой Faker в броузере, то делам запрос на API /get-text "
" Если не работают асинхронные запросы, то делаем запрос с получением документа и сгенерированного текста целиком "
import {USE_API_FAKER, USE_BROWSER_FAKER, USE_SUBMIT_AND_PAGE_RELOAD, CustomFaker} from '/static/js/settings.js';
const API_GET_TEXT_URL = get_urls()["text_gen"];
const XHR_API_URL = get_urls()["page_url"];
const CSRF_TOKEN = get_token();

window.onload = () => {
    var check_configuration = () => {
    if (!CSRF_TOKEN) {
        throw new Error();
    }
    if (USE_API_FAKER && USE_BROWSER_FAKER && USE_SUBMIT_AND_PAGE_RELOAD) {
        throw new Error("Установите значение true для одной из 3 констант");
    }
    if (!USE_API_FAKER && !USE_BROWSER_FAKER && !USE_SUBMIT_AND_PAGE_RELOAD) {
        throw new Error("Установите значение true для одной из 3 констант");
    }
    };
    check_configuration();

    (() => {
        var dumps = (str) => {
            " 1) Черновая разбивка текста на отдельные слова "
            var split_by_space = (str_) => {
                return str_.split(" ");
            };
            var filter = (arr_t) => {
                "2) Очистить слово от не относящихся к слову символов "
                var result_arr = [];
                var word_r = new RegExp(/\w+|[а-яА-Я]+/, "s");
                for (var i = 0; i < arr_t.length; i++) {
                    var match = arr_t[i].match(word_r);
                    if (match && match.length) {
                        result_arr.push(match[0]);
                    }
                }
                return result_arr;
            };
            var to_small_case = (arr) => {
                " 3) Всё в единый регистр - нижний "
                var small_words = [];
                while (arr.length) {
                    let word = arr.pop();
                    word = word.toLowerCase();
                    small_words.push(word);
                }
                return small_words;
            };
            return to_small_case(filter(split_by_space(str)));
        };
        var is_valid = (event_or_null) => {
            var value = !event_or_null === null ? event_or_null.target.value :
            document.forms[0].querySelector(".form-control").value;
            if (!value.length) {
                document.forms[0].getElementsByTagName("textarea")[0].setCustomValidity("Текст неразборчив или пуст");
                document.forms[0].getElementsByTagName("textarea")[0].className += " error";
                return false;
            }
                if (dumps(value).length > 0) {
                    document.forms[0].getElementsByTagName("textarea")[0].setCustomValidity("");
                    document.forms[0].getElementsByTagName("textarea")[0].classList.remove("error");
                } else {
                    document.forms[0].getElementsByTagName("textarea")[0].setCustomValidity("Текст неразборчив или пуст");
                    document.forms[0].getElementsByTagName("textarea")[0].className += " error";
                    return false;
                }
            return true;
        };
        var reset_form = (event) => {
            if (!event.target.status == 201) {
                return;
            }
            document.forms[0].getElementsByTagName("textarea")[0].value = "";
        };
        var load_random_text_from_api = (ev) => {
            var request = new XMLHttpRequest();
            request.addEventListener("load", function(event) {
                if (event.target.status == 200) {
                    var text = JSON.parse(event.target.responseText);
                    document.forms[0].getElementsByTagName("textarea")[0].value = text["text"];
                    is_valid();
                }
            });
            request.open("POST", API_GET_TEXT_URL);
            request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            request.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            request.send();
            if (ev) {
                ev.stopPropagation();
                ev.preventDefault();
            }
        };
        var generate_text = (ev) => {
            try {
                var text = CustomFaker.lorem.text();
                } catch(er) {
                load_random_text_from_api(null);
                return;
            }
            add_into_form(text);
            ev.stopPropagation();
            ev.preventDefault();
            document.forms[0].getElementsByTagName("textarea")[0].classList.remove("error");            
        };
        var add_into_form = (text) => {
            document.forms[0].querySelector(".form-control").value = text;
        };
        var xhr_send_text_to_api = (ev) => {
            ev.preventDefault();
            var on_success_redirect = (e) => {
                if (event.target.status == 201) {
                    console.log(JSON.parse(event.target.responseText));
                    window.location.href = (document.location.origin + JSON.parse(event.target.responseText)).replace(/['"«»]/g, '');
                }
            };
            var add_to_formdata = (arr) => {
                var form = new FormData();
                while (arr.length > 0) {
                    form.append("words", arr.pop(0));
                }
                return form;
            };
            var request = new XMLHttpRequest();
            request.addEventListener("load", reset_form);
            request.addEventListener("load", on_success_redirect);
            request.open("POST", XHR_API_URL, true);
            request.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            var cleaned_data = dumps(document.forms[0].querySelector(".form-control").value);
            if (!is_valid()) {
               return;
            }
            const form = add_to_formdata(cleaned_data);
            request.send(form);
        };
        if (USE_SUBMIT_AND_PAGE_RELOAD) {
            return;
        }
        if (USE_BROWSER_FAKER) {
            document.querySelector(".generate").addEventListener("click", generate_text);
        }
        if (USE_API_FAKER) {
            document.querySelector(".generate").addEventListener("click", load_random_text_from_api);
        }
        document.querySelector(".submit").addEventListener("click", xhr_send_text_to_api);
        document.forms[0].getElementsByTagName("textarea")[0].addEventListener("keyup", is_valid);
    })();
};
