"  Использовать ресурсы броузера для генерации текста и его разделения по словам. "
" Если броузер не работает с библиотекой Faker в броузере, то делам запрос нга API "
" Если не работают асинхронные запросы, то делаем запрос с получением документа целиком "
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
        throw new Error();
    }
    if (!USE_API_FAKER && !USE_BROWSER_FAKER && !USE_SUBMIT_AND_PAGE_RELOAD) {
        throw new Error();
    }
    };
    check_configuration();

    (() => {
        var form_validation = (is_debug=false) => {
            let form = document.forms[0];
            let text = form.querySelector(".form-control").value;
            if (text == "") {
                return false;
            }
            var bad_chars_in_word = new RegExp(/\b[^-\s]\b/, "s");  // Плохие символы внутри слова
            var bad_word = new RegExp(/\b[^a-zA-Z]+\b/, "s");  // Всё слово целиком
            var words = text.split(" ");
            for (var i = 0; i < words.length; i++) {
                if (words[i].match(bad_word)) {
                    if (is_debug) {
                        return words[i];
                    }
                    return false;
                }
                if (words[i].match(bad_chars_in_word)) {
                    if (is_debug) {
                        return words[i];
                    }
                    return false;
                }
            }
            return true;
        };
        var generate_text = (ev) => {
            ev.stopPropagation();
            ev.preventDefault();
            var text = CustomFaker.lorem.text();
            add_into_form(text);
        };
        var add_into_form = (text) => {
            document.forms[0].querySelector(".form-control").value = text;
        };
        var xhr_send_text_to_api = (ev) => {
            ev.preventDefault();
            var dumps = (str) => {
                var filter = (arr_t) => {
                    " Заменить символы в конце слова (предложения, оборота... итп)"
                    var result_arr = arr_t.slice(0);
                    var word_r = new RegExp(/\w+|[а-яА-Я]+[\,\.;]$/, "s");
                    for (var i = 0; i < arr_t.length; i++) {
                        var match = arr_t[i].match(word_r);
                        if (match) {
                            var match = match[0];
                            let symbol = match.slice(match.length - 1, match.length);
                            let word = result_arr[i];
                            result_arr[i] = word.slice(0, word.indexOf(symbol)) + word.slice(word.indexOf(symbol) + 1, word.length);
                        }
                    }
                    return result_arr;
                };
                var to_small_case = (arr) => {
                    var small_words = [];
                    while (arr.length) {
                        let word = arr.pop();
                        small_words.push(word);
                    }
                    return small_words;
                };
                const form = new FormData();
                var arr = str.split(" ");
                var arr = filter(arr);
                var arr = to_small_case(arr);
                for (var i = 0; i < arr.length; i++) {
                    form.append("words", arr[i]);
                }
                return form;
            };
            if (!form_validation()) {
                document.forms[0].getQuerySelector("form-control").setCustomValidity("Текст неразборчив или пуст");
                return;
            }
            var request = new XMLHttpRequest();
            request.open("POST", XHR_API_URL, true);
            request.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            //request.setRequestHeader("Content-Type", "multipart/form-data");
            request.send(dumps(document.forms[0].querySelector(".form-control").value));
        };
        document.querySelector(".generate").addEventListener("click", generate_text);
        document.querySelector(".submit").addEventListener("click", xhr_send_text_to_api);
    })();

};
