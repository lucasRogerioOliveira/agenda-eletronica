angular.module('contatoModulo', ["rest"]);
angular.module('contatoModulo').config(function($interpolateProvider){
   $interpolateProvider.startSymbol("{[");
   $interpolateProvider.endSymbol("]}");
});


angular.module('contatoModulo').directive('contatoForm', function(){
   return{
       restrict: 'E',
       replace: true,
       scope:{
           contato: "=?",
           contatos: "=",
           index: "=?"
       },
       templateUrl: '/static/contatos/html/contato_form.html',
       controller: function($scope, ContatoApi) {
           $scope.salvandoFlag = false;
           $scope.errosFlag = false;
           $scope.salvar = function () {
               $scope.salvandoFlag = true;
               var promessa = ContatoApi.salvar($scope.contato);
               promessa.success(function (contato) {
                   if ($scope.index !== undefined){
                       $scope.contatos[$scope.index] = contato;
                   } else {
                       $scope.contatos.unshift(contato);
                   }
                   console.log(contato);
                   $scope.id = '';
                   $scope.contato.nome = '';
                   $scope.contato.email = '';
                   $scope.contato.celular = '';
                   $scope.contato.bairro = '';
                   $scope.contato.logradouro = '';
                   $scope.contato.numero = '';
                   $scope.contato.cep = '';
                   $scope.errosFlag = false;
                   $scope.salvandoFlag = false;
               });
               promessa.error(function (result) {
                   console.log(result);
                   $scope.result = result;
                   $scope.salvandoFlag = false;
                   $scope.errosFlag = true;
               });
           }
       }
   };
});

angular.module("contatoModulo").directive("formInput", function(ContatoApi){
    return{
       restrict: "E",
       templateUrl: '',
       scope:{
            error_msg: "&",
            label: "&",
            value: "&",
            property: "&"
       },
       controller: function($scope){
            $scope.error_msg = false;
            $scope.label = "";
            $scope.value = "";
            $scope.property = "";
       }
    };

});