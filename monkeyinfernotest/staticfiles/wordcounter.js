
function WordCounterCtrl($scope, $http){
    $scope.words = [];
    
    $scope.doCalculation = function() {
        $http.post(' /ajax/',
            {article : $scope.article_text}
        ).success(function(data) {
                $scope.words = data;
                $scope.article_text='Paste another one';
                }        
        )
    };
}