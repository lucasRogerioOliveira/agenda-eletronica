angular.module('inputs', []);
angular.module('inputs').config(function($interpolateProvider){
   $interpolateProvider.startSymbol('{[');
   $interpolateProvider.endSymbol(']}');
});


angular.module('inputs').directive('formInput', function(){
    return{
       restrict: 'E',
       replace: true,
       templateUrl: '/static/input/html/form_input.html'
    };
});