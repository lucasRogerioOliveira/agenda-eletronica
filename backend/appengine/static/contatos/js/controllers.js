angular.module('contatoApp', ['contatoModulo']).controller('ContatoController', function($scope, ContatoApi){
    $scope.contato = {
        id: '',
        nome:'',
        email: '',
        celular: '',
        logradouro: ''
    };
    $scope.contatos = contatos;
    $scope.mostrarFormFlag = false;
    $scope.mostrarOuEsconderForm = function(){
        $scope.mostrarFormFlag =  !$scope.mostrarFormFlag;
    };
    $scope.editar = function(id, index){
        var promessa = ContatoApi.buscarPorId(id);
        promessa.success(function(result){
            $scope.contato = result.contato;
            $scope.index = index;
            $scope.mostrarFormFlag = true;
        });
    };
    $scope.deletar = function(id, index){
        var promessa = ContatoApi.deletarPorId(id);
        promessa.success(function(){
            $scope.index = index;
            $scope.contatos.splice(index,1);
        });
    }
});
