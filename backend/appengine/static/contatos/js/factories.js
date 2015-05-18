angular.module("rest", []).factory('ContatoApi', function($http){
    return {
        salvar: function(contato) {
            return $http.post('/contatos/home/save', contato);
        },
        buscarPorId: function(id) {
            return $http.post('/contatos/home/editar_form/' + id);
        },
        deletarPorId: function(id) {
            return $http.post('/contatos/home/delete/' + id);
        }
    };
});