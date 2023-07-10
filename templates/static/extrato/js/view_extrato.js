const form = document.querySelector('form');
const selectConta = document.querySelector('select[name="conta"]');
const selectCategoria = document.querySelector('select[name="categoria"]');
const selectPeriodo = document.querySelector('select[name="periodo"]');

function urlParams() {
    let querySearch = window.location.search;
    querySearch = querySearch.substring(1);

    let params = querySearch.split('&');
    let paramsObj = {};

    for(let i = 0; i < params.length; i++) {
        let [key, value] = params[i].split('=');
        paramsObj[key] = value;

        if(key == 'reset_filters') {
            return false;
        }
    }

    return paramsObj;
}

let paramsObj = urlParams();

if(paramsObj) {
    let valueConta = paramsObj.conta;
    let valueCategoria = paramsObj.categoria;
    let valuePeriodo = paramsObj.periodo;

    selectConta.value = valueConta;
    selectCategoria.value = valueCategoria;
    selectPeriodo.value = valuePeriodo;
}